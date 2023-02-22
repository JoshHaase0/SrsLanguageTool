import pickle
from languages import bosnian as lng
import os.path
from random import randint
from functools import partial

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.core.window import Window

# Time : 3 hours, 55 minutes

# Joshua Haase 2/15/2023 1.0
#       Created the base app as a terminal program with a Bosnian word library of 99
# Joshua Haase 2/17/2023 1.1
#       Changed the weighted system, used to roll then roll again based on weight. now there is only one roll
#       to find the word. A new list is generated with each word repeated the same amount as its own weight.
# Joshua Haase 2/19/2023 2.0
#       Did a complete overhaul of the system and gui. Gave it a real gui instead of a terminal
#           // Plans to make a mobile version and to make keybinds for the pc version
# Joshua Haase 2/19/2023 2.1
#       Expanded the Bosnian word library to 150 words. Made saves update when word library is expanded
#       instead of deleting and starting a new save.
# Joshua Haase 2/22/2023 2.2
#       Added keyboard functionality, enter for confirm word, esc for new word, rctrl for hint
#       Plan on adding a refocus for the textbox



class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            pass 
        self._keyboard.bind(on_key_down = self._on_keyboard_down)

    def build(self):
        self.dictionary = lng if not self.exists() else self.read_Save()
        if len(self.dictionary) < len(lng):
            old = len(self.dictionary)
            for i in range(len(lng) - len(self.dictionary)):
                self.dictionary.append(lng[old+i])
            self.write_Save(self.dictionary)

        self.location = self.gen_Word()
        self.current_Word = self.dictionary[self.location][0]
        self.eng_Words = self.dictionary[self.location][1].lower().split(" / ")


        # Starts building the gui

        main_layout = BoxLayout(orientation = "vertical")
        # Builds the top bar
        top_bar = BoxLayout(size_hint = (1, 0.3))
        hint_Button = Button(text = "Hint",
                             pos_hint = {"center_x" : 0.5, "center_y" : 0.5})
        hint_Button.bind(on_press = self.on_button)
        top_bar.add_widget(hint_Button)
        self.hint_Text = TextInput(multiline = True,
                              readonly = True,
                              halign = "left",
                              font_size = 25)
        top_bar.add_widget(self.hint_Text)
        new_Word_Button = Button(text = "New Word",
                                 pos_hint = {"center_x" : 0.5, "center_y" : 0.5})
        new_Word_Button.bind(on_press = self.on_button)
        top_bar.add_widget(new_Word_Button)

        # Builds the middle bar
        middle_bar = BoxLayout(size_hint = (1, 1))
        self.word = Button(text = self.current_Word,
                      pos_hint = {"center_x" : 0.5, "center_y" : 0.5},
                      font_size = 55)
        self.word.bind(on_press = self.on_guess)
        middle_bar.add_widget(self.word)

        # Builds the bottom bar
        bottom_bar = BoxLayout(size_hint = (1, 0.3))
        self.guess = TextInput(multiline = False,
                               halign = "right",
                               font_size = 55,
                               size_hint = (0.9, 1))
        bottom_bar.add_widget(self.guess)
        save_Button = Button(text = "Save",
                             pos_hint = {"center_x" : 0.5, "center_y" : 0.5},
                             size_hint = (0.1, 1))
        save_Button.bind(on_press = self.on_button)
        bottom_bar.add_widget(save_Button)

        # Puts it all together
        main_layout.add_widget(top_bar)
        main_layout.add_widget(middle_bar)
        main_layout.add_widget(bottom_bar)

        return main_layout

    # Processes all button inputs
    def on_button(self, instance):
        match (instance.text):
            case "Hint":
                self.hint_Text.text = f"{self.dictionary[self.location][1][0:2]}...\nLength: {len(self.eng_Words[0])}\nWords: {len(self.eng_Words)}"
            case "New Word":
                self.new_word()
            case "Save":
                self.write_Save(self.dictionary)

    def on_guess(self, instance):
        guess = self.guess.text.lower()
        if guess[0:2] != "./":
            if guess not in self.eng_Words:
                self.dictionary[self.location][2] += 4
                self.word.background_color = get_color_from_hex("#FF0F0F")
                self.word.text = f"{self.dictionary[self.location][0]} : {self.dictionary[self.location][1]}"
            elif guess in self.eng_Words:
                self.dictionary[self.location][2] -= 3
                self.new_word()
        else:
            if guess == "./save":
                self.write_Save(self.dictionary)
            elif guess == "./read":
                text = ""
                for i in self.dictionary:
                    text += f"{i}\n"
                self.hint_Text.text = text

    def new_word(self):
        self.location = self.gen_Word()
        self.current_Word = self.dictionary[self.location][0]
        self.eng_Words = self.dictionary[self.location][1].lower().split(" / ")
        self.word.text = self.current_Word
        self.word.background_color = get_color_from_hex("#00FF0F")
        self.hint_Text.text = ""
        self.guess.text = ""




    # Writes a save file
    def write_Save(self, save):
        with open('save', 'wb') as fp:
            pickle.dump(save, fp)
            print("\nSave finished\n")
            self.hint_Text.text = "Save finished"

    # Reads a save file
    def read_Save(self):
        with open('save', 'rb') as fp:
            save = pickle.load(fp)
            return save
        
    # Returns a bool for if the file exists or not
    def exists(self):
        return os.path.isfile("save")

    # Generates a new word
    def gen_Word(self):
        weighted_Locations = []
        for i in range(len(self.dictionary)):
            for j in range(self.dictionary[i][2]):
                weighted_Locations.append(i)
        location = weighted_Locations[randint(0, len(weighted_Locations) - 1)]
        return location
    
    def _keyboard_closed(self):
        pass
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(f"{keycode}")
        if (keycode[0] == 13):
            self.on_guess(self.word)
        elif (keycode[0] == 306):
            self.hint_Text.text = f"{self.dictionary[self.location][1][0:2]}...\nLength: {len(self.eng_Words[0])}\nWords: {len(self.eng_Words)}"
        elif (keycode[0] == 27):
            self.new_word()
        return True

if __name__ == "__main__":
    app = MainApp()
    app.run()
