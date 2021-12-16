import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pywhatkit as pwt
import pyautogui as pygui
import requests

# telegram_api_ key = "5056598073:AAGhD-kiMHD-QdtQA7jb_LLZP9SNfKUzFvg"


import time

ua = UserAgent()

opts = Options()
opts.add_argument("user-agent="+ua.random)
driver = webdriver.Chrome(options=opts)
actions = ActionChains(driver)

def busqueda():
    # idavuelta = driver.find_element(By.XPATH, '//*[@id="form_busqueda"]/div/div[2]/div[2]/div/label/span').click()
    origen = driver.find_element(By.XPATH,'//*[@id="form_busqueda"]/div/div[3]/div[1]/div[1]/div[1]')
    origen.click()
    bsas = driver.find_element(By.XPATH,'//*[@id="form_busqueda"]/div/div[3]/div[1]/div[1]/div[2]/div/div[14]')
    bsas.click()
    destino = driver.find_element(By.XPATH,'//*[@id="form_busqueda"]/div/div[3]/div[2]/div[1]/div[1]')
    destino.click()
    actions.send_keys('Mar del plata')
    actions.perform()
    time.sleep(2)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(0.5)
    # mdq = driver.find_element(By.XPATH, '//*[@id="form_busqueda"]/div/div[3]/div[2]/div[1]/div[2]/div/div')
    # time.sleep(2)
    # mdq.click()
    fechaida = driver.find_element(By.XPATH, '//*[@id="form_busqueda"]/div/div[4]/div[1]/div[1]/a/span').click()
    monthchange = driver.find_element(By.XPATH, '//*[@id="datepicker-calendar-fecha_ida"]/div[1]/div[2]').click()
    fechita = driver.find_element(By.XPATH, '//*[@id="cell17-fecha_ida"]').click()
    # fechavuelta = driver.find_element(By.XPATH, '//*[@id="form_busqueda"]/div/div[4]/div[2]/div[1]/a/span').click()
    # vueltita = driver.find_element(By.XPATH,' //*[@id="cell30-fecha_vuelta"]').click()
    buscar = driver.find_element(By.XPATH, '//*[@id="form_busqueda"]/div/div[7]/div/button').click()

def send_message(message):
    print("Send Message")
    requests.post('https://api.telegram.org/bot5056598073:AAGhD-kiMHD-QdtQA7jb_LLZP9SNfKUzFvg/sendMessage',
                  data = {'chat_id' : '@trencitoboti', 'text' : message})



while True:

    driver.get("https://webventas.sofse.gob.ar/")
    time.sleep(2)


    busqueda()


    html = driver.page_source
    soup = bs4.BeautifulSoup(html, "html.parser")

    # Busca los dias disponibles
    dias = soup.find_all("span", {"class": "dia_numero"})
    calendario_ida = soup.find_all("section", {"class": "calendario ida"})
    asientos_disponibles = soup.find_all("div", {"class": "disponibles"})
    n = soup.find_all("p", {"class": "m-0 cantidad"})

    ndisp = []
    en_stock = []


    # Agrega el dia disponible a la lista de stock
    for dia in dias:
        if "\n" not in dia:
            en_stock.append(dia.text)

    #Agrega los asientos disponibles a la lista de asientos disponibles
    for ln in n:
        ndisp.append(ln.text)



    if bool(en_stock) == True:
        for p, num in zip(en_stock, ndisp):
            send_message("Para el dia: " + p + " hay: " + num + " disponibles")
            print("Para el dia:", p, "hay:", num, "disponibles")
    else:
        check = "nada"
        print("NO HAY NADA MOSTRO")


    time.sleep(10)

