# Contao-Bordmittel und Feldtypen

## Die erste Frage

Vor jeder Zeile Code: **Wie löst Contao das nativ?** Welches
Inhaltselement, welches Modul, welches Widget, welches Muster im Kern
gibt es dafür? Erst wenn die Antwort belegbar „gar keines" lautet,
entsteht eigener Code.

Nachschlagen statt raten: <https://docs.contao.org/5.x/manual/de/>

## Was Contao bereits mitbringt

| Aufgabe | Bordmittel |
| --- | --- |
| Seitenstruktur, Navigation, Weiterleitung, Zugriffsschutz | Seitentypen und Seiteneinstellungen |
| Gestaltung, Ausgabe von CSS und JS | Theme, Seitenlayout, Modul-Einbindung |
| Inhalte auf einer Seite | Artikel mit Inhaltselementen |
| Text mit Auszeichnung | Inhaltselement Text mit TinyMCE |
| Bild, Bildergalerie, Download, Downloadliste | eigene Inhaltselemente |
| Bildgrößen, Zuschnitt, Ausgabeformat, Dichte | **Imagesets** (Bildgrößen im Theme) |
| Aufzählung, Tabelle, Akkordeon, Slider, Player | eigene Inhaltselemente |
| Formulare samt Versand und Speicherung | Formulargenerator |
| Nachrichten, Blog, FAQ, Newsletter, Kalender | die jeweiligen Bundles |
| Mehrsprachigkeit | Seitenbäume je Sprache und Sprachverknüpfung |
| Suche, Sitemap, Feeds, Canonical | Kern-Einstellungen je Seite |
| Verweise auf Seiten, Dateien, Werte | **Insert-Tags** |

Nichts davon wird nachgebaut. Ein eigenes Galerie-Element neben dem
Contao-Element ist ein Fehler, auch wenn es hübscher aussieht.

## Templates tragen keinen Inhalt

- **Kein fester Text in einem Template.** Keine Überschrift, kein
  Fließtext, keine Beschriftung, keine Telefonnummer, keine Adresse,
  keine Jahreszahl. Alles kommt aus einem Feld.
- **Keine zusammengesetzten Pfade.** Ein Template baut nie
  `/files/…/{slug}.svg`. Die Datei kommt aus einem Datei-Picker, die
  UUID wird im Controller aufgelöst.
- **Insert-Tags statt Handarbeit** für Links, Dateien,
  Seiteneigenschaften und Umgebungswerte. Aufgelöst wird über den
  Insert-Tag-Parser, nicht mit einer eigenen Ersetzung.
- Ein Template enthält Struktur und Logik der Ausgabe — sonst nichts.

**Prüfung:** Alle Templates nach sichtbarem Text durchsuchen. Jeder
Treffer ist entweder ein fehlendes Feld oder eine fehlende Übersetzung.

## Feldtypen: was statt was

Diese Tabelle stammt aus dem NEO-Standardprompt für Contao und gilt
unverändert.

| Statt … | … Bordmittel nutzen |
| --- | --- |
| URL oder Alias als Text | **Seiten-Picker** (`rgxp => 'url'`, `dcaPicker => true`); Auflösung über den Insert-Tag-Parser |
| Icon-Name als Text | **Select** mit kuratierter Liste (`options_callback`, `chosen` für Suche) |
| Farbe oder Variante als Text | **Select** mit den echten Varianten |
| Logo oder Bild als Text, oder Auswahl aus einem Ordner-Scan | **Datei-Picker** (`fileTree`, `filesOnly`, `extensions` begrenzt, `fieldType`, `multiple`, `isSortable`) — der Redakteur kann im Dialog hochladen |
| HTML in einem Textfeld | **TinyMCE** (`rte => 'tinyMCE'`); im Template kein `<p>` darum, TinyMCE liefert bereits Absätze |
| Bild als Pfad | **fileTree** mit begrenzten Endungen |
| Wiederholzeilen als `a \| b \| c` | **Kind-Tabelle** (`ptable`/`ctable`, Muster `tl_form` → `tl_form_field`): jede Zeile ein echtes Formular mit Selects und Pickern |
| Kommagetrennte Aufzählung im Textfeld | **Listenelement** bzw. Kind-Tabelle |
| Tabelle als Textblock | **Kind-Tabelle** oder das Tabellen-Inhaltselement |

