import kivy
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import main
import copy


class MyApp(App):

    def build(self):
        self.players = []
        self.cache = set()
        self.char = None
        self.cities = {main.normalize_city_name(x) for x in open("cities.txt", "r").readlines() if x.strip()}
        self.player = 1
        self.r1 = RelativeLayout()
        self.label = Label(text="Введите количество игроков",
                           pos_hint={"x": .25, "y": .8},
                           size_hint=(.5, .06),
                           font_size='56px')
        self.player_label = Label(text=f"Игрок №{self.player}",
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
        self.button1 = Button(size_hint=(.12, .06),
                              pos_hint={"x": .25, "y": 0.5},
                              text="Ответить")
        self.button1.bind(on_release=lambda x: self.input_to_label())
        self.start_button = Button(size_hint=(.12, .06),
                                   pos_hint={"x": .25, "y": 0.5},
                                   text="Старт")
        self.start_button.bind(on_release=lambda x: self.start_game())
        self.r1.add_widget(self.textinput)
        self.r1.add_widget(self.start_button)
        self.r1.add_widget(self.label)
        self.r1.add_widget(self.error_lable)
        return self.r1

    def input_to_label(self):
        city = main.user_point(self.char, self.cache, self.textinput.text, self.cities)
        if city == "redo":
            self.error_lable.text = "Попробуйте ввести город еще раз"
        else:
            self.char = main.get_next_char(city)
            main.move_to_cache(city, self.cities, self.cache)
            self.error_lable.text = ""
            self.label.text = self.textinput.text
            self.textinput.text = ""
            # try:
            #     self.player = self.players.__next__()
            # except StopIteration:
            #     self.players = copy.deepcopy(self.players_cache)
            #     self.players = self.players.__iter__()
            #     self.player = self.players.__next__()
            self.player_label.text = f"Игрок №{self.player}"


    def set_error(self, message: str):
        self.error_lable.text = message

    def get_textinput_text(self):
        return self.textinput.text

    def start_game(self):
        self.r1.remove_widget(self.start_button)
        self.r1.add_widget(self.button1)
        self.r1.add_widget(self.give_up_button)
        self.r1.add_widget(self.player_label)
        self.label.text = "Введите любой город"
        self.players_cache = copy.deepcopy(self.players)
        # self.players = list(range(int(self.textinput.text))).__iter__()

        self.textinput.text = ""


