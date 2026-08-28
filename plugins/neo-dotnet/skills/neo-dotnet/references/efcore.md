# Entity Framework Core

Lesekonvention siehe `SKILL.md`.

> **Vor dem Schreiben lesen:** die offizielle Doku der eingesetzten
> EF-Core-Fassung. Verhalten bei Verfolgung, Aufteilung von Abfragen und
> Migrationen unterscheidet sich zwischen Hauptfassungen.

## Abfragen

- **Kein N+1.** Verbundene Daten werden **mitgeladen** (`Include`) oder
  in einer zweiten, bewussten Abfrage geholt — nie in einer Schleife.
- **Die Abfragezahl wird gemessen**: Protokollierung im Test einschalten
  und die Zahl als Erwartung festhalten. Eine Zahl, die niemand kennt,
  wächst.
- **Lesen ohne Verfolgung** (`AsNoTracking`), wo nichts geschrieben wird.
- **Projektion statt ganzer Entität**: Der Endpunkt holt die Felder, die
  er zurückgibt, nicht das ganze Modell mit allen Verweisen.
- **Kein `IQueryable` über die Schichtgrenze.** Was die Fachschicht
  verlässt, ist eine Liste oder ein Ergebnis — sonst entscheidet die
  Oberfläche über Datenbankarbeit.
- **Paginierung ist Pflicht**, wo die Menge wachsen kann; eine
  unbegrenzte Liste ist ein Ausfall mit Ansage.

## Schreiben

- **Eine Arbeitseinheit je Anwendungsfall**: sammeln, einmal speichern.
- **Transaktion, wo mehrere Aggregate zusammen gültig sein müssen.**
- **Nebenläufigkeit wird behandelt**, nicht gehofft: Zeitstempelspalte
  oder Versionsfeld, und der Konflikt hat eine Antwort.
- **Keine Schleife mit `SaveChanges` darin.**

## Migrationen

- **Vorwärtsgerichtet, ohne Datenverlust.** Neue Spalten nullbar oder
  mit Vorgabewert; eine Umbenennung ist Anlegen, Umkopieren, Entfernen —
  in getrennten Schritten, nicht in einem.
- **Jede Migration wird gegen eine Kopie eines echten Bestands
  geprüft**, nicht gegen eine leere Datenbank.
- **Kein automatisches Migrieren beim Start** in der Produktion: die
  Migration ist ein eigener, protokollierter Schritt der Ausrollung
  (Skill `neo-deployment`).
- **Zurückrollen ist geplant**, bevor ausgerollt wird — mindestens als
  beschriebener Weg.

## Mandantentrennung

- **Die Trennung liegt im Datenzugriff**, als Abfragefilter am Modell —
  nicht in der Sorgfalt des Aufrufers.
- **Ein Test beweist sie**: Ein Konto des einen Mandanten fragt Daten
  des anderen an und bekommt nichts. Ohne diesen Test gilt die Trennung
  als nicht vorhanden (Skill `neo-sicherheit`).
- **Wo der Filter absichtlich umgangen wird** (Wartung, Auswertung),
  steht das benannt und begründet an einer Stelle.

## Modell und Datenbank

- **Das Modell beschreibt die Datenbank vollständig**: Schlüssel,
  Fremdschlüssel, Löschart, Indizes, Feldlängen, Genauigkeit von
  Dezimalwerten (Geld: siehe Skill `neo-code`, `references/datenmodell.md`).
- **Indizes gehören zur Abfrage, die sie braucht** — und werden mit
  Zahlen begründet, nicht mit Gefühl.
- **Keine Geschäftsregel in der Datenbank**, außer sie ist eine
  Integritätsregel; was fachlich entschieden wird, entscheidet der Code.
