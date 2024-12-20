import random
import RPi.GPIO as GPIO
import time
import chess
import chess.engine
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import ImageDraw, ImageFont, Image


# GPIO-Setup für Buttons
class ButtonMatrix:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.buttonIDs = [[4, 3, 2, 1], [8, 7, 6, 5], [16, 15, 14, 13], [12, 11, 10, 9]]
        self.rowPins = [18, 23, 24, 25]
        self.columnPins = [21, 22, 17, 4]
        for row in self.rowPins:
            GPIO.setup(row, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for col in self.columnPins:
            GPIO.setup(col, GPIO.OUT)
            GPIO.output(col, GPIO.HIGH)

    def readButton(self):
        for j, colPin in enumerate(self.columnPins):
            GPIO.output(colPin, GPIO.LOW)  # Aktiviere Spalte
            for i, rowPin in enumerate(self.rowPins):
                if GPIO.input(rowPin) == GPIO.LOW:  # Wenn Zeile aktiviert wird
                    GPIO.output(colPin, GPIO.HIGH)  # Spalte deaktivieren
                    time.sleep(0.2)  # Debounce
                    return i, j  # Rückgabe von Zeile und Spalte
            GPIO.output(colPin, GPIO.HIGH)  # Spalte deaktivieren
        return None


# OLED-Setup
class OLED:
    def __init__(self):
        serial = i2c(port=1, address=0x3C)
        self.device = sh1106(serial)
        self.font = ImageFont.load_default()

    def display_text(self, text):
        with Image.new("1", (self.device.width, self.device.height)) as image:
            draw = ImageDraw.Draw(image)
            draw.text((0, 0), text, font=self.font, fill=255)
            self.device.display(image)

    def clear(self):
        self.device.clear()

    def display_logo(self):
        logo_image = Image.new("1", (128, 64))
        logo_pixels = logo_image.load()

        # Logo-Daten
        logo_data = [
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xe0, 0x00, 0x00, 0x1e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xe0, 0x00, 0x00, 0x1e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x1e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf0, 0x01, 0x80, 0x1e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf0, 0x03, 0x80, 0x1e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf0, 0x03, 0xc0, 0x1e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf0, 0x03, 0xc0, 0x1e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf0, 0x03, 0xc0, 0x1e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0xf0, 0x03, 0xc0, 0x1e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0xf8, 0x07, 0xe0, 0x3f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfc, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x07, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xc0, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x1f, 0xf8, 0x00, 0x00, 0x00, 0x1f, 0xff, 0xe0, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x3f, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x3e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x3e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x3e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x1f, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x1f, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x3f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xf8, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xe0, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0xfc, 0x0f, 0xfe, 0x00, 0x01, 0xff, 0xff, 0xfc, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0xf0, 0x07, 0xfe, 0x00, 0x00, 0x7f, 0x00, 0x7f, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x01, 0xe0, 0x03, 0xff, 0x80, 0x00, 0x7e, 0x00, 0x1f, 0x80, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x01, 0xe0, 0x03, 0xe7, 0xe0, 0x00, 0x3e, 0x00, 0x07, 0xc0, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x01, 0xe0, 0x03, 0xc1, 0xfc, 0x00, 0x3e, 0x00, 0x03, 0xc0, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x01, 0xe0, 0x03, 0x80, 0x7f, 0x00, 0x3e, 0x00, 0x07, 0x80, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x01, 0xf0, 0x03, 0x80, 0x1f, 0xe0, 0x3e, 0x00, 0x0f, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x01, 0xf8, 0x07, 0x80, 0x03, 0xff, 0x7e, 0x00, 0x3e, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0xfc, 0x0f, 0xc0, 0x00, 0xff, 0xff, 0x00, 0xf8, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x7f, 0xff, 0xe0, 0x00, 0x1f, 0xff, 0xff, 0xe0, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x1f, 0xff, 0xff, 0xe0, 0x1f, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x01, 0xff, 0xff, 0xff, 0xff, 0xff, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0xff, 0xff, 0xff, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7f, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x38, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        ]

        # Logo-Daten rendern
        for y in range(64):
            for x in range(128):
                byte_index = (y * 128 + x) // 8
                bit_index = 7 - (x % 8)
                if logo_data[byte_index] & (1 << bit_index):
                    logo_pixels[x, y] = 1

        self.device.display(logo_image)



# Schachcomputer-Logik und Interaktion
class ChessComputer:
    def __init__(self):
        self.matrix = ButtonMatrix()
        self.oled = OLED()
        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish", timeout=10)

        # Konfiguration des Stockfish-Skill-Levels
        self.engine.configure({
            "Skill Level": 20,  # Maximales Level
            "Threads": 4        # Multi-Threading für schnellere Berechnungen
        })

        self.current_move = ""
        self.phase = 0
        self.log = []  # Für Anzeige der letzten Züge
        self.computer_turn = None
        self.start_game()

    def start_game(self):
        self.display_startup_animation()
        self.display_start_prompt()
        self.determine_starting_player()

    def display_startup_animation(self):
        self.oled.display_logo()
        time.sleep(2)  # Zeige das Logo 3 Sekunden lang an
        self.oled.clear()

    def display_start_prompt(self):
        self.oled.display_text("Press any key\nto start")
        while not self.matrix.readButton():
            time.sleep(0.1)
        self.oled.clear()

    def determine_starting_player(self):
        self.computer_turn = random.choice([True, False])
        if self.computer_turn:
            self.oled.display_text("Computer starts.")
            time.sleep(2)
            self.computer_move()
        else:
            self.oled.display_text("Player starts.\nenter first move:")
            time.sleep(2)

    def display_game_status(self, current_message=None):
        # Füge aktuelle Nachricht hinzu, falls vorhanden
        if current_message:
            if not self.log or self.log[-1] != current_message:  # Verhindere doppelte Logs
                self.log.append(current_message)

        # Baue die Anzeige auf
        text = "\n".join(self.log[-3:])  # Zeige die letzten 3 Züge
        if self.computer_turn:
            text += "\nComputer thinks..."
        elif self.current_move:
            text += f"\nInput move: {self.current_move}"
        else:
            text += "\nInput move:"

        self.oled.display_text(text)


    def handle_input(self):
        if self.computer_turn:
            return  # Spieler kann keine Eingaben machen, wenn der Computer zieht

        button = self.matrix.readButton()
        if button:
            row, col = button
            button_id = self.matrix.buttonIDs[row][col]
            self.process_input(button_id)

    def process_input(self, button_id):
        # Sondertasten
        if button_id == 13:  # Aufgeben
            self.oled.display_text("Confirm surrender?")
            while True:
                button = self.matrix.readButton()
                if button:
                    row, col = button
                    confirm_id = self.matrix.buttonIDs[row][col]
                    if confirm_id == 16:  # GO-Taste
                        self.oled.display_text("Game over.\nPlayer surrendered.")
                        self.end_game()
                        return
                    else:
                        self.oled.display_text("Cancelled.")
                        time.sleep(1)
                        self.display_game_status()
                        return

        elif button_id == 14:  # Clear
            self.current_move = ""
            self.phase = 0
            self.display_game_status()
            return

        elif button_id == 15:  # Del
            if self.current_move:
                # Entferne das letzte Zeichen
                self.current_move = self.current_move[:-1]
                # Setze die Phase entsprechend der verbleibenden Eingabe zurück
                if len(self.current_move) == 0:
                    self.phase = 0  # Kein Zeichen: Zurück zur Spalteneingabe
                elif len(self.current_move) == 1:
                    self.phase = 1  # Ein Zeichen: In der Zeileneingabe des Startfelds
                elif len(self.current_move) == 2:
                    self.phase = 2  # Zwei Zeichen: Spalteneingabe des Zielfelds
                elif len(self.current_move) == 3:
                    self.phase = 3  # Drei Zeichen: Zeileneingabe des Zielfelds
                self.display_game_status()  # Zeige aktualisierte Eingabe an
            else:
                self.oled.display_text("Nothing to delete.")
                time.sleep(1)
            return

        elif button_id == 16:  # GO
            if len(self.current_move) == 4:  # Normale Züge
                if self.check_promotion():
                    self.oled.display_text("Choose piece to\nconvert to.")
                    return  # Warte auf Umwandlungseingabe
                if self.make_move(self.current_move):
                    self.current_move = ""  # Zug zurücksetzen
                    self.phase = 0
                    self.computer_turn = True
                    self.display_game_status()
                else:
                    self.oled.display_text("Invalid move.")
                    time.sleep(1)
                    self.current_move = ""
                    self.phase = 0
                    self.display_game_status()  # Aktualisiere den Status nach Fehler
            elif len(self.current_move) == 5:  # Umwandlungszüge (mit Figur)
                if self.make_move(self.current_move):
                    self.current_move = ""  # Zug zurücksetzen
                    self.phase = 0
                    self.computer_turn = True
                    self.display_game_status()
                else:
                    self.oled.display_text("Invalid move.")
                    time.sleep(1)
                    self.current_move = ""
                    self.phase = 0
                    self.display_game_status()  # Aktualisiere den Status nach Fehler
            else:
                self.oled.display_text("Move not complete.")
                time.sleep(1)
                self.display_game_status()  # Aktualisiere den Status nach Fehler
            return



        # Umwandlungstasten
        elif button_id in [9, 10, 11, 12]:  # Umwandlung (Dame, Turm, Läufer, Springer)
            promotion_pieces = {9: "q", 10: "r", 11: "b", 12: "n"}
            if self.phase == 3 and self.current_move:
                self.current_move += promotion_pieces[button_id]
                self.display_game_status(f"Selected: {promotion_pieces[button_id]}")
            else:
                self.oled.display_text("No conversion\npossible.")
                time.sleep(1)
            return

        # Normale Eingabe
        if self.phase == 0:  # Startfeld Spalte (a-h)
            if 1 <= button_id <= 8:
                self.current_move = chr(96 + button_id)
                self.phase = 1
                self.display_game_status()
            else:
                self.oled.display_text("Invalid move.\nFrom-Column.")
                time.sleep(1)
                self.display_game_status()
        elif self.phase == 1:  # Startfeld Zeile (1-8)
            if 1 <= button_id <= 8:
                self.current_move += str(button_id)
                self.phase = 2
                self.display_game_status()
            else:
                self.oled.display_text("Invalid move.\nFrom-Row.")
                time.sleep(1)
                self.display_game_status()
        elif self.phase == 2:  # Zielfeld Spalte (a-h)
            if 1 <= button_id <= 8:
                self.current_move += chr(96 + button_id)
                self.phase = 3
                self.display_game_status()
            else:
                self.oled.display_text("Invalid move.\nTo-Column.")
                time.sleep(1)
                self.display_game_status()
        elif self.phase == 3:  # Zielfeld Zeile (1-8)
            if 1 <= button_id <= 8:
                self.current_move += str(button_id)
                self.display_game_status()
            else:
                self.oled.display_text("Invalid move.\nTo-Row.")
                time.sleep(1)
                self.display_game_status()

    def check_promotion(self):
        try:
            # Überprüfe, ob der aktuelle Zug gültig ist
            if not self.current_move or len(self.current_move) < 4:
                return False

            last_move = chess.Move.from_uci(self.current_move.lower())
            piece = self.board.piece_at(last_move.from_square)
            
            # Prüfen, ob ein Bauer auf dem Feld ist und ob er auf eine Umwandlungsreihe zieht
            if piece and piece.symbol().lower() == "p" and chess.square_rank(last_move.to_square) in [0, 7]:
                return True

            return False
        except Exception as e:
            print(f"Fehler in check_promotion: {e}")
            return False


    def make_move(self, move):
        try:
            chess_move = chess.Move.from_uci(move.lower())
            if chess_move in self.board.legal_moves:
                self.board.push(chess_move)  # Spielerzug ausführen
                self.log.append(f"Player: {move}")  # Zug protokollieren
                self.current_move = ""  # Eingabe zurücksetzen
                self.phase = 0  # Phase zurücksetzen
                if not self.board.is_game_over():
                    self.computer_move()  # Computerzug ausführen
                return True
        except ValueError:
            pass
        return False

    def computer_move(self):
        try:
            if not self.computer_turn:  # Verhindere Doppelzug
                return

            result = self.engine.play(self.board, chess.engine.Limit(time=2))
            self.board.push(result.move)
            
            # Log und Anzeige aktualisieren
            move_text = f"Computer: {result.move.uci()}"
            if self.log and self.log[-1] != move_text:  # Verhindere doppelte Logs
                self.log.append(move_text)
            self.display_game_status(move_text)
        except Exception as e:
            print(f"Fehler beim Computerzug: {e}")
            self.oled.display_text("Error with\n Computer move!")
            time.sleep(2)
        finally:
            self.computer_turn = False  # Übergibt die Kontrolle an den Spieler
            self.display_game_status()  # Aktualisiere das Display für den Spieler




    def end_game(self):
        self.oled.display_text("Game over.\nWanna go\nagain?")
        
        while True:
            button = self.matrix.readButton()
            if button:
                row, col = button
                button_id = self.matrix.buttonIDs[row][col]
                if button_id == 16:  # GO-Taste
                    # Schachbrett und Status zurücksetzen
                    self.board.reset()
                    self.phase = 0
                    self.current_move = ""
                    self.computer_turn = None
                    self.log = []  # Spiel-Log zurücksetzen
                    self.display_start_prompt()  # Prompt für neues Spiel anzeigen
                    self.determine_starting_player()  # Wer startet, erneut bestimmen
                    return  # Kehre zur Hauptspiel-Schleife zurück
                else:
                    self.oled.display_text("Confirm\nto start over.")
                    time.sleep(1)


    def run(self):
        while not self.board.is_game_over():
            if self.computer_turn:
                self.computer_move()
            else:
                self.handle_input()
            time.sleep(0.1)  # CPU-Last reduzieren

        self.end_game()


if __name__ == "__main__":
    chess_computer = ChessComputer()
    chess_computer.run()
