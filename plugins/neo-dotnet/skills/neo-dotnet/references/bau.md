# Der Bau ist streng — und zentral

Lesekonvention siehe `SKILL.md`.

> **Was der Bau nicht erzwingt, gilt nach drei Monaten nicht mehr.**

Sprache, Projektschnitt und Stil stehen im Skill `neo-code`,
`references/dotnet.md`. Hier steht, **wie** daraus ein Blocker wird, den
niemand versehentlich umgeht.

## Eine Stelle, nicht je Projekt

Die Strenge steht in **`Directory.Build.props`** im Wurzelverzeichnis und
gilt damit für jedes Projekt der Mappe. In einer einzelnen `.csproj`
steht sie nicht — dort wird sie beim nächsten neuen Projekt vergessen.

```xml
<Project>
  <PropertyGroup>
    <Nullable>enable</Nullable>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <EnableNETAnalyzers>true</EnableNETAnalyzers>
    <AnalysisLevel>latest-all</AnalysisLevel>
    <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
    <ImplicitUsings>enable</ImplicitUsings>
    <ContinuousIntegrationBuild
        Condition="'$(CI)' == 'true'">true</ContinuousIntegrationBuild>
  </PropertyGroup>
</Project>
```

- **`TreatWarningsAsErrors` ist nicht verhandelbar.** Eine Warnung, die
  man wegsehen kann, wird weggesehen — und zwar von allen, ab dem Tag,
  an dem die erste stehen bleibt.
- **`EnforceCodeStyleInBuild`** zieht die Regeln der `.editorconfig` in
  den Bau. Ohne das ist die `.editorconfig` eine Bitte.
- **Eine Unterdrückung trägt eine Begründung**, in derselben Zeile oder
  in der Projektkonfiguration — nie verstreut und nie kommentarlos.
- **Die Stufe wird nicht gesenkt, um grün zu werden.** Wer sie senkt,
  legt vor, warum, und der Projektinhaber entscheidet (Kernregel 1).

## Pakete: eine Fassung, eine Quelle, eine Sperrdatei

- **Zentrale Paketverwaltung.** `Directory.Packages.props` im
  Wurzelverzeichnis, `ManagePackageVersionsCentrally` auf `true`, die
  Fassungen als `<PackageVersion>`; die Projekte nennen nur noch
  `<PackageReference>` ohne Fassung. Zwei Projekte mit zwei Fassungen
  desselben Pakets sind sonst der Normalfall, nicht die Ausnahme.
- **Sperrdatei ist Pflicht.** `RestorePackagesWithLockFile` auf `true`
  erzeugt `packages.lock.json`; die Datei wird **eingecheckt**. In der CI
  wird mit `dotnet restore --locked-mode` wiederhergestellt — schlägt
  fehl, sobald jemand eine Abhängigkeit ändert, ohne die Sperrdatei
  nachzuziehen. Für Bibliotheken, die weitergegeben werden, gilt das
  nicht (die Sperrdatei einer Bibliothek wirkt beim Verbraucher nicht).
- **Quellenzuordnung** (package source mapping): Jedes Paket kommt aus
  einer benannten Quelle. Ohne sie kann ein gleichnamiges Paket aus einer
  anderen Quelle gezogen werden — der klassische Angriff über die
  Lieferkette (Skill `neo-sicherheit`).
- **`NuGetAudit` an**, mit `NuGetAuditMode` auf `all`, damit auch
  mittelbare Abhängigkeiten gemeldet werden. Eine gemeldete Schwachstelle
  ist ein Blocker, kein Ticket für später.

## Der Bau ist reproduzierbar

- **Dieselbe Quelle liefert dasselbe Erzeugnis.** `global.json` legt die
  SDK-Fassung fest, `rollForward` eng gestellt; sonst ändert ein anderes
  SDK die mittelbaren Fassungen und die Sperrdatei bricht.
- **`ContinuousIntegrationBuild` in der CI**, damit die Pfade in den
  Symbolen nicht vom Rechner abhängen.
- **Kein Bau, der nur auf einem Rechner geht.** Läuft er nicht in einem
  frischen Container, gilt die Anwendung als nicht fertig
  (Skill `neo-deployment`).

## Architekturtests: die Schichtgrenze wird gemessen

`neo-code`, `references/dotnet.md` legt die Verweisrichtung fest —
`Domain` verweist auf nichts, `Api` kennt `Infrastructure` nicht. **Eine
Einbahnstraße ohne Schild ist keine.**

Deshalb ist ein **Architekturtest Pflicht**, sobald es mehr als ein
Projekt gibt. Er läuft als gewöhnlicher Test in der CI und schlägt fehl,
wenn jemand die Richtung dreht:

- `Domain` hat **keinen** Verweis auf `Infrastructure`, `Api` oder ein
  Rahmenwerk (EF Core, ASP.NET Core, Serialisierung).
- `Api` greift **nicht** unmittelbar auf `DbContext` zu.
- Kein Typ aus `Infrastructure` erscheint in einer öffentlichen Signatur
  von `Domain`.
- Typen, die eine Schnittstelle umsetzen, liegen in der Schicht, die sie
  umsetzen darf.

Umgesetzt mit einer Bibliothek für Architekturtests (etwa
`NetArchTest.Rules`) oder — schwächer, aber besser als nichts — durch
Projektverweise, die die falsche Richtung gar nicht erst erlauben.

**Der Projektverweis ist die stärkere Sperre**, weil er schon den Bau
bricht. Der Architekturtest ergänzt ihn dort, wo eine Regel innerhalb
eines Projekts gilt.

## Abnahme

- [ ] `Directory.Build.props` vorhanden, mit `Nullable`,
      `TreatWarningsAsErrors`, Analysestufe und
      `EnforceCodeStyleInBuild`.
- [ ] Keine Unterdrückung ohne Begründung; Liste der Unterdrückungen
      berichtet.
- [ ] `Directory.Packages.props` mit zentraler Fassungsverwaltung.
- [ ] `packages.lock.json` eingecheckt, CI stellt mit `--locked-mode`
      wieder her.
- [ ] Quellenzuordnung gesetzt, `NuGetAudit` an, null offene
      Schwachstellen.
- [ ] `global.json` mit fester SDK-Fassung.
- [ ] Architekturtest vorhanden und grün; die geprüften Regeln benannt.
- [ ] Bau in einem frischen Container gelaufen.
