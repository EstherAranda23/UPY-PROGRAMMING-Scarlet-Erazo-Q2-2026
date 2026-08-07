import tkinter as tk
import random
import os
import sys
import threading
import time

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 400

WHITE = "#FFFFFF"
BLACK = "#000000"
DARK_GRAY = "#14141E"
TILE_COLOR = "#3C5078"
LINE_COLOR = "#788CB4"
MENU_BG = "#000000"
BUTTON_COLOR = "#FF5050"
SHIP_FALLBACK_COLOR = "#FFD700"


class AudioManager:
    """Sistema de audio que intenta varios backends."""
    def __init__(self):
        self.backend = None
        self.sounds = {}
        self._loops = {}
        self._lock = threading.Lock()

        # 1. Intentar playsound (puro Python, funciona en cualquier version)
        try:
            from playsound import playsound
            self.backend = "playsound"
            self._playsound = playsound
            print("[Audio] Backend: playsound (MP3 soportado)")
            return
        except Exception as e:
            print("[Audio] playsound no disponible:", str(e))

        # 2. Intentar pygame.mixer
        try:
            import pygame
            if not pygame.get_init():
                pygame.init()
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.backend = "pygame"
            self.pygame = pygame
            print("[Audio] Backend: pygame.mixer")
            return
        except Exception as e:
            print("[Audio] pygame.mixer no disponible:", str(e))

        # 3. Intentar winsound (Windows solo, solo WAV)
        if sys.platform == "win32":
            try:
                import winsound
                self.backend = "winsound"
                self.winsound = winsound
                print("[Audio] Backend: winsound (solo WAV)")
                return
            except Exception as e:
                print("[Audio] winsound no disponible:", str(e))

        print("[Audio] === SIN AUDIO ===")
        print("[Audio] Para activar el audio instala:")
        print("[Audio]    pip install playsound==1.2.2")
        print("[Audio] O para mejor calidad:")
        print("[Audio]    pip install pygame")

    def load(self, name, path):
        if not os.path.exists(path):
            print("[Audio] Archivo no encontrado:", path)
            return
        self.sounds[name] = path
        print("[Audio] Cargado:", name, "->", path)

    def _loop_playsound(self, name, path):
        """Hilo que reproduce en loop usando playsound."""
        while self._loops.get(name, False):
            try:
                self._playsound(path, block=True)
            except Exception as e:
                print("[Audio] Error en loop:", e)
                break

    def play(self, name, loop=False, volume=1.0):
        if name not in self.sounds:
            print("[Audio] Sonido no cargado:", name)
            return

        path = self.sounds[name]

        if self.backend == "playsound":
            try:
                if loop:
                    # Detener loop anterior si existe
                    self._loops[name] = False
                    time.sleep(0.1)
                    self._loops[name] = True
                    t = threading.Thread(target=self._loop_playsound, args=(name, path), daemon=True)
                    t.start()
                    print("[Audio] Reproduciendo en loop:", name)
                else:
                    t = threading.Thread(target=self._playsound, args=(path, False), daemon=True)
                    t.start()
                    print("[Audio] Reproduciendo:", name)
            except Exception as e:
                print("[Audio] Error playsound:", e)

        elif self.backend == "pygame":
            try:
                snd = self.pygame.mixer.Sound(path)
                snd.set_volume(volume)
                if loop:
                    snd.play(-1)
                else:
                    snd.play()
                print("[Audio] Reproduciendo:", name)
            except Exception as e:
                print("[Audio] Error pygame:", e)

        elif self.backend == "winsound":
            try:
                flags = self.winsound.SND_FILENAME | self.winsound.SND_ASYNC
                if loop:
                    flags |= self.winsound.SND_LOOP
                self.winsound.PlaySound(path, flags)
                print("[Audio] Reproduciendo:", name)
            except Exception as e:
                print("[Audio] Error winsound (probablemente no es WAV):", e)

    def stop_all(self):
        print("[Audio] Deteniendo todo...")
        # Detener loops
        for name in list(self._loops.keys()):
            self._loops[name] = False

        if self.backend == "playsound":
            # playsound no tiene stop, los threads terminan solos
            pass
        elif self.backend == "pygame":
            try:
                self.pygame.mixer.stop()
            except:
                pass
        elif self.backend == "winsound":
            try:
                self.winsound.PlaySound(None, self.winsound.SND_PURGE)
            except:
                pass


