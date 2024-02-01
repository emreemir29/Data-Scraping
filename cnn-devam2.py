from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

browser = webdriver.Firefox()
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
    
    print("Haber başlıkları başarıyla kaydedildi.")
else:
    print("Aradığınız anahtar kelimeye uygun haber bulunamadı.")

# Haber URL'lerini tutacak bir liste oluşturalım
haber_url_leri = []
    
# Haber URL'sini alalım
haber_link = metin.find("span", attrs={"class":"container__headline-text"})
if haber_link is not None:
    haber_url = haber_link["data-zjs-href"]
    haber_url_leri.append(haber_url)
else:
    print("Haber linki bulunamadı.")


# Haber içeriklerini tutacak bir liste oluştura lım
haber_icerikleri = []

for haber_url in haber_url_leri:
    # Haber URL'sini ziyaret edelim
    browser.get(haber_url)

    # Sayfanın yüklenmesini bekleyelim
    time.sleep(5)

    # Sayfanın kaynak kodunu alalım
    html = browser.page_source

    # Kaynak kodu BeautifulSoup ile analiz edelim
    soup = BeautifulSoup(html, "html.parser")
   
    # Haber içeriğini alalım

    classes = ["video-resource__description", "article__content"]  # Aramak istediğiniz class isimlerini buraya ekleyin
    for class_name in classes:
        elements = soup.find_all("div", attrs={"class": class_name})
        for element in elements:
            if element is not None:
                haber_icerigi = element.text
            else:
                haber_icerigi = "Element bulunamadı"
    # Haber içeriğini listeye ekleyelim
    haber_icerikleri.append(haber_icerigi)
#düzelt
# Anahtar kelimeleri bir liste içinde belirtelim
anahtar_kelimeler = ["israel", "war", "attack"]

# Her bir anahtar kelimenin kaç kez geçtiğini bulmak için bir sözlük oluşturalım
kelime_sayilari = {}

for haber_icerigi in haber_icerikleri:
    for kelime in anahtar_kelimeler:
        # Eğer kelime daha önce bulunmuşsa, sayısını arttıralım
        if kelime in kelime_sayilari:
            kelime_sayilari[kelime] += haber_icerigi.lower().count(kelime)
        # Eğer kelime daha önce bulunmamışsa, sözlüğe ekleyelim
        else:
            kelime_sayilari[kelime] = haber_icerigi.lower().count(kelime)

# Kelime sayılarını yazdıralım
for kelime, sayi in kelime_sayilari.items():
    print(f"'{kelime}' kelimesi {sayi} kez geçiyor.")

#düzelt  
# Haber başlıkları, URL'leri ve içeriklerini bir DataFrame'e dönüştürelim
df = pd.DataFrame({"Haber Başlıkları": haber_basliklari, "Haber URL'leri": haber_url_leri, "Haber İçerikleri": haber_icerikleri})

# DataFrame'i bir Excel dosyasına kaydedelim
df.to_excel("haber_bilgileri.xlsx", index=False)

print("Haber bilgileri başarıyla kaydedildi.")

"""
# Anahtar kelimeleri bir liste içinde belirtelim
anahtar_kelimeler = ["kelime1", "kelime2", "kelime3"]

# Her bir anahtar kelimenin kaç kez geçtiğini bulmak için bir sözlük oluşturalım
kelime_sayilari = {}

for haber_icerigi in haber_icerikleri:
    for kelime in anahtar_kelimeler:
        # Eğer kelime daha önce bulunmuşsa, sayısını arttıralım
        if kelime in kelime_sayilari:
            kelime_sayilari[kelime] += haber_icerigi.lower().count(kelime)
        # Eğer kelime daha önce bulunmamışsa, sözlüğe ekleyelim
        else:
            kelime_sayilari[kelime] = haber_icerigi.lower().count(kelime)

# Kelime sayılarını yazdıralım
for kelime, sayi in kelime_sayilari.items():
    print(f"'{kelime}' kelimesi {sayi} kez geçiyor.")


"""