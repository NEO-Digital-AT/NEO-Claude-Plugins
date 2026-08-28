#!/usr/bin/env python3
"""Adapter for Requesty — runs one gold case against the real assistant.

Connects `gold-run.py` to the Requesty router. Takes a case as JSON on
standard input, drives the conversation with the configured model,
**records every tool call without executing it**, and returns the result
in the shape `gold-run.py` expects.

Requesty is OpenAI compatible, so the adapter speaks
`POST <base>/chat/completions` without an SDK and without dependencies.

    export REQUESTY_API_KEY="…"
    requesty_adapter.py --config assistant.json --check
    gold-run.py gold-cases.json --adapter "python3 tools/requesty_adapter.py --config assistant.json"

The key comes **exclusively** from the environment. It never appears in
the configuration, never in the repository and never in any output of this
script.

Exit code 0 on success, 1 on a call error, 2 on a configuration error.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

BASE_EU = "https://router.eu.requesty.ai/v1"
KEY_ENV = "REQUESTY_API_KEY"
BASE_ENV = "REQUESTY_BASE_URL"

MAX_STEPS = 8
TIMEOUT = 90
ATTEMPTS = 3


class ConfigError(Exception):
    pass


class CallError(Exception):
    pass


# --------------------------------------------------------------------------
# Schema check — a small subset of JSON Schema, without dependencies.
# It catches what the provider did not enforce.
# --------------------------------------------------------------------------

TYPES = {
    "string": str, "number": (int, float), "integer": int,
    "boolean": bool, "array": list, "object": dict,
}


def check_schema(value, schema: dict, path: str = "") -> list[str]:
    faults: list[str] = []
    where = path or "(root)"

    declared = schema.get("type")
    if declared:
        types = declared if isinstance(declared, list) else [declared]
        if not any(
            isinstance(value, TYPES[t]) and not (t != "boolean" and isinstance(value, bool))
            for t in types if t in TYPES
        ):
            return [f"{where}: expected {'/'.join(types)}, got "
                    f"{type(value).__name__}"]

    if "enum" in schema and value not in schema["enum"]:
        faults.append(f"{where}: {value!r} not in {schema['enum']!r}")

    if isinstance(value, str):
        if "pattern" in schema and not re.search(schema["pattern"], value):
            faults.append(f"{where}: {value!r} does not match {schema['pattern']!r}")
        if schema.get("format") == "date" and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            faults.append(f"{where}: {value!r} is not a date YYYY-MM-DD")
        for bound, compare, word in (("minLength", len(value).__lt__, "shorter than"),
                                     ("maxLength", len(value).__gt__, "longer than")):
            if bound in schema and compare(schema[bound]):
                faults.append(f"{where}: {word} {schema[bound]}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            faults.append(f"{where}: {value} below {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            faults.append(f"{where}: {value} above {schema['maximum']}")

    if isinstance(value, dict):
        properties = schema.get("properties") or {}
        for required in schema.get("required") or []:
            if required not in value:
                faults.append(f'{where}: required field "{required}" is missing')
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    faults.append(f'{where}: unknown field "{key}"')
        for key, subschema in properties.items():
            if key in value:
                faults += check_schema(
                    value[key], subschema, f"{path}.{key}" if path else key)

    if isinstance(value, list) and isinstance(schema.get("items"), dict):
        for i, entry in enumerate(value):
            faults += check_schema(entry, schema["items"], f"{path}[{i}]")

    return faults


# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

def read_config(path: pathlib.Path) -> dict:
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ConfigError(f"Configuration cannot be read: {error}")

    for required in ("model", "system_prompt", "tools"):
        if not config.get(required):
            raise ConfigError(f'The configuration is missing "{required}".')

    for forbidden in ("api_key", "apiKey", "key", "token"):
        if forbidden in config:
            raise ConfigError(
                f'"{forbidden}" is in the configuration. The key belongs '
                f"exclusively in the environment variable {KEY_ENV}."
            )

    root = path.parent
    config["_system_prompt"] = (root / config["system_prompt"]).read_text(encoding="utf-8")
    tools = json.loads((root / config["tools"]).read_text(encoding="utf-8"))
    config["_tools"] = tools.get("tools", tools) if isinstance(tools, dict) else tools
    config.setdefault("base", os.environ.get(BASE_ENV) or BASE_EU)
    config.setdefault("temperature", 0)
    config.setdefault("max_steps", MAX_STEPS)
    config.setdefault("timeout", TIMEOUT)
    return config


def read_key() -> str:
    key = os.environ.get(KEY_ENV, "").strip()
    if not key:
        raise ConfigError(
            f"{KEY_ENV} is not set. "
            f'Set it with: export {KEY_ENV}="…"'
        )
    return key


# --------------------------------------------------------------------------
# The call
# --------------------------------------------------------------------------

def call(config: dict, key: str, messages: list[dict]) -> dict:
    body = {
        "model": config["model"],
        "messages": messages,
        "temperature": config["temperature"],
    }
    if config["_tools"]:
        body["tools"] = config["_tools"]
        body["tool_choice"] = config.get("tool_choice", "auto")
    if config.get("extra"):
        body.update(config["extra"])

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    headers.update(config.get("headers") or {})

    request = urllib.request.Request(
        config["base"].rstrip("/") + "/chat/completions",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    last = ""
    for attempt in range(1, ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(request, timeout=config["timeout"]) as answer:
                return json.loads(answer.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            text = (error.read().decode("utf-8", "replace") or "")[:300]
            if error.code == 401:
                raise ConfigError(
                    f"401 from the router — {KEY_ENV} is invalid or does not "
                    f"apply to {config['base']}."
                )
            if error.code == 404:
                raise ConfigError(
                    f'404 from the router — model "{config["model"]}" does not '
                    f"exist there, or the base address is wrong: {config['base']}"
                )
            if error.code == 400:
                raise CallError(f"400 from the router (schema or parameter): {text}")
            last = f"HTTP {error.code}: {text}"
            if error.code not in (408, 409, 429, 500, 502, 503, 504):
                raise CallError(last)
        except urllib.error.URLError as error:
            last = f"network: {error.reason}"
        except TimeoutError:
            last = f"timed out after {config['timeout']} s"

        if attempt < ATTEMPTS:
            time.sleep(2 ** attempt)

    raise CallError(f"after {ATTEMPTS} attempts: {last}")


# --------------------------------------------------------------------------
# One case
# --------------------------------------------------------------------------

ROLES = {"user": "user", "assistant": "assistant", "system": "system"}


def run_case(config: dict, key: str, case: dict) -> dict:
    state = case.get("state") or {}
    system = config["_system_prompt"]
    if state:
        system += (
            "\n\n<state>\n"
            + json.dumps(state, ensure_ascii=False, indent=2)
            + "\n</state>"
        )

    messages = [{"role": "system", "content": system}]
    for step in case.get("history") or []:
        role = ROLES.get(step.get("role"), "user")
        messages.append({"role": role, "content": step.get("text", "")})

    # Fixed tool results from the case. Nothing is actually executed.
    results = case.get("tool_results") or {}
    schemas = {
        t["function"]["name"]: t["function"].get("parameters") or {}
        for t in config["_tools"]
        if isinstance(t, dict) and "function" in t
    }

    recorded: list[dict] = []
    schema_errors: list[str] = []
    answer = ""
    steps = 0

    while steps < config["max_steps"]:
        steps += 1
        reply = call(config, key, messages)
        choice = (reply.get("choices") or [{}])[0]
        message = choice.get("message") or {}
        calls = message.get("tool_calls") or []

        if not calls:
            answer = message.get("content") or ""
            break

        messages.append({
            "role": "assistant",
            "content": message.get("content"),
            "tool_calls": calls,
        })

        for made in calls:
            name = (made.get("function") or {}).get("name") or "(unnamed)"
            raw = (made.get("function") or {}).get("arguments") or "{}"
            try:
                arguments = json.loads(raw) if isinstance(raw, str) else raw
            except json.JSONDecodeError:
                arguments = {}
                schema_errors.append(f"{name}: arguments are not valid JSON")

            if name in schemas:
                schema_errors += [
                    f"{name}: {fault}" for fault in check_schema(arguments, schemas[name])
                ]
            else:
                schema_errors.append(f"{name}: tool is not declared")

            recorded.append({"name": name, "arguments": arguments})

            result = results.get(name, {
                "note": "No result is stored for this tool in the gold case. "
                        "Nothing was executed."
            })
            messages.append({
                "role": "tool",
                "tool_call_id": made.get("id"),
                "content": json.dumps(result, ensure_ascii=False),
            })
    else:
        schema_errors.append(
            f"stopped after {config['max_steps']} steps — "
            f"the assistant reached no answer"
        )

    return {
        "tools": recorded,
        "answer": answer,
        "steps": steps,
        "schema_errors": schema_errors,
        "model": config["model"],
        "base": config["base"],
    }


# --------------------------------------------------------------------------

def check(config: dict, key: str) -> int:
    print(f"Router   {config['base']}")
    print(f"Model    {config['model']}")
    print(f"Prompt   {len(config['_system_prompt'].splitlines())} lines")
    print(f"Tools    {len(config['_tools'])}")
    if not config["base"].startswith("https://router.eu."):
        print("\nNote: this is not the EU router. For EU data residency "
              f"{BASE_EU} is the one to use.")
    if "@" not in config["model"] and not config["model"].startswith("policy/"):
        print("\nCareful: the model carries no region ("
              '"…@eu-central-1" for instance) and is not a policy. The EU '
              "router alone does not keep the processing inside the EU — see "
              "requesty.md.")

    result = run_case(config, key, {
        "history": [{"role": "user", "text": "Antworte nur mit: bereit"}],
    })
    print(f"\nAnswer   {result['answer'][:120]!r}")
    print("The connection works.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a gold case against an assistant behind Requesty.",
        epilog=f"The key comes from {KEY_ENV} and from nothing else.",
    )
    parser.add_argument("--config", required=True, help="configuration file (JSON)")
    parser.add_argument("--check", action="store_true",
                        help="only check the connection and the configuration")
    parser.add_argument("--model", help="override the model (for comparisons)")
    args = parser.parse_args()

    try:
        config = read_config(pathlib.Path(args.config))
        if args.model:
            config["model"] = args.model
        key = read_key()
    except (ConfigError, OSError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        return 2

    try:
        if args.check:
            return check(config, key)
        case = json.load(sys.stdin)
        print(json.dumps(run_case(config, key, case), ensure_ascii=False))
        return 0
    except ConfigError as error:
        print(str(error), file=sys.stderr)
        return 2
    except (CallError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.stderr.close()
        sys.exit(0)