**Flache Listen** mit genau einem Wert je Zeile (etwa Schlagworte) dürfen
ein Listen-Assistent bleiben. Sobald eine Zeile zwei Angaben trägt, ist
es eine Kind-Tabelle.

Werden bestehende Daten umgebaut: Migrations-Befehl schreiben (alte Blobs
in die Kind-Tabelle), Controller mit Rückfall auf die Altdaten, damit die
Seite jederzeit läuft.

## Werte, die ein Fremdsystem selbst kennt

Liefert eine API ihre gültigen Werte (Modell-Listen, Verteiler,
Vorlagen), werden sie live als `options_callback` geladen und
zwischengespeichert — kein Freitextfeld, kein Abtippen.

Zwei Fallen, beide bereits eingetreten:

1. **Der Schlüssel muss zuerst gespeichert sein.** Solange keiner
   hinterlegt ist oder die API nicht antwortet, muss das Feld ein
   Textfeld bleiben (`onload_callback` schaltet um) — sonst sperrt man
   sich aus.
2. **Der gespeicherte Wert bleibt immer in der Optionsliste**, auch wenn
   die API ihn gerade nicht listet. Sonst zeigt Contao das Feld als leer
   und der Wert geht beim nächsten Speichern verloren. Fehlt der
   API-Schlüssel im Container, kommt die Liste leer zurück und bereits
   gesetzte Felder wirken plötzlich unbelegt.

## Redakteursrechte — vier Dinge, sonst 403

| Schlüssel | Bedeutung |
| --- | --- |
| `modules` | erlaubte Backend-Module |
| `alpty` | erlaubte Seitentypen — wird **auch beim Bearbeiten von Inhalten** geprüft, nicht nur beim Anlegen von Seiten |
| `cud` | Tabellenrechte (`create`, `update`, `delete`); ohne sie sieht der Redakteur Listen, kann aber nichts ändern |
| `alexf` | Feldrechte. Ein Feld gilt in Contao bereits als ausgeschlossen, sobald es einen `inputType` hat — ein ausdrückliches `exclude` ist nicht nötig. Wer nur auf `exclude` prüft, übersieht alle Kernfelder |

Dazu die Seitenrechte (`chmod`) mit den Präfixen `u` (Besitzer), `g`
(Gruppe), `w` (Welt). Redakteure bekommen Artikel- und Inhaltsrechte,
**keine** Rechte an der Seitenstruktur, an Themes, Layouts, Modulen,
Einstellungen, Benutzern oder am Formulargenerator.

Gegenprobe mit einem Testredakteur ist Pflicht: was er sehen soll, sieht
er; was er nicht darf, endet nachweislich in 403.

## Bilder

- Größen, Zuschnitt, Ausgabeformat und Dichte kommen **ausschließlich aus
  den Imagesets** im Theme. Sie werden im Backend gepflegt, nicht im
  Code.
- Keine zweite Bildverarbeitung neben Contao — kein eigener Wandler im
  Build, keine von Hand abgelegten Varianten.
- `width` und `height` kommen serverseitig aus der Datei, nie geraten.
- Unterhalb des ersten Bildschirms `loading="lazy"`, das LCP-Bild mit
  hoher Priorität.

## Häufige Fehler

- Ein Inhaltselement, das ein bestehendes nachbaut.
- Ein Template mit einem Satz darin.
- Ein Textfeld, wo Contao einen Picker hat.
- Eine Ordnerliste statt eines Datei-Pickers — ein neu hochgeladenes Bild
  wäre damit nicht wählbar.
- Konsolenbefehle als `root` ausgeführt: danach gehören Dateien dem
  falschen Benutzer und das Backend kann nicht mehr speichern.
