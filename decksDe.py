# -*- coding: utf-8 -*-
import requests
from json import loads
from pparser import Parser
from bs4 import BeautifulSoup

class DecksDe(Parser):
    def __init__(self, login, password, sitefolder, parsername):
        super(DecksDe, self).__init__(login, password, sitefolder, parsername)
        self.DOM = "https://www.decks.de"
        self.data = {
            "login":"",
            "ort":"login",
            "useremail":login,
            "userpass":password
            }
        self.mainCycle()
        
    def auth(self):
        self.loginHandler = self.session.post("https://www.decks.de/decks/include/php/login.php", data=self.data)
        print("Авторизовались")
    
    def basketWork(self):
        basket = self.session.get("https://www.decks.de/decks/order/warenkorb.php?v=wk")
        soup = BeautifulSoup(basket.text, 'lxml')
        items = soup.find_all("div", class_="oneLineWK")
        links = [self.DOM + item.find('div', class_='coverBox').find('a').get('href') for item in items]
        return links
    
    def tracksGet(self, tid):
        phpAudio = self.session.get("https://www.decks.de/decks/rpc/getAudio.php?id={}".format(tid))
        phpAudioJsoned = loads(phpAudio.text)
        links = phpAudioJsoned.get('sound')
        names = phpAudioJsoned.get('track')
        return links, names
    
    def getAllPages(self, reason):
        links = self.basketWork()
        result = list()
        for link in links:
            page = self.session.get(link)
            soup = BeautifulSoup(page.text, 'lxml')
            labelDetail = soup.find('div', class_='detail_label').find('h1').text.split('/')
            A,B = labelDetail[1], labelDetail[0]
            artistDetail = soup.find('div', class_='detail_artist').find('h1').text
            titleDetail = soup.find('div', class_='detail_titel').find('h1').text
            styleBox = soup.find('div', class_='StyleBox').find('div', class_="LStylehead").text
            
            infodates = soup.find_all('div', class_="infodateblock")
            infodateM = list()
            for infodate in infodates:
                try:
                    if infodate.find('div', class_="infodateval").text != "":
                        infodateM.append(infodate.find('div', class_="infodateval").text)
                    
                except:
                    None
                    
            print(infodateM)
            try:
                infodateM = "{a} {b}".format(a=infodateM[0], b=infodateM[1])
            except:
                infodateM = "{a}".format(a=infodateM[0])
            
            infomemo = soup.find("div", id="info_memo").find('p').text
            bonusText = str()
            try:
                bonusText = soup.find('div', class_="bonusTxt").find('blockquote').text
            except:
                None
            description = "{a} {b}".format(a=infomemo,b=bonusText)
            if reason == 0:
                result.append((A,B, artistDetail, titleDetail, styleBox, infodateM, description))
            elif reason == 1:
                tracks = soup.find_all('div', class_='OneListen')
                tracksId = tracks[0].find('div').get('data-code')
                tracksNames = list()
                tracks, tracksNames = self.tracksGet(tracksId)
                
                detailCover = soup.find('div', id="detail_cover")
                photos = detailCover.find_all('img')
                photos = [photo.get('data-zoom-image') for photo in photos]
                folderName = f'{A} {B} {artistDetail} {titleDetail} {styleBox}'
                
                self.savePics(name=A,foldername=folderName,urls=photos)
                self.saveMp3s(name=tracksNames,foldername=folderName,urls=tracks)
                
                
            
        return result