from kivy.config import Config
from kivy.core.audio import SoundLoader


Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '500')
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy import platform
from kivy.app import App
from kivy.properties import NumericProperty, Clock, ObjectProperty, StringProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Quad, Triangle
import random

Builder.load_file('menu.kv')

class MainWidget(RelativeLayout):
    from transforms import transform, transform_2D, transform_perspective
    from user_actions import on_keyboard_up, on_keyboard_down, on_touch_down, on_touch_up, keyboard_closed
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    menu_widget = ObjectProperty()
    vertical_lines = []
    number_of_vertical_lines = 8
    vertical_lines_spacing = 0.2

    horizontal_lines = []
    number_of_horizontal_lines = 10
    horizontal_lines_spacing = 0.1

    current_offset_y = 0
    speed = 0.8

    current_offset_x = 0
    speed_x = 1

    current_speed_x = 0

    number_of_tiles = 12
    tiles = []
    tiles_coordinates = []

    current_loop_y = 0

    ship_width = 0.1
    ship_height = 0.035
    ship_base_y = 0.04
    ship = None
    ship_coordinates = [(0, 0), (0, 0), (0, 0)]

    state_game_over = False
    state_game_has_started = False

    menu_title = StringProperty("G   A   L   A   X   Y")
    menu_button_title = StringProperty("START")

    score = StringProperty('')
    new_score = ''
    final_score = StringProperty('')

    is_paused = False
    new_current_offset_y = 0
    sound_begin = None
    sound_galaxy = None
    sound_gameover_impact = None
    sound_gameover_voice = None
    sound_music1 = None
    sound_restart = None

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_audio()
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.init_ship()
        self.reset_game()
        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def init_audio(self):
        self.sound_begin = SoundLoader.load('audio/begin.wav')
        self.sound_galaxy = SoundLoader.load('audio/galaxy.wav')
        self.sound_gameover_impact = SoundLoader.load('audio/gameover_impact.wav')
        self.sound_gameover_voice = SoundLoader.load('audio/gameover_voice.wav')
        self.sound_music1 = SoundLoader.load('audio/music1.wav')
        self.sound_restart = SoundLoader.load('audio/restart.wav')

        self.sound_begin.volume = 1
        self.sound_galaxy.volume = 1
        self.sound_gameover_impact.volume = 1
        self.sound_gameover_voice.volume = 1
        self.sound_music1.volume = 1
        self.sound_restart.volume = 1

    def reset_game(self):
        self.current_offset_y = 0
        self.current_offset_x = 0
        self.current_speed_x = 0
        self.current_loop_y = 0
        self.speed = 0
        self.speed_x = 0
        self.score = ''
        self.tiles_coordinates = []

        self.pre_fill_tiles_coordinates()
        self.generate_tile_coordinates()

        self.state_game_over = False

    def is_desktop(self):
        if platform == 'win':
            return True
        return False

    def init_ship(self):
        with self.canvas:
            Color(0, 0, 0)
            self.ship = Triangle()

    def update_ship(self):
        center_x = self.width / 2
        base_y = self.ship_base_y * self.height
        ship_half_width = self.ship_width * self.width / 2
        point1_x = center_x - ship_half_width
        point1_y = base_y
        point2_x = center_x
        point2_y = base_y + self.ship_height * self.height
        point3_x = center_x + ship_half_width
        point3_y = base_y

        self.ship_coordinates[0] = (point1_x, point1_y)
        self.ship_coordinates[1] = (point2_x, point2_y)
        self.ship_coordinates[2] = (point3_x, point3_y)
        x1, y1 = self.transform(*self.ship_coordinates[0])
        x2, y2 = self.transform(*self.ship_coordinates[1])
        x3, y3 = self.transform(*self.ship_coordinates[2])

        self.ship.points = [x1, y1, x2, y2, x3, y3]

    def check_ship_collision(self):
        for i in range(0, len(self.tiles_coordinates)):
            ti_x, ti_y = self.tiles_coordinates[i]
            if ti_x > self.current_loop_y + 1:
                return False
            if self.check_ship_collision_with_tile(ti_x, ti_y):
                return True
        return False

    def check_ship_collision_with_tile(self, ti_x, ti_y):
        xmin, ymin = self.get_tile_coordinates(ti_x, ti_y)
        xmax, ymax = self.get_tile_coordinates(ti_x + 1, ti_y + 1)
        for i in range(0, 3):
            px, py = self.ship_coordinates[i]
            if xmin <= px <= xmax and ymin <= py <= ymax:
                return True
        return False

    def init_tiles(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.number_of_tiles):
                self.tiles.append(Quad())

    def pre_fill_tiles_coordinates(self):
        for i in range(0, 10):
            self.tiles_coordinates.append((0, i))

    def generate_tile_coordinates(self):
        last_x = 0
        last_y = 0
        for i in range(len(self.tiles_coordinates) - 1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_loop_y:
                del self.tiles_coordinates[i]

        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_x = last_coordinates[0]
            last_y = last_coordinates[1] + 1

        for i in range(len(self.tiles_coordinates), self.number_of_tiles):
            r = random.randint(0, 2)
            start_index = -int(self.number_of_vertical_lines / 2) + 1
            end_index = start_index + self.number_of_vertical_lines - 1
            if last_x <= start_index:
                r = 1
            if last_x >= end_index - 1:
                r = 2
            self.tiles_coordinates.append((last_x, last_y))
            if r == 1:
                last_x = last_x + 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y = last_y + 1
                self.tiles_coordinates.append((last_x, last_y))
            if r == 2:
                last_x = last_x - 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y = last_y + 1
                self.tiles_coordinates.append((last_x, last_y))
            last_y = last_y + 1

    def get_line_x_from_index(self, index):
        central_line_x = self.perspective_point_x
        spacing = self.vertical_lines_spacing * self.width
        offset = index - 0.5
        line_x = central_line_x + offset * spacing + self.current_offset_x
        return line_x

    def get_tile_coordinates(self, ti_x, ti_y):
        ti_y = ti_y - self.current_loop_y
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y

    def get_line_y_from_index(self, index):
        spacing_y = self.horizontal_lines_spacing * self.height
        line_y = index * spacing_y - self.current_offset_y
        return line_y

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.number_of_vertical_lines):
                self.vertical_lines.append(Line())

    def update_tiles(self):
        for i in range(0, self.number_of_tiles):
            tile = self.tiles[i]
            tile_coordinates = self.tiles_coordinates[i]
            xmin, ymin = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])
            xmax, ymax = self.get_tile_coordinates(tile_coordinates[0] + 1, tile_coordinates[1] + 1)
            x1, y1 = self.transform(xmin, ymin)
            x2, y2 = self.transform(xmin, ymax)
            x3, y3 = self.transform(xmax, ymax)
            x4, y4 = self.transform(xmax, ymin)
            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def update_vertical_lines(self):
        start_index = -int(self.number_of_vertical_lines / 2) + 1
        for i in range(start_index, start_index + self.number_of_vertical_lines):
            line_x = self.get_line_x_from_index(i)
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.number_of_horizontal_lines):
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):
        start_index = -int(self.number_of_vertical_lines / 2) + 1
        end_index = start_index + self.number_of_vertical_lines - 1
        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)
        for i in range(0, self.number_of_horizontal_lines):
            line_y = self.get_line_y_from_index(i)
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def update(self, dt):
        time_factor = dt * 60
        self.ids.pause_button.opacity = 0
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()

        if not self.state_game_over and self.state_game_has_started and not self.is_paused:
            self.sound_music1.play()
            speed_y = self.speed * self.height / 100
            self.current_offset_y = self.current_offset_y + speed_y * time_factor

            spacing_y = self.horizontal_lines_spacing * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y = self.current_offset_y - spacing_y
                self.generate_tile_coordinates()
                self.current_loop_y = self.current_loop_y + 1

            self.score = str(self.current_loop_y)

            speed_x = self.current_speed_x * self.width / 100
            self.current_offset_x = self.current_offset_x + speed_x * time_factor
            self.ids.pause_button.opacity = 1

        if not self.check_ship_collision() and not self.state_game_over:
            self.sound_gameover_impact.play()
            self.state_game_over = True
            self.menu_widget.opacity = 1
            self.final_score = 'SCORE: ' + self.score
            self.reset_game()
            self.sound_music1.stop()
            self.menu_title = 'G A M E   O V E R!'
            self.menu_button_title = 'RESTART'
            self.sound_gameover_voice.play()
            self.ids.pause_button.opacity = 0
            self.sound_gameover_voice.play()
            self.state_game_has_started = False

    def on_start_game(self):
        self.state_game_has_started = True
        self.menu_widget.opacity = 0
        if self.menu_button_title == 'START':
            self.sound_begin.play()
        self.speed = 0.7
        self.speed_x = 1
        if self.is_paused:
            self.toggle_pause()
        if self.menu_button_title == 'RESTART':
            self.sound_restart.play()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused and not self.state_game_over and self.state_game_has_started:
            self.menu_title = 'G A M E   P A U S E D !'
            self.menu_button_title = 'RESUME'
            self.sound_music1.stop()
            self.new_current_offset_y = self.current_offset_y
            self.current_offset_y = 0
            self.new_score = self.score
            self.final_score = 'SCORE: ' + self.score
            self.menu_widget.opacity = 1
            self.ids.pause_button.opacity = 0
        elif not self.state_game_over and self.state_game_has_started:
            self.current_offset_y = self.new_current_offset_y
            self.menu_widget.opacity = 0
            self.ids.pause_button.opacity = 1


class GalaxyApp(App):
    sound_galaxy = SoundLoader.load('audio/galaxy.wav')
    sound_galaxy.volume = 1

    def on_start(self):
        self.sound_galaxy.play()


GalaxyApp().run()