class GalaxyGame:
    def transform(self, x, y):
        tx, ty = self.transform_perspective(x, y)
        return tx, self.height - ty

    def transform_2D(self, x, y):
        return int(x), int(self.height - y)

    def transform_perspective(self, x, y):
        lin_y = y * self.perspective_point_y / self.height
        if lin_y > self.perspective_point_y:
            lin_y = self.perspective_point_y
        diff_x = x - self.perspective_point_x
        diff_y = self.perspective_point_y - lin_y
        factor_y = diff_y / self.perspective_point_y
        factor_y = pow(factor_y, 3)
        tr_x = self.perspective_point_x + diff_x * factor_y
        tr_y = self.perspective_point_y - factor_y * self.perspective_point_y
        return int(tr_x), int(tr_y)

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("O N E   P I E C E")
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg=DARK_GRAY)

        self.canvas = tk.Canvas(self.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT,
                                bg=DARK_GRAY, highlightthickness=0)
        self.canvas.pack()

        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

        self.perspective_point_x = self.width / 2
        self.perspective_point_y = self.height * 0.75

        self.V_NB_LINES = 8
        self.V_LINES_SPACING = 0.4
        self.H_NB_LINES = 8
        self.H_LINES_SPACING = 0.15

        self.SPEED = 0.95
        self.current_offset_y = 0
        self.current_y_loop = 0
        self.SPEED_X = 4.2
        self.current_speed_x = 0
        self.current_offset_x = 0

        self.NB_TILES = 16
        self.tiles_coordinates = []

        self.SHIP_WIDTH = 0.1
        self.SHIP_HEIGHT = 0.035
        self.SHIP_BASE_Y = 0.04
        self.ship_coordinates = [(0, 0), (0, 0), (0, 0), (0, 0)]

        self.state_game_over = False
        self.state_game_has_started = False

        self.menu_title = "O  N  E    P  I  E  C  E"
        self.menu_button_title = "START"
        self.score_txt = "SCORE: 0"

        self.audio = AudioManager()
        self.init_audio()

        self.ship_image_original = None
        self._current_ship_img = None
        self.init_ship_image()

        self.root.bind("<KeyPress>", self.on_key_down)
        self.root.bind("<KeyRelease>", self.on_key_up)
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.bind("<Motion>", self.on_mouse_move)

        self.reset_game()
        self.audio.play("galaxy", loop=True, volume=0.8)

        self.running = True
        self.last_time = time.time()
        self.game_loop()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def init_audio(self):
        self.audio.load("begin", "audio/begin.mp3")
        self.audio.load("galaxy", "audio/music1.mp3")
        self.audio.load("gameover_impact", "audio/gameover_impact.mp3")
        self.audio.load("gameover_voice", "audio/gameover_voice.mp3")
        self.audio.load("music1", "audio/music1.mp3")
        self.audio.load("restart", "audio/restart.mp3")

    def init_ship_image(self):
        ship_path = "imagenes/1.jpg"
        if not os.path.exists(ship_path):
            print("[Imagen] No encontrada:", ship_path)
            print("[Imagen] Instala Pillow para ver la imagen: pip install pillow")
            return
        try:
            from PIL import Image
            self.ship_image_original = Image.open(ship_path)
            print("[Imagen] 1 cargado")
        except ImportError:
            print("[Imagen] Pillow no instalado. Ejecuta: pip install pillow")
        except Exception as e:
            print("[Imagen] Error:", str(e))

    def get_ship_image_for_size(self, w, h):
        if self.ship_image_original is None or w <= 0 or h <= 0:
            return None
        try:
            from PIL import Image, ImageTk
            orig_w, orig_h = self.ship_image_original.size
            ratio = min(w / orig_w, h / orig_h)
            new_w = max(1, int(orig_w * ratio))
            new_h = max(1, int(orig_h * ratio))
            resized = self.ship_image_original.resize((new_w, new_h), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(resized)
        except:
            return None

    def reset_game(self):
        self.current_offset_y = 0
        self.current_y_loop = 0
        self.current_speed_x = 0
        self.current_offset_x = 0
        self.tiles_coordinates = []
        self.score_txt = "SCORE: " + str(self.current_y_loop)
        self.pre_fill_tiles_coordinates()
        self.generate_tiles_coordinates()
        self.state_game_over = False

    def pre_fill_tiles_coordinates(self):
        for i in range(0, 10):
            self.tiles_coordinates.append((0, i))

    def generate_tiles_coordinates(self):
        last_x = 0
        last_y = 0
        for i in range(len(self.tiles_coordinates) - 1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]
        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_x = last_coordinates[0]
            last_y = last_coordinates[1] + 1
        for i in range(len(self.tiles_coordinates), self.NB_TILES):
            r = random.randint(0, 2)
            start_index = -int(self.V_NB_LINES / 2) + 1
            end_index = start_index + self.V_NB_LINES - 1
            if last_x <= start_index:
                r = 1
            if last_x >= end_index:
                r = 2
            self.tiles_coordinates.append((last_x, last_y))
            if r == 1:
                last_x += 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            elif r == 2:
                last_x += -1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            last_y += 1

    def get_line_x_from_index(self, index):
        central_line_x = self.perspective_point_x
        spacing = self.V_LINES_SPACING * self.width
        offset = index - 0.5
        line_x = central_line_x + offset * spacing + self.current_offset_x
        return line_x

    def get_line_y_from_index(self, index):
        spacing_y = self.H_LINES_SPACING * self.height
        line_y = index * spacing_y - self.current_offset_y
        return line_y

    def get_tile_coordinates(self, ti_x, ti_y):
        ti_y = ti_y - self.current_y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y

    def update_ship(self):
        center_x = self.width / 2
        base_y = self.SHIP_BASE_Y * self.height
        half_width = self.SHIP_WIDTH * self.width / 2
        ship_height = self.SHIP_HEIGHT * self.height
        self.ship_coordinates[0] = (center_x - half_width, base_y)
        self.ship_coordinates[1] = (center_x - half_width, base_y + ship_height)
        self.ship_coordinates[2] = (center_x + half_width, base_y + ship_height)
        self.ship_coordinates[3] = (center_x + half_width, base_y)

    def get_transformed_ship_points(self):
        points = []
        for coord in self.ship_coordinates:
            tx, ty = self.transform(*coord)
            points.append(tx)
            points.append(ty)
        return points

    def check_ship_collisions(self):
        for i in range(0, len(self.tiles_coordinates)):
            ti_x, ti_y = self.tiles_coordinates[i]
            if ti_y > self.current_y_loop + 1:
                return False
            if self.check_ship_collision_with_tile(ti_x, ti_y):
                return True
        return False

    def check_ship_collision_with_tile(self, ti_x, ti_y):
        xmin, ymin = self.get_tile_coordinates(ti_x, ti_y)
        xmax, ymax = self.get_tile_coordinates(ti_x + 1, ti_y + 1)
        for i in range(0, 4):
            px, py = self.ship_coordinates[i]
            if xmin <= px <= xmax and ymin <= py <= ymax:
                return True
        return False

    def on_key_down(self, event):
        if event.keysym == "Left":
            self.current_speed_x = self.SPEED_X
        elif event.keysym == "Right":
            self.current_speed_x = -self.SPEED_X
        elif event.keysym == "space":
            if not self.state_game_has_started or self.state_game_over:
                self.on_menu_button_pressed()

    def on_key_up(self, event):
        if event.keysym in ("Left", "Right"):
            self.current_speed_x = 0

    def on_mouse_down(self, event):
        x, y = event.x, event.y
        if not self.state_game_has_started or self.state_game_over:
            if self.is_inside_button(x, y):
                self.on_menu_button_pressed()
        else:
            if x < self.width / 2:
                self.current_speed_x = self.SPEED_X
            else:
                self.current_speed_x = -self.SPEED_X

    def on_mouse_up(self, event):
        self.current_speed_x = 0

    def on_mouse_move(self, event):
        if not self.state_game_has_started or self.state_game_over:
            if self.is_inside_button(event.x, event.y):
                self.canvas.config(cursor="hand2")
            else:
                self.canvas.config(cursor="")

    def is_inside_button(self, x, y):
        bx1 = self.width // 2 - 90
        by1 = int(self.height * 0.65) - 25
        bx2 = self.width // 2 + 90
        by2 = int(self.height * 0.65) + 25
        return bx1 <= x <= bx2 and by1 <= y <= by2

    def game_loop(self):
        if not self.running:
            return
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        if dt > 0.1:
            dt = 0.016
        self.update(dt)
        self.draw()
        self.root.after(16, self.game_loop)

    def update(self, dt):
        time_factor = dt * 60
        self.update_ship()
        if not self.state_game_over and self.state_game_has_started:
            speed_y = self.SPEED * self.height / 100
            self.current_offset_y += speed_y * time_factor
            spacing_y = self.H_LINES_SPACING * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                self.score_txt = "SCORE: " + str(self.current_y_loop)
                self.generate_tiles_coordinates()
            speed_x = self.current_speed_x * self.width / 100
            self.current_offset_x += speed_x * time_factor
        if not self.check_ship_collisions() and not self.state_game_over and self.state_game_has_started:
            self.state_game_over = True
            self.menu_title = "G  A  M  E    O  V  E  R"
            self.menu_button_title = "RESTART"
            self.audio.stop_all()
            self.audio.play("gameover_impact", volume=1.0)
            self.root.after(3000, lambda: self.audio.play("gameover_voice", volume=1.0))
            print("GAME OVER")

    def on_menu_button_pressed(self):
        if self.state_game_over:
            self.audio.play("restart", volume=1.0)
        else:
            self.audio.play("begin", volume=1.0)
        self.audio.stop_all()
        self.audio.play("music1", loop=True, volume=0.8)
        self.reset_game()
        self.state_game_has_started = True

    def draw(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill=DARK_GRAY, outline="")

        for i in range(0, min(self.NB_TILES, len(self.tiles_coordinates))):
            tile_coordinates = self.tiles_coordinates[i]
            xmin, ymin = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])
            xmax, ymax = self.get_tile_coordinates(tile_coordinates[0] + 1, tile_coordinates[1] + 1)
            x1, y1 = self.transform(xmin, ymin)
            x2, y2 = self.transform(xmin, ymax)
            x3, y3 = self.transform(xmax, ymax)
            x4, y4 = self.transform(xmax, ymin)
            points = [x1, y1, x2, y2, x3, y3, x4, y4]
            self.canvas.create_polygon(points, fill=TILE_COLOR, outline=LINE_COLOR, width=1)

        start_index = -int(self.V_NB_LINES / 2) + 1
        for i in range(start_index, start_index + self.V_NB_LINES):
            line_x = self.get_line_x_from_index(i)
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.canvas.create_line(x1, y1, x2, y2, fill=LINE_COLOR, width=1)

        end_index = start_index + self.V_NB_LINES - 1
        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)
        for i in range(0, self.H_NB_LINES):
            line_y = self.get_line_y_from_index(i)
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.canvas.create_line(x1, y1, x2, y2, fill=LINE_COLOR, width=1)

        ship_points = self.get_transformed_ship_points()
        xs = ship_points[0::2]
        ys = ship_points[1::2]
        min_x = min(xs)
        max_x = max(xs)
        min_y = min(ys)
        max_y = max(ys)
        ship_w = max(1, max_x - min_x)
        ship_h = max(1, max_y - min_y)

        if self.ship_image_original:
            ship_img = self.get_ship_image_for_size(ship_w + 20, ship_h + 20)
            if ship_img:
                self._current_ship_img = ship_img
                cx = (min_x + max_x) / 2
                cy = (min_y + max_y) / 2
                self.canvas.create_image(cx, cy, image=ship_img, anchor=tk.CENTER)
            else:
                self.canvas.create_polygon(ship_points, fill=SHIP_FALLBACK_COLOR, outline=WHITE, width=2)
        else:
            self.canvas.create_polygon(ship_points, fill=SHIP_FALLBACK_COLOR, outline=WHITE, width=2)

        self.canvas.create_text(20, 20, text=self.score_txt, fill=WHITE,
                                font=("Arial", 16, "bold"), anchor=tk.NW)

        if not self.state_game_has_started or self.state_game_over:
            self.draw_menu()

    def draw_menu(self):
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill=MENU_BG, stipple="gray50")
        self.canvas.create_text(self.width // 2, int(self.height * 0.4),
                                text=self.menu_title, fill=WHITE,
                                font=("Arial", 36, "bold"))
        bx = self.width // 2
        by = int(self.height * 0.65)
        self.canvas.create_rectangle(bx - 90, by - 25, bx + 90, by + 25,
                                     fill=BUTTON_COLOR, outline=WHITE, width=2)
        self.canvas.create_text(bx, by, text=self.menu_button_title, fill=WHITE,
                                font=("Arial", 18, "bold"))

    def on_close(self):
        self.running = False
        self.audio.stop_all()
        self.root.destroy()


if __name__ == "__main__":
    game = GalaxyGame()