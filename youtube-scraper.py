from selenium import webdriver 
import pandas as pd 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
#driver = webdriver.Chrome(ChromeDriverManager().install())
#wait = WebDriverWait(driver, 10)
df = pd.DataFrame(columns = ['link', 'title', 'description', 'views', 'likes'])

links =["https://www.youtube.com/watch?v=nqtobIpZt68&ab_channel=%24uicideboy%24"]

def scrape(url):
    r = requests.get(url)
    s = BeautifulSoup(r.text, "html.parser")
    st = str(s)
    with open("soup.txt", 'w', encoding="utf-8") as f:
        f.write(st)
    #title
    title = s.find("title").text
    title = title[:-10] #remove ' - YouTube'
    #likes    
    l = st.index("likes")
    likes = st[l-15:l-1]
    q = likes.index('"')
    while True:
        likes = likes[q+1:]
        try:
            q = likes.index('"')
        except:
            break
    likes = likes[q-1:].translate(str.maketrans('', '', ','))
    #views
    v = st.index('viewCount')
    views = st[v+12:v+24]
    q = views.index('"')
    views = views[:q]
    #description
    d = st.index('shortDescription')
    #descriptions have a max length of 5000
    #so to be safe we must scan back at least that amount
    description = st[d+19:d+5019]
    q = description.index('"')
    description = description[:q]
    data = {'title':title, 'views':views, 'likes':likes,
            'description':description}

    return data

for x in links:
    data = scrape(x)
    print(data)
