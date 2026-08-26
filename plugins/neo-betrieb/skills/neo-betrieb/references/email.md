# E-Mail-Zustellbarkeit

Der Versand meldet Erfolg, sobald der Server die Nachricht angenommen
hat. Ob sie im Posteingang landet, sagt das nicht. Eine Anwendung, deren
Kennwort-Zurücksetzen im Spam liegt, ist für den Anwender kaputt.

## Die drei Einträge im DNS

| Eintrag | Was er tut | Was falsch läuft, wenn er fehlt |
| --- | --- | --- |
| **SPF** | Nennt die Server, die für die Domäne senden dürfen | Fremde Server dürfen in Ihrem Namen senden; Empfänger stufen ab |
| **DKIM** | Signiert die Nachricht, der Empfänger prüft die Signatur | Keine Echtheitsprüfung möglich |
| **DMARC** | Sagt, was bei fehlgeschlagener Prüfung passieren soll, und liefert Berichte | Niemand erfährt, wer in Ihrem Namen sendet |

**Reihenfolge beim Einrichten:**

1. SPF setzen — **alle** sendenden Dienste aufnehmen: Anwendung,
   Mailserver, Newsletter-Dienst, Ticketsystem, CRM, Zahlungsanbieter.
   Ein vergessener Dienst ist ein Zustellproblem, das später niemand
   zuordnet.
2. DKIM je sendendem Dienst einrichten und die Signatur prüfen.
3. DMARC zunächst **beobachtend** setzen, Berichte auswerten, und erst
   nach ein paar Wochen ohne Fehlalarm verschärfen. Wer sofort scharf
   stellt, blockiert die eigene Post.
4. Nach jeder Änderung an den sendenden Diensten alle drei erneut
   prüfen.

Weitere Punkte, die die Zustellung tragen: ein sauberer Rückwärtsverweis
für die sendende IP, eine gültige Absenderdomäne mit Website, und keine
gemischte Nutzung derselben Domäne für Massenversand und Systempost.

## Trennung von Transaktion und Werbung

**Getrennte Absender oder getrennte Subdomänen.** Eine Werbekampagne mit
vielen Abmeldungen und Beschwerden zieht sonst die Rechnung, das
Kennwort-Zurücksetzen und die Bestellbestätigung mit nach unten.

| Art | Beispiel | Einwilligung |
| --- | --- | --- |
| Transaktion | Kennwort, Rechnung, Bestätigung, Statusmeldung | aus dem Vertragsverhältnis |
| Werbung | Newsletter, Angebote, Rückholmails | Einwilligung, mit Nachweis und Abmeldung |

Werbepost braucht eine Abmeldung, die in einem Schritt funktioniert, und
die Abmeldung wirkt sofort (Skill `neo-recht`).

## Rückläufer und Beschwerden

- **Harte Rückläufer** (Adresse existiert nicht) werden dauerhaft
  gesperrt. Weiter zu senden schadet der Reputation der Domäne.
- **Weiche Rückläufer** (Postfach voll, Server nicht erreichbar) werden
  begrenzt wiederholt und dann ebenfalls gesperrt.
- Beschwerden über Rückmeldeschleifen der großen Anbieter werden
  ausgewertet und führen zur Abmeldung, nicht zu einer weiteren Mail.
- Die Sperrliste ist Teil der Anwendung, nicht eine Datei auf einem
  Rechner.

## Aufbau der Nachricht

- **Immer ein Textteil**, nicht nur HTML. Ein Bild als einziger Inhalt
  ist der Klassiker im Spamordner.
- Betreff sagt, worum es geht, ohne Ausrufezeichen und ohne Versalien.
- Absendername und Absenderadresse gehören zusammen und sind
  wiedererkennbar.
- Eine Antwortadresse, die jemand liest — kein Postfach ins Nichts.
- Bilder mit Alternativtext, Kontrast beachtet, Breite begrenzt
  (Skill `neo-design`).
- Vektorlogos gehen in Mailprogrammen nicht: eine Rasterfassung
  mitliefern (Skill `neo-contao`).
- Pflichtangaben im Fuß, bei Werbung zusätzlich die Abmeldung
  (Skill `neo-recht`).

## Prüfung vor dem Livegang

- [ ] SPF, DKIM und DMARC gesetzt und geprüft — für **jeden** sendenden
      Dienst.
- [ ] Testversand an die großen Anbieter, jeweils Posteingang geprüft,
      nicht nur den Versandbericht.
- [ ] Textteil vorhanden, Darstellung in mehreren Programmen angesehen.
- [ ] Rückläuferbehandlung greift, Sperrliste funktioniert.
- [ ] Abmeldung wirkt sofort.
- [ ] Zugangsdaten des Mailversands stehen in der Konfiguration, nie im
      Code und nie in einem Modulendpunkt (Skill `neo-sicherheit`).
