from bs4 import BeautifulSoup
import requests


def generateListAutoMake(_url, _attrName, _subAttrName):
    r = requests.get(_url)
    #r = requests.get("https://www.truecar.com/shop/new/?filterType=brand") or https://www.truecar.com/shop/new/?filterType=brand&makeSlug=jaguar
    #data-test-item
    #"shopMakeModelMakeListTab"  or "shopNewMakeModelSelectItem"
    s = BeautifulSoup(r.content,'html.parser')
    a = []
    i = 0
    textModel = s.find_all(attrs={"data-test":_attrName})
    for text in textModel:
        b = textModel[i][_subAttrName]
        i += 1
        a.append(b)
    return a

url = "https://www.truecar.com/shop/new/?filterType=brand"
subAttributeName = "data-test-item"
attributeName = "shopMakeModelMakeListTab"
#url = input("enter URL:")
#attrName = input("enter Attribute to Search:")
#subAttrName = input("enter Sub Attribute to Search:")

makeList = generateListAutoMake(url,attributeName,subAttributeName)

#https://www.truecar.com/shop/new/?filterType=brand&makeSlug=

