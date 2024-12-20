import chess
import chess.engine
import time
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import ImageDraw, ImageFont, Image


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


class TestChessLogicWithStockfish:
    def __init__(self, stockfish_path):
        self.board = chess.Board()
        self.engine_test = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        self.engine_chess_computer = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        self.move_count = 0
        self.oled = OLED()
        self.log = []  # Log der letzten Züge für die OLED-Anzeige

    def display_game_status(self, current_message=None):
        # Füge aktuelle Nachricht hinzu, falls vorhanden
        if current_message:
            if not self.log or self.log[-1] != current_message:  # Verhindere doppelte Logs
                self.log.append(current_message)

        # Baue die Anzeige auf
        text = "\n".join(self.log[-3:])  # Zeige die letzten 3 Züge
        if self.board.turn:
            text += "\nDein Zug:"
        else:
            text += "\nWarten auf Computer..."

        self.oled.display_text(text)

    def simulate_game(self, max_moves=200, delay=2):
        self.oled.display_text("Simulation startet...")
        time.sleep(2)

        while not self.board.is_game_over() and self.move_count < max_moves:
            self.oled.clear()
            print(f"\n--- Zug {self.move_count + 1} ---")
            print(self.board)

            # Entscheide, wer zieht
            if self.board.turn:
                # Weiß zieht (Test-Computer, als "Spieler")
                result = self.engine_test.play(self.board, chess.engine.Limit(time=1))
                move = result.move
                player = "Spieler (Weiß)"
            else:
                # Schwarz zieht (Schachcomputer, als "Computer")
                result = self.engine_chess_computer.play(self.board, chess.engine.Limit(time=1))
                move = result.move
                player = "Computer (Schwarz)"

            # Ausgabe des Zugs
            print(f"{player} zieht: {move}")
            if self.is_promotion(move):
                print(f"Umwandlung erfolgreich: {move}")

            # Aktualisiere OLED
            if player.startswith("Spieler"):
                log_message = f"Spieler: {move}"
            else:
                log_message = f"Computer: {move}"
            self.display_game_status(log_message)

            # Zug ausführen
            self.board.push(move)
            self.move_count += 1
            time.sleep(delay)

        self.oled.clear()
        self.oled.display_text("Spiel beendet!")

        print("\n=== Spiel beendet ===")
        if self.board.is_checkmate():
            print("Schachmatt! Gewinner:", "Weiß" if self.board.turn else "Schwarz")
        elif self.board.is_stalemate():
            print("Patt! Keine weiteren Züge möglich.")
        elif self.board.is_insufficient_material():
            print("Unentschieden wegen unzureichendem Material.")
        else:
            print("Maximale Züge erreicht.")

        print("\nEndstand des Schachbretts:")
        print(self.board)

    def is_promotion(self, move):
        piece = self.board.piece_at(move.from_square)
        if piece and piece.piece_type == chess.PAWN and chess.square_rank(move.to_square) in [0, 7]:
            return True
        return False

    def run(self):
        try:
            self.simulate_game(max_moves=200, delay=1)
        except Exception as e:
            print(f"Fehler während der Simulation: {e}")
        finally:
            self.engine_test.quit()
            self.engine_chess_computer.quit()


if __name__ == "__main__":
    stockfish_path = "/usr/games/stockfish"
    test_chess_logic = TestChessLogicWithStockfish(stockfish_path)
    test_chess_logic.run()
