# !usr\bin\activate
# :using "utf-8":

import customtkinter as ctk
import random as rnd
from PIL import Image
import pyperclip
import ctypes
import sys
import os

import assets.messegespy as msgpy


#__Author__: Zhilyaev Arseniy
#__Mail__: ay.zhiliaev@outlook.com
#__GitHub__: https://github.com/1nonlySeny
VERSION = "PG V1.2 Beta"


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(VERSION)
        self.geometry("400x280")
        self.resizable(False, False)

        try:
            # $Set Windows titlebar icon$
            if sys.platform.startswith('win'):
                self.customtkinter_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                self.after(200, lambda: self.iconbitmap(os.path.join(self.customtkinter_directory, "assets", "icons", "logo.ico")))

                # $Set the taskbar icon$
                myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

        # $Create dependent variables$
        self.digits = ['1', '2', '3', '4', '5','6', '7', '8', '9', '0']

        self.uppercase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                        'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                        'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        
        self.lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                        'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                        'u', 'v', 'w', 'x', 'y', 'z']
        
        self.punctuation = ['%', '*', ')', '?', '@', '#', '$', '~']

        # $Set images for buttons$
        self.copyImg = ctk.CTkImage(light_image=Image.open(os.path.join(self.customtkinter_directory, "assets", "icons", "copy.png")))

        self.build()

    def build(self):
        # $Build widgets$
        self.mainEntry = ctk.CTkEntry(self, width=350, height=50, placeholder_text="Введите количество символов в пароле")
        self.mainEntry.place(x=25, y=20)

        self.digitsBox = ctk.CTkCheckBox(self, width=20, height=20, fg_color="#906DDE", hover_color="#B56DDE", text="Использовать ли цифры при генерации пароля?")
        self.digitsBox.place(x=25, y=80)

        self.uppercaseBox = ctk.CTkCheckBox(self, width=20, height=20, fg_color="#906DDE", hover_color="#B56DDE", text="Использовать ли заглавные буквы \n при генерации пароля?")
        self.uppercaseBox.place(x=25, y=110)

        self.lowercaseBox = ctk.CTkCheckBox(self, width=20, height=20, fg_color="#906DDE", hover_color="#B56DDE", text="Использовать ли строчные буквы \n при генерации пароля?")
        self.lowercaseBox.place(x=25, y=145)

        self.punctuationBox = ctk.CTkCheckBox(self, width=20, height=20, fg_color="#906DDE", hover_color="#B56DDE",  text="Использовать ли специальные символы \n при генерации пароля?")
        self.punctuationBox.place(x=25, y=180)

        self.createBtn = ctk.CTkButton(self, width=70, height=40, text="Сгенерировать", fg_color="#906DDE", hover_color="#B56DDE", command=self.generate )
        self.createBtn.place(x=270, y=220)

        self.copyBtn = ctk.CTkButton(self, image=self.copyImg, text="", fg_color="#906DDE", hover_color="#B56DDE", width=40, height=40, command=lambda: pyperclip.copy(self.textresult.get()))
        self.copyBtn.place(x=225, y=220)

        self.textresult = ctk.CTkEntry(self, width=195, height=40, placeholder_text="Тут будет ваш пароль", text_color="GREEN", state="disabled")
        self.textresult.place(x=25, y=220)


    def generate(self):
        # $Create dependent variables$
        digitsList = []
        uppercaseList = []
        lowercaseList = []
        punctuationList = []
    
        # $Destroy and set the widget to display the result (I can't do it any other way)$
        self.textresult.destroy()
        self.textresult = ctk.CTkEntry(self, width=195, height=40, placeholder_text="Тут будет ваш пароль", text_color="green")
        self.textresult.place(x=25, y=220)
        self.textresult.configure(state="normal")

        # $Translate the string into int. If there is an error, output$
        symbols = int(self.mainEntry.get())

        # $Character count check$
        if symbols < 6:
            self.textresult.insert(0, msgpy.MinimalNumbersSymbols)
            self.textresult.configure(state="disabled", text_color="RED")
        # $Checking for selected categories$
        if self.digitsBox.get() == 0 and self.uppercaseBox.get() == 0 and self.lowercaseBox.get() == 0 and self.punctuationBox.get() == 0:
            self.textresult.insert(0, msgpy.NoGenerationCategoriesSelected)
            self.textresult.configure(state="disabled", text_color="RED")
            return 
       
        # $Check already selected categories and randomize values from their lists$
        if self.digitsBox.get():
            _listlong = len(self.digits)
            for i in range(symbols):
                rndIndex = rnd.randint(0, _listlong - 1)
                digitsList.append(self.digits[rndIndex])
        if self.uppercaseBox.get():
            _listlong = len(self.uppercase)
            for i in range(symbols):
                rndIndex = rnd.randint(0, _listlong - 1)
                uppercaseList.append(self.uppercase[rndIndex])
        if self.lowercaseBox.get():
            _listlong = len(self.lowercase)
            for i in range(symbols):
                rndIndex = rnd.randint(0, _listlong - 1)
                lowercaseList.append(self.lowercase[rndIndex])
        if self.punctuationBox.get():
            _listlong = len(self.punctuation)
            for i in range(symbols):
                rndIndex = rnd.randint(0, _listlong - 1)
                punctuationList.append(self.punctuation[rndIndex])

        # $Combine the randoms in the litas into one and mix it up$
        output = digitsList + uppercaseList + lowercaseList + punctuationList
        rnd.shuffle(output)

        # $Basic password creation cycle$ 
        while len(output) != symbols:
            _listlong = len(output)
            index = rnd.randint(0, _listlong)
            try:
                output.pop(index)
            except IndexError:
                try:
                    output.pop(index - 1)
                except IndexError:
                    pass

        else:
            rnd.shuffle(output)
            _result = ''.join(output)
            self.textresult.insert(0, _result)
            self.textresult.configure(state="disabled", text_color="RED")
        

if __name__ == '__main__':
    app = MainApp()
    app.mainloop()

