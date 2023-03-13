# -*- coding: utf-8 -*-
from pparser import Parser
import re
import requests
from bs4 import BeautifulSoup

class VynilFuture(Parser):
    def __init__(self, login, password, sitefolder, parsername, link_struct):
        super(VynilFuture, self).__init__(login, password, sitefolder, parsername)
        self.DOM = "https://www.vinylfuture.com"
        self.link_struct = link_struct
        self.data = {
            'loginFeld': login,
            'passwortFeld': password,
            'vinylfuture': '',
            'loginSubmit': 'LogIn',
            'href': '/start'
        }
        self.mainCycle()
        
    def auth(self):
        self.loginHandler = self.session.post('https://www.vinylfuture.com/ajaxHelper/handleLogin.php',data=self.data)
        print("Авторизовались")
        
    def getAllPages(self, reason):
        page, next_page = 1, True
        data = []

        while next_page:
            link = f'{self.link_struct}{page}'
            r = self.session.get(link)
            soup = BeautifulSoup(r.text, 'lxml')

            print(f'Парсим страницу {page}')

            items = soup.find_all('article', class_='product')

            for item in items:
                imgs = item.find_all('div', class_='img')
                #print(imgs)
                imgs = [self.DOM + img.find('img').get('src').replace('/m/','/xl/') for img in imgs]
                print(imgs)
                tracks = item.find('ul', class_='playtrack')
                if type(tracks) != type(None):
                    tracks = tracks.find_all('li')
                    tracks = [track.find('a', class_='track') for track in tracks]
                    tracksNames = [t.text.strip() for t in tracks]
                    # [track.find('b').decompose() for track in tracks]

                    parts = imgs[0].split('/')
                    parts = [p for p in parts if p]
                    part = 'https://www.vinylfuture.com/streamit/{}/{}/'.format(parts[-3], parts[-2])
                    tracks = [part + t.get('href').split('__')[-1].replace('_', '') + '.mp3' for t in
                              tracks]

                name = item.find('div', class_='label')
                name1 = name.find('strong').text
                name2 = name.text.replace("add label to watchlist", "").replace(name1, "")
                art1 = item.find('h2', class_='artist').find('a').text
                art2 = item.find('h3', class_='title').text
                style = item.find('div', class_='style')
                desc = item.find('div', class_='description').text
                styleText = str()
                for string in style.stripped_strings:
                    styleText += string + " "

                date = item.find('div', class_='date').text
                price = str()

                try:
                    price = item.find('span', class_='price').text
                except:
                    price = "OUT OF STOCK"
                
                
                if type(tracks) != None and reason == 1:
                    mp3Name = "{name1} {name2} {art1} {art2}".format(name1=name1,name2=name2,art1=art1,art2=art2)
                    picsName = f"{name1}".replace(" ","-")
                    self.savePics(foldername=mp3Name, name=picsName, urls=imgs)
                    self.saveMp3s(name=tracksNames, foldername=mp3Name, urls=tracks)
                    
                if type(tracks) == None and reason == 1:
                    mp3Name = "{name1} {name2} {art1} {art2}".format(name1=name1,name2=name2,art1=art1,art2=art2)
                    picsName = f"{name1}".replace(" ","-")                    
                    self.savePics(foldername=mp3Name, name=picsName, urls=imgs)
                
                if reason == 0:
                    tracksCount = int()
                    try:
                        tracksCount = len(tracks)
                    except:
                        tracksCount = 0
                        
                    toData = [name1,art1,art2,name2,f"{art1} - {art2}",desc,styleText,date,"0.26",price]
                    if tracksCount != 0:
                        for i in range(tracksCount):
                            toData.append(f"Track {i+1}")
                    
                    data.append(toData)
                
            next_page = len(items) > 0
            page += 1
        return data