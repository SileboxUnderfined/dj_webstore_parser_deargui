# -*- coding: utf-8 -*-
import json
from vynilFuture import VynilFuture
from decksDe import DecksDe

class Main:
    def __init__(self):
        self.version = 1.1
        self.vynilFutureData = self.readSettings("vynilfuture.json")
        self.decksdeData = self.readSettings("decksde.json")

    def mainCycle(self):
        print("Parser version", self.version)
        print("Выберите парсер")
        print("1 - VynilFuture\n2 - decks.de\n9 - настройки\nEnter - выход")
        choice = self.choiceInputter()
        if choice == 1:
            vynilf = VynilFuture(self.vynilFutureData.get('login'), self.vynilFutureData.get('password'), "output/vynilFuture", "vynilFuture")
        elif choice == 2:
            decksde = DecksDe(self.decksdeData.get('login'), self.decksdeData.get('password'), "output/decksDe", "decksDe")
        elif choice == 9:
            self.doYouWantToChange()
        else:
            print("Выходим из программы")
            return
        
        self.mainCycle()

    def doYouWantToChange(self):
        print("Настройки какого парсера вы хотите изменить?\n1- VynilFuture\n2 - DancingVynil\n0 - назад")
        choice = self.choiceInputter()
        if choice == 1:
            self.settingsChange("vynilfuture.json")
        elif choice == 2:
            self.settingsChange("decksde.json")

    def settingsChange(self, settingsFile):
        readedDict = self.readSettings(settingsFile)
        saveDict = {"login": readedDict['login'], "password": readedDict['password']}
        print("Что вы хотите изменить?\n1 - логин\n2 - пароль\nEnter - применить изменения")
        choice = self.choiceInputter()

        if choice == 1:
            print("Ваш логин - ", saveDict['login'])
            print("Ведите новый логин")
            saveDict['login'] = input(">>> ")

        elif choice == 2:
            print("Ваш пароль - ", saveDict['password'])
            print("Введите новый пароль")
            saveDict['password'] = input(">>> ")

        elif choice == 0:
            self.createSettingsFileUserEdited(saveDict, settingsFile)
        
        elif choice == 0 and saveDict['login'] == readedDict['login'] or saveDict['password'] == readedDict['password']:
            print("Вы не внесли изменений")

        self.mainCycle()

    def readSettings(self, settingsFile):
        savedDict = dict()
        try:
            with open(settingsFile, "rt") as f:
                savedDict = json.load(f)

        except:
            self.createSettingsFile(settingsFile)

        return savedDict

    def createSettingsFile(self, settingsFile):
        print("данные от сайта", settingsFile.replace(".json", ""))
        print("Введите логин")
        login = input(">>> ")
        print("Введите пароль")
        password = input(">>> ")
        toSave = {"login": login, "password":password}
        with open(settingsFile, "wt") as f:
            json.dump(toSave, f)

    def createSettingsFileUserEdited(self, data, settingsFile):
        with open(settingsFile, "wt") as f:
            json.dump(data,f)

        self.mainCycle()
        
    def choiceInputter(self):
        choice = input(">>> ")
        if choice == "":
            return 0
        try:
            choice = int(choice)
        except:
            print("Вы ввели не число")
            self.choiceInputter()
        
        return choice

if __name__ == '__main__':
    m = Main()
    m.mainCycle()
