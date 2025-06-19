# PygameProjekt
Projekt von ....

## Meine Spielidee
### Spielesammlung von verschiedenen Klassikern und eigenen Ideen
#### FlappyBird
- Steuerung: mit Leertaste hochfliegen
- Spiel wird schneller über Zeit
- verschiedenfarbige "Pipes"
- Fluganimation
- einfache Kollosionserkennung mit pygame.Rect Klasse
- Wenn mit Pipe Kollidiert: GameOver
- Gameover: Menu mit zwei Möglichkeiten: Verlassen(q oder esc) oder nocheinmal spielen(r oder Leertaste)  -> wird auch aufgerufen, wenn das Fenster über X geschlossen werden soll
#### Jumping Frog: simpler Platformer
- Steuerung: Leertaste: Springen, A: nach links, D: nach rechts
- unendlich viele Platformen -> per Zufall wird eine neue Platform immer ein Stück weiter rechts oder links und ein Stück weiter oben erzeugt, wenn eine Platform zu weit nach unten kommt
- mit halber Geschwindigkeit scrollender Hintergrund, wie die Plattformen
- Gamover wenn der Spieler zu weit nach unten fällt
- Gamover wird genauso gemacht, wie bei FlappyBird
#### Pong
- Pong (wenn auch mit ein Paar Verbesserungen)

#### Mario
- Super Mario mit:
- Animationen
- Einem (theoretisch unendlich großen) System mit 2d 50x50 Pixel großen Teilen
- realistischer Physik

## Arbeit am Spiel
### 27.02.2025
#### Ziele

Heute möchte ich....
-     Jumping Frog beenden


#### Erreichte Ziele und mögliche Probleme
-      Jumping Frog beendet

####Noch verbesserungswürdig: 
-     Score, gameoversystem, bessere unendliche Plattformgeneration, einige Anpassungen an der Physik
....

### 13.3.25
..
#### Erreichte Ziele
-      Spiel weitergamacht: Pong
-      paddle klasse und Game Klasse fast fertig
-     circle klasse angefangen
...


### 20.03.2025

#### Erreichte Ziele
-      Pong Ball Klasse beendet, Button Klasse für bessere Menus angefangen.
Funktionen von der Button Klasse: 
-      getClicked: setzt den gegenwärtigen status mithilfe der Mouseposition und den Maustasten
-      draw: malt ein rechteck und rendert den ButtonText in der mitte des Buttons

### 27.03.2025

#### Erreichte Ziele
-      Button Klasse beendet
-      Einige Funktionen eingefügt: Gameover(Noch über button), Restart, Quit


### 3.04.2025

#### Erreichte Ziele
-      Bug Fixes: Ball prallt besser von den Paddles und Wänden ab.
-      Gameover wenn ball zu weit links/rechts

### 10.04.2025

#### Erreichte Ziele
-      Pong beendet: Scoresystem eingefügt: Zähler und Highscore, der dann in data.txt gespeichert wird wenn das spiel beendet wird.
-     Neue Spielidee: Mario (2d) 

### 15.5.2025

#### Erreichte Ziele
-        Mario: 
-        Grid Klasse draw methode beendet: jetzt werden alle Felder, die auf dem Bildschirm sichtbar sind mit dem dazugehörigen Bild gemalt.
-        Player Klasse Kamerabewegung hinzugefügt: Die Kamera folgt dem Spieler in einer abgerundeten Bewegung
-        Player Klasse draw Methode: Der Spielerwird anhand der gegenwärtgen Kameraposition (so wie alles andere) gemalt
-        Player Klasse move Methode: einfache Bewegung

### 22.5.2025

#### Erreichte Ziele
-      Pong: 
-      Höhere Numerische Stabilität durch Iterativen Physiksolver:
-      Der Ball bewegt sich jetzt in kleineren Schritten, jedoch mehrmals pro Wiederholung der Haupschleife
---
-      Mario:
-      Spielerbewegung, Kollosionserkennung und der Umgang damit. (auch iterativ: __move, __handle_collision und update Funktionen)
-      Animation des Spielers: Gehen, Rennen, Springen (__animate Funktion)