from bs4 import BeautifulSoup
from requests import session
from os import makedirs
OUTPUTDIR = 'output/'
DOM = 'http://www.vinylfuture.com'

def logining():
    userAgent = 'Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'
    data = {
    'loginFeld': 'megrikyan@gmail.com',
    'passwortFeld': '5f354faa51aa7',
    'vinylfuture': '',
    'loginSubmit': 'LogIn',
    'href': '/start'
    }
    ss = session()
    ss.headers['User-Agent'] = userAgent
    loginHandler = ss.post('https://www.vinylfuture.com/ajaxHelper/handleLogin.php',data=data)
    return ss

def getAllPages(ss):
    page, next_page = 1, True
    data = []

    while next_page:
        r = ss.get(
            f'https://www.vinylfuture.com/m_myDeejay/sm_myRecords/sort_interpretasc/perpage_160/page_{page}')
        soup = BeautifulSoup(r.text, 'lxml')

        print(f'Парсим страницу {page}')

        wrapDiv = soup.find(id='wrapwrapper')
        frame = wrapDiv.find(id="myIframe")

        pr = ss.get(DOM + frame['src'])
        soup = BeautifulSoup(pr.text,'lxml')

        items = soup.find_all('article', class_='product')

        for item in items:
            imgs = item.find_all('div', class_='img')
            imgs = [DOM + img.find('a', class_='zoom').get('href') for img in imgs]

            name = item.find('div', class_='label')
            name1 = name.find('strong').text
            name2 = name.text.replace("add label to watchlist", "").replace(name1, "")
            art1 = item.find('h2', class_='artist').find('a').text
            art2 = item.find('h3', class_='title').text

            picsName = f"{name1}".replace(" ","-")
            foldername = f'{deleteBad(name1)}/'
            collected = (imgs,picsName,foldername)
            data.append(collected)

        print('количество найденых элементов - ',len(items))
        next_page = len(items) > 0
        page += 1
    return data

def deleteBad(s):
    badsymbs = '( ) ‘ : , & “ ; ! ? * % # [ ] { } / --- > -- ... . .. "'.split()
    for symb in badsymbs:
        s = s.replace(symb,'')
    return s

def dumpImages(data,ss):
    for img in data:
        path = f'{OUTPUTDIR}{img[2]}'
        try:
            makedirs(path)
        except FileExistsError:
            pass
        picsName = f'{deleteBad(img[1])}.jpeg'
        print(f'скачиваем {picsName} в папку {path}')
        raw = ss.get(img[0][0],stream=True)
        with open(f'{path}{picsName}','wb') as f:
            f.write(raw.content)

        print('скачивание завершено успешно')

if __name__ in "__main__":
    ss = logining()
    imgs = getAllPages(ss)
    dumpImages(imgs,ss)