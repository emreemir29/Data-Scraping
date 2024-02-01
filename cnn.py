from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

browser = webdriver.Chrome()
browser.get("https://edition.cnn.com/")

# arama kutusunu bulalım ve tıklayalım
arama_kutusu = browser.find_element(By.CSS_SELECTOR, ".header__search-icon")
arama_kutusu.click()

# arama kutusuna metin yazalım
time.sleep(2)
text_alani = browser.find_element(By.XPATH, "//input[@placeholder='Search CNN...']")
text_alani.send_keys("israel palestine war")

# arama düğmesine tıklayalım
time.sleep(3)
text_button = browser.find_element(By.CSS_SELECTOR, ".search-bar__button-text")
text_button.click()

# sayfanın yüklenmesini bekleyelim
time.sleep(5)

# Sayfanın kaynak kodunu alalım.
html = browser.page_source

# Kaynak kodu BeautifulSoup ile analiz edelim.
soup = BeautifulSoup(html, "html.parser")

metinler = soup.find_all("div", attrs={"class": "container__text container_list-images-with-description__text"})
haber_basliklari = []
for metin in metinler:
    haber_basliklari.append(metin.find("span", attrs={"class":"container__headline-text"}).text)

if len(haber_basliklari) > 0:
    print("Haber başlıkları:")
    for baslik in haber_basliklari:
        print(baslik)
    
    # Haber başlıklarını bir Excel dosyasına kaydedelim.
    df = pd.DataFrame(haber_basliklari, columns=["Haber Başlıkları"])
    df.to_excel("haber_basliklari.xlsx", index=False)
    
    print("Haber başlıkları başarıyla kaydedildi.")
else:
    print("Aradığınız anahtar kelimeye uygun haber bulunamadı.")

# tarayıcıyı kapat
browser.quit()
