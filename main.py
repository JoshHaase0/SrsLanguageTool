import pickle
from languages import bosnian as lng
import os.path
from random import randint

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex

# Time : 3 hours, 31 minutes

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



class MainApp(App):
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
            self.hint_Text.text = "~Save finished~"
    # Reads a save file
    def read_Save(self):
        with open('save', 'rb') as fp:
            save = pickle.load(fp)
            return save
    # Returns a bool for if the file exists or not
    def exists(self):
        return os.path.isfile("save")

    def gen_Word(self):
        weighted_Locations = []
        for i in range(len(self.dictionary)):
            for j in range(self.dictionary[i][2]):
                weighted_Locations.append(i)
        location = weighted_Locations[randint(0, len(weighted_Locations) - 1)]
        return location

if __name__ == "__main__":
    app = MainApp()
    app.run()



# Legacy code for the console app

# def main():
#     dictionary = lng if not exists() else read_Save()
#     exit = False
#     while True:
#         guess = ""
#         weighted_Locations = []
#         for i in range(len(dictionary)):
#             for j in range(dictionary[i][2]):
#                 weighted_Locations.append(i)
#         location = weighted_Locations[randint(0, len(weighted_Locations)-1)];
#
#         word = dictionary[location][0]
#         eng_Words = dictionary[location][1].lower().split(" / ")
#         while True:
#             print(dictionary[location][0])
#             guess = input("Guess:\t")
#             if guess[0:2] == "./":
#                 break
#             elif guess == "":
#                 print(f"\nWord:\t{dictionary[location][0]}\nHint:\t{dictionary[location][1][0:2]} -- Len: {len(dictionary[location][1].split(' / ')[0])}\n")
#             else:
#                 if guess.lower() in eng_Words:
#                     dictionary[location][2] -= 3
#                 #     Loses weight if the answer is right
#                 else:
#                     dictionary[location][2] += 4
#                 #     Gains weight if the answer is wrong
#
#                 print(f"\n{dictionary[location][0]}\t:\t{dictionary[location][1]} --- WEIGHT: {dictionary[location][2]}\n")
#                 break;
#         if guess == "./SAVE":
#             write_Save(dictionary)
#         elif guess == "./MENU":
#             menu()
#         elif guess == "./QUIT":
#             exit = True
#             break
#         elif guess == "./RELOAD":
#             break
#     if not exit:
#         main()
#
# def menu():
#     while True:
#         option = input("\n\n1.) View Save\n2.) Top Word\n3.) Worst Word\n4.) Return\n")
#         if (option == "1"):
#             save = read_Save()
#             for item in save:
#                 print(f"{item}")
#         elif (option == "2"):
#             max = 0
#             location = 0
#             save = read_Save()
#             for i in range(len(save)):
#                 value = save[i][2]
#                 if value <= max:
#                     max = value
#                     location = i
#             print(f"\nMax: {save[location]}")
#         elif (option == "3"):
#             min = 10000
#             location = 0
#             save = read_Save()
#             for i in range(len(save)):
#                 value = save[i][2]
#                 if value >= min:
#                     min = value
#                     location = i
#             print(f"\nMin: {save[location]}")
#         elif (option == "4"):
#             break
#
#
# # Writes a save file
# def write_Save(save):
#     with open('save', 'wb') as fp:
#         pickle.dump(save, fp)
#         print("\nSave finished\n")
# # Reads a save file
# def read_Save():
#     with open('save', 'rb') as fp:
#         save = pickle.load(fp)
#         return save
# # Returns a bool for if the file exists or not
# def exists():
#     return os.path.isfile("save")
