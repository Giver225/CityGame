from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import main


class MyApp(App):

    def build(self):
        self.players = []
        self.cache = set()
        self.char = None
        self.cities = {main.normalize_city_name(x) for x in open("cities.txt", "r").readlines() if x.strip()}
        self.r1 = RelativeLayout()
        self.label = Label(text="Введите количество игроков",
                           pos_hint={"x": .25, "y": .8},
                           size_hint=(.5, .06),
                           font_size='56px')
        self.player_label = Label(text=f"Игрок №1",
                                  pos_hint={"x": .25, "y": .7},
                                  size_hint=(.5, .06),
                                  font_size='30px')
        self.error_lable = Label(text="",
                                 pos_hint={"x": .25, "y": .2},
                                 size_hint=(.5, .06),
                                 font_size='20px')
        self.textinput = TextInput(size_hint=(.5, .06),
                                   pos_hint={"x": .25, "y": 0.6},
                                   multiline=False)
        self.give_up_button = Button(size_hint=(.12, .06),
                                     pos_hint={"x": .63, "y": 0.5},
                                     text="Сдаться")
        self.give_up_button.bind(on_release=lambda x: self.delete_player())
        self.button1 = Button(size_hint=(.12, .06),
                              pos_hint={"x": .25, "y": 0.5},
                              text="Ответить")
        self.button1.bind(on_release=lambda x: self.input_to_label())
        self.start_button = Button(size_hint=(.12, .06),
                                   pos_hint={"x": .25, "y": 0.5},
                                   text="Старт")
        self.start_button.bind(on_release=lambda x: self.start_game())
        self.again_button = Button(size_hint=(.12, .06),
                                   pos_hint={"x": .44, "y": 0.5},
                                   text="Заново")
        self.again_button.bind(on_release=lambda x: self.new_game())
        self.r1.add_widget(self.textinput)
        self.r1.add_widget(self.start_button)
        self.r1.add_widget(self.label)
        self.r1.add_widget(self.error_lable)
        return self.r1

    def input_to_label(self):
        city = main.user_point(self.char, self.cache, self.textinput.text, self.cities)
        if city == 0:
            self.error_lable.text = f'Город должен начинаться с буквы {self.char.capitalize()}.'
        elif city == 1:
            self.error_lable.text = "Этот город уже был назван."
        elif city == 2:
            self.error_lable.text = "Такого города не существует в России"
        else:
            self.char = main.get_next_char(city)
            main.move_to_cache(city, self.cities, self.cache)
            self.error_lable.text = ""
            self.label.text = self.textinput.text
            self.change_player()

    def change_player(self):
        self.textinput.text = ""
        while True:
            self.player += 1
            if self.player > max(self.players):
                self.player = self.players[0]
            if self.player not in self.players:
                print(self.player, self.players)
                continue
            break
        self.player_label.text = f"Игрок №{self.player}"

    def delete_player(self):
        del self.players[self.players.index(self.player)]
        self.change_player()
        if len(self.players) == 1:
            self.end_game()
        self.error_lable.text = ''

    def set_error(self, message: str):
        self.error_lable.text = message

    def get_textinput_text(self):
        return self.textinput.text

    def end_game(self):
        self.label.text = "Поздравляем, победил"
        self.r1.remove_widget(self.textinput)
        self.r1.remove_widget(self.button1)
        self.r1.remove_widget(self.give_up_button)
        self.r1.add_widget(self.again_button)

    def new_game(self):
        self.r1.remove_widget(self.player_label)
        self.r1.add_widget(self.textinput)
        self.r1.add_widget(self.start_button)
        self.label.text = "Введите количество игроков"
        self.r1.remove_widget(self.again_button)

    def start_game(self):
        try:
            self.players = list(range(1, int(self.textinput.text) + 1))
            if int(self.textinput.text) < 2 or int(self.textinput.text) > 322:
                return
        except:
            return
        self.player = 1
        self.player_label.text = "Игрок №1"
        self.r1.remove_widget(self.start_button)
        self.r1.add_widget(self.button1)
        self.r1.add_widget(self.give_up_button)
        self.r1.add_widget(self.player_label)
        self.label.text = "Введите любой город"
        self.textinput.text = ""
