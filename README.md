![1](https://github.com/user-attachments/assets/79deccf4-195d-4cf2-8566-5256b2cde1c0)

# cherrypi

Raspberry Pi Zero 2 W based Portable Chess Computer


![1345](https://github.com/user-attachments/assets/e1ad9f5d-69b3-400c-b369-6a879702a258)
![2331](https://github.com/user-attachments/assets/85d27000-4344-44d7-8f23-d0c429c6f2c4)
![12](https://github.com/user-attachments/assets/6596596c-9a8d-4c6d-be01-3d6eb8d45f84)

# Cherrypi - über Kirschkuchen und Schachcomputer

Dieses Repository dokumentiert den Aufbau meines selbstgebauten Schachcomputers – ein persönliches Projekt, das von der Idee bis zur Umsetzung eine Reise voller Höhen und Tiefen war. Der Computer sollte ein Weihnachtsgeschenk sein, das nicht nur funktional, sondern auch emotional besonders ist. Obwohl er heute nicht funktionsfähig ist, bedeutet mir dieses Projekt eine Menge. Es war eine Reise mit vielen Höhen und Tiefen, ich habe sooo viel gelernt und hoffe darauf, dass dieses Projekt eines Tages (bald) von allen nachgebaut werden kann, die sich ein ähnliches Projekt wünschen. 


![IMG_8A8BB41F64B1-1](https://github.com/user-attachments/assets/8ce64253-fce1-460d-a680-53646f64a5ac)
![IMG_86837E7B299C-1](https://github.com/user-attachments/assets/5b5cac45-c3fe-4e87-bc9a-8b18aa3a05ca)

---

## 🛠️ **Funktionalität**

Der Cherrypi-Schachcomputer bietet:


1. **Eigenständige Schachfunktion:**
   - Nutzt **Stockfish** als Schach-Engine. Spielt auf etwa 2500er ELO. 
   - Steuere das Spiel mit einer 16-Tasten-Matrix (ähnlich einem tragbaren Brett).
   - Zeigt Spielinformationen auf einem **OLED-Display** an.

2. **Portabilität:**
   - Dank eines **UPS-Moduls** (mit Akku) und eines **Ein/Aus-Schiebeschalters** kann der Computer überall verwendet werden.

3. **Software-Integration:**
   - Automatischer Start in das Schachprogramm direkt beim Hochfahren.
   - Alle Funktionen laufen eigenständig – ohne Internetverbindung.

4. **Benutzerfreundliches Gehäuse:**
   - Ein 3D-gedrucktes Gehäuse schützt die Hardware.
   - Magnetverschluss für einfachen Zugriff auf die Elektronik.
   - 3D-gedruckte Keycaps für ein individuelles Schach-Feeling.

---
## 🎮 **Spielanleitung**

### **Tastenbelegung**
Die 16-Tasten-Matrix ist wie folgt organisiert:


| Taste (S1-S16) | Funktionalität         | Beschreibung                       |
|----------------|------------------------|------------------------------------|
| S1             | A/1                    | Spalte A oder Reihe 1              |
| S2             | B/2                    | Spalte A oder Reihe 1              |
| S3             | C/3                    | Spalte A oder Reihe 1              |
| S4             | D/4                    | Spalte A oder Reihe 1              |
| S5             | E/5                    | Spalte A oder Reihe 1              |
| S6             | F/6                    | Spalte A oder Reihe 1              |
| S7             | G/7                    | Spalte A oder Reihe 1              |
| S8             | H/8                    | Spalte A oder Reihe 1              |
| S9             | Dame                   | Bauernumwandlung in Dame           |
| S10            | Turm                   | Bauernumwandlung in Turm           |
| S11            | Läufer                 | Bauernumwandlung in Läufer         |
| S12            | Springer               | Bauernumwandlung in Springer       |
| S13            | Surrende               | Beendet Spiel durch Aufgave        |
| S14            | Clear                  | Löscht gesamte Eingabe             |
| S15            | Delete                 | Löscht letzte Ziffer von Eingabe   |
| S16            | Go                     | Bestätigt Eingabe                  |

### **Züge eingeben**
- Um einen Zug einzugeben, drücke **nacheinander zwei Felder**:
  - Das erste Feld ist die Startposition des Steins.
  - Das zweite Feld ist die Zielposition des Steins.
  - Beispiel: Um von `E2` nach `E4` zu ziehen, drücke die Tasten 5,2,5,4 (e2e4) und bestätige den Zug mit "Go". 

### **Sonderfunktionen**
- **Bauernumwandlung:**
  - Wird ein Bauer in die letzte Reihe bewegt, erscheint auf dem Display die Aufforderung zur Umwandlung.
  - Wähle mit den Tasten `A`, `B`, `C`, `D` die gewünschte Figur:
    - `A`: Königin
    - `B`: Turm
    - `C`: Läufer
    - `D`: Springer

- **Rochade:**
  - Gib den Zug des Königs an. Das System erkennt automatisch die Rochade, sofern legal.

- **Zug zurücknehmen:**
  - Halte die Taste `S16` gedrückt, um den letzten Zug zurückzunehmen.

- **Neues Spiel starten:**
  - Halte `S1` gedrückt, um das Spiel zurückzusetzen und eine neue Partie zu beginnen.

### **Display-Anzeige**

- Das OLED-Display zeigt:
  - Den aktuellen Zug.
  - Die letzten Züge.
  - Hinweise wie "Press any key to start" oder Fehler bei illegalen Zügen.

## 🔧 **Zusammenbau**

### **Benötigte Komponenten**
- **Raspberry Pi Zero W** (ohne Headerpins).
- **1,3-Zoll-OLED-Display** (I2C, 128x64 Pixel).
- **16-Tasten-Matrix**.
- **3D-gedrucktes Gehäuse** (STLs sind in diesem Repository verfügbar!).
- **3D-gedruckte Keycaps für die Tasten-Matrix** (Wird diesem Repository als STL beigefügt, sobald die finalen Designs fertig sind)
- **Magnete** für den Verschlussmechanismus.
- **Lötstation**, Lötzinn, Entlötpumpe und Multimeter.

### **Software**
- Raspberry Pi OS Lite (32-Bit).
- Python-Skripte für das Schachprogramm, das OLED-Display und die Tastatureingabe.
- Systemd-Dienste für das automatische Starten von Programmen und das Überwachen des UPS-Schalters.

---

## 💡 **Schritte zum Zusammenbau**

### **1. Hardware vorbereiten**
- **OLED-Display:** I2C-Verbindungen verlöten und testen.
- **Tastaturmatrix:** Verlöten und mit GPIO-Pins verbinden.
- **Raspberry Pi:** Headerpins entfernen (falls vorhanden) und alle Verbindungen sauber verlöten.
- **UPS-Modul:** Mit dem Pi verbinden und den Schalter für Ein/Aus konfigurieren.

### 2. Softwareanforderungen
1. **Raspberry Pi OS** (aktuellste Version)
2. **Python 3**
3. Bibliotheken:
   - `RPi.GPIO`
   - `luma.oled`
   - `Pillow`
   - `python-chess`
   - `stockfish`
4. **I2C-Tools** zur Aktivierung und Testen des I2C-Busses.
  

### Hardware und Komponentenliste
| **Komponente**                          | **Anzahl** | **Beschreibung**                                 |
|-----------------------------------------|------------|-------------------------------------------------|
| Raspberry Pi Zero 2 W                   | 1          | Mini-Computer zur Steuerung                     |
| 1.3 Zoll OLED Display (SH1106, I2C)     | 1          | Display zur Anzeige der Schachzüge              |
| 4x4 Button-Matrix                       | 1          | Eingabegerät für Schachzüge                     |
| LiPo-Akku 3.7V (1000mAh)                | 1          | Stromversorgung für den Raspberry Pi            |
| Waveshare UPS HAT für Raspberry Pi Zero | 1          | HAT-Modul zur Akkuverwaltung und Stromversorgung|
| Micro-SD-Karte (mind. 8GB)              | 1          | Speicherkarte für Raspberry Pi OS und Code      |

---


## Wiring Guide 

<img width="539" alt="Bildschirmfoto 2024-12-16 um 10 53 50" src="https://github.com/user-attachments/assets/e0960a62-ca42-4f72-8d2f-7379c8c0a741" />


### Button-Matrix Verkabelung
| **Matrix-Pin** | **Raspberry Pi GPIO (BCM)** | **Physischer Pin** | **Beschreibung** |
|-----------------|----------------------------|--------------------|------------------|
| **1**          | GPIO 25                    | Pin 22             | Zeile 1          |
| **2**          | GPIO 23                    | Pin 16             | Zeile 2          |
| **3**          | GPIO 24                    | Pin 18             | Zeile 3          |
| **4**          | GPIO 18                    | Pin 12             | Zeile 4          |
| **5**          | GPIO 27                    | Pin 13             | Spalte 1         |
| **6**          | GPIO 22                    | Pin 15             | Spalte 2         |
| **7**          | GPIO 17                    | Pin 11             | Spalte 3         |
| **8**          | GPIO 4                     | Pin 7              | Spalte 4         |

### OLED-Display (SH1106) Verkabelung
| **OLED Pin**    | **Raspberry Pi GPIO (BCM)** | **Physischer Pin** | **Beschreibung**         |
|------------------|----------------------------|--------------------|--------------------------|
| **VCC**         | 3.3V                       | Pin 1              | Spannungsversorgung      |
| **GND**         | GND                        | Pin 9              | Masse                    |
| **SDA**         | GPIO 2 (SDA)               | Pin 3              | I2C-Datenleitung         |
| **SCL**         | GPIO 3 (SCL)               | Pin 5              | I2C-Taktleitung          |

### Zusammenfassung der Pinbelegung
| **Funktion**         | **Raspberry Pi GPIO (BCM)** | **Physischer Pin** |
|-----------------------|----------------------------|--------------------|
| Button-Matrix Zeile 1 | GPIO 25                   | Pin 22             |
| Button-Matrix Zeile 2 | GPIO 23                   | Pin 16             |
| Button-Matrix Zeile 3 | GPIO 24                   | Pin 18             |
| Button-Matrix Zeile 4 | GPIO 18                   | Pin 12             |
| Button-Matrix Spalte 1| GPIO 27                   | Pin 13             |
| Button-Matrix Spalte 2| GPIO 22                   | Pin 15             |
| Button-Matrix Spalte 3| GPIO 17                   | Pin 11             |
| Button-Matrix Spalte 4| GPIO 4                    | Pin 7              |
| OLED VCC              | 3.3V                      | Pin 1              |
| OLED GND              | GND                       | Pin 9              |
| OLED SDA              | GPIO 2 (SDA)              | Pin 3              |
| OLED SCL              | GPIO 3 (SCL)              | Pin 5              |

### Hinweise für die Verkabelung
1. **Button-Matrix**: Die Reihen-Pins sind als **Eingänge** und die Spalten-Pins als **Ausgänge** konfiguriert.
2. **OLED-Display**: Verwendet das **I2C-Protokoll**; muss in der Raspberry Pi Konfiguration aktiviert entsprechend werden (`sudo raspi-config`).


### Bildergalerie

![IMG_7413](https://github.com/user-attachments/assets/995f9a41-c0e2-448c-8c33-d4b459cbea2a)

---


