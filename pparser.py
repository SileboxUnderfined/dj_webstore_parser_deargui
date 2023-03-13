# -*- coding: utf-8 -*-
from abc import abstractmethod
import requests
import os
from openpyxl import Workbook

class Parser:
    def __init__(self, login, password, sitefolder, parsername):
        self.folder = sitefolder
        self.parsername = parsername
        self.userAgent = 'Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'
        self.session = requests.Session()
        self.session.headers['User-Agent'] = self.userAgent
        
    def makedirs(self, path):
        os.makedirs(path, exist_ok=True)
        
    def delete_bad_symb(self, s):
        badsymbs = '( ) ‘ : , & “ ; ! ? * % # [ ] { } --- > -- ... .. /" / \''.split()
        for symb in badsymbs:
            s = s.replace(symb,'')
        return s
  
    def writeExcel(self, data, name="output.xlsx"):
        wb = Workbook()
        ws = wb.active
        [ws.append(row) for row in data]
        try:
            wb.save(f"{self.folder}/{name}")
        except FileNotFoundError:
            os.makedirs(self.folder)
            self.writeExcel(data)
            
    def savePics(self, name, foldername, urls):
        path = os.path.join(self.folder, foldername)
        self.makedirs(path)
        charNeeded = 65

        for url in urls:
            fname = name + "-" + chr(charNeeded) + ".jpeg"
            fname = self.delete_bad_symb(fname)

            fileraw = self.session.get(url, stream=True)
            with open(os.path.join(path, fname), 'wb') as file:
                file.write(fileraw.content)

            charNeeded += 1

    def saveMp3s(self, name, foldername, urls):
        path = os.path.join(self.folder, foldername)
        self.makedirs(path)

        for i in range(len(urls)):
            fname = self.delete_bad_symb(name[i])
            fileraw = self.session.get(urls[i], stream=True)
            with open(os.path.join(path, fname + '.mp3'), 'wb') as file:
                file.write(fileraw.content)
                
            print(f'Скачали аудиофайл - {fname}')
            
    def mainCycle(self):
        self.auth()
        print("создаём файл Excel...")
        data = self.getAllPages(0)
        self.writeExcel(data,name="output.xlsx")
        print("файл(ы) Excel был успешно создан(ы).")
        print("Собираем аудиозаписи и обложки...")
        mediaData = self.getAllPages(1)
        print("Аудиозаписи и обложки были успешно собраны.")
        print("Парсер {} завершил свою работу".format(self.parsername))
    
    @abstractmethod
    def auth(self):
        pass
    
    @abstractmethod
    def getAllPages(self):
        pass