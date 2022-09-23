from datetime import date
from bs4 import BeautifulSoup
import requests

def generateList(_url, _attrName):
    r = requests.get(_url)
    s = BeautifulSoup(r.content,'html.parser')
    a = []
    i = 0
    textModel = s.find_all(attrs={"data-test":_attrName})
    for text in textModel:
        b = textModel[i].div.next_sibling.string
        i += 1
        a.append(b)
    return a

def buildModelUrl(_makeItem):
    makeSlug = _makeItem.lower()
    return f'https://www.truecar.com/shop/new/?filterType=brand&makeSlug={makeSlug}'

def buildUrl(_carMake, _carModel, _carYear):
    return f'https://www.truecar.com/{_carMake}/{_carModel}/{_carYear}/build/?postalCode=75080'

def generateYearMakeModelTrimMsrp(year, make, model, _url):
    r = requests.get(_url)
    s = BeautifulSoup(r.content, 'html.parser')
    a = []
    textTrim = s.find_all(attrs={"data-test":"trimHighlightsCardName"})
    textMsrp = s.find_all(attrs={"data-test":"trimHighlightsCardMsrp"})
    j = len(textTrim)
    for i in range(j): 
        trim = textTrim[i].string
        msrp = textMsrp[i].string
        str = f'"{year}","{make}","{model}","{trim}","{msrp}"'
        a.append(str)
    return '\n'.join(a)

def compileLists(_makeList): 
    a = []

    for make in _makeList:
        url = buildModelUrl(make)
        modelList = generateList(url,"shopNewMakeModelSelectItem")
        for model in modelList:
            year = date.today().year
            url = buildUrl(make, model, year)
            list = generateYearMakeModelTrimMsrp(year, make, model, url)
            if list: a.append(list)
            year = year + 1
            url = buildUrl(make, model, year)
            list = generateYearMakeModelTrimMsrp(year, make, model, url)
            if list: a.append(list)
            print(f'completed: {make} {model}')
    return a

url = "https://www.truecar.com/shop/new/?filterType=brand"
makeList = generateList(url,"shopMakeModelMakeListTab")
makeAndModel = compileLists(makeList)
msrps = '\n'.join(makeAndModel)

f = open("msrp.csv", "w")
f.write(msrps)
f.close()
