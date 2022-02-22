import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
import os

# telegram_api_ key = "5056598073:AAGhD-kiMHD-QdtQA7jb_LLZP9SNfKUzFvg"
# holi

import time

# ua = UserAgent()

# Driver y opciones originales
# opts = Options()
# opts.add_argument("user-agent="+ua.random)
# driver = webdriver.Chrome(options=opts)
# actions = ActionChains(driver)

#Para poder hacer deployment en heroku
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1000,1080")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

actions = ActionChains(driver)
#caca
def busqueda():
    # idavuelta = driver.find_element(By.XPATH, '//*[@id="form_busqueda"]/div/div[2]/div[2]/div/label/span').click()
    # time.sleep(0.5)
    origen = driver.find_element(By.XPATH, '//*[@id="form_busqueda"]/div/div[3]/div[1]/div[1]/div[1]')
    origen.click()
    actions.send_keys('buenos aires')
    actions.perform()
    time.sleep(2)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    # bsas = driver.find_element(By.XPATH, '//*[@id="form_busqueda"]/div/div[3]/div[1]/div[1]/div[2]/div/div[14]')
    # bsas.click()
    destino = driver.find_element(By.XPATH, '//*[@id="form_busqueda"]/div/div[3]/div[2]/div[1]/div[1]')
    destino.click()
    time.sleep(1)
    actions.send_keys('pinamar')
    actions.perform()
    time.sleep(2)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(0.5)
    # mdq = driver.find_element(By.XPATH, '//*[@id="form_busqueda"]/div/div[3]/div[2]/div[1]/div[2]/div/div')
    # time.sleep(2)
    # mdq.click()
    fechaida = driver.find_element(By.XPATH, '//*[@id="form_busqueda"]/div/div[4]/div[1]/div[1]/a/span').click()
    time.sleep(2)
    # monthchange = driver.find_element(By.XPATH, '//*[@id="datepicker-calendar-fecha_ida"]/div[1]/div[2]').click()
    fechita = driver.find_element(By.XPATH, '//*[@id="cell26-fecha_ida"]').click()
    # time.sleep(0.5)
    # fechavuelta = driver.find_element(By.XPATH, '//*[@id="form_busqueda"]/div/div[4]/div[2]/div[1]/a/span').click()
    # time.sleep(0.5)
    # monthchangevuelta = driver.find_element(By.XPATH, '//*[@id="datepicker-calendar-fecha_vuelta"]/div[1]/div[2]').click()
    # monthchangevuelta = driver.find_element(By.XPATH, '//*[@id="datepicker-calendar-fecha_vuelta"]/div[1]/div[2]').click()
    time.sleep(0.5)
    pax_menu = driver.find_element(By.XPATH, '//*[@id="adulto"]').click()
    time.sleep(0.1)
    pax_cant = driver.find_element(By.XPATH, '//*[@id="adulto"]/option[2]').click()
    # vueltita = driver.find_element(By.XPATH, ' //*[@id="cell1-fecha_vuelta"]').click()
    buscar = driver.find_element(By.XPATH, '//*[@id="form_busqueda"]/div/div[7]/div/button').click()


output = "Inicia el loop para no mandar 2 veces el mismo mensaje"
interes = ["SAB 26 FEB"]
# interes_vuelta = ["VIE 25 FEB", "SAB 26 FEB"]

def send_message(message, dia):
    # if output != message and output is not None:
         if dia in interes:
             print("Send Message")
             requests.post('https://api.telegram.org/bot5056598073:AAHyhBvoMRztbzNyLldsDxbNzdqh8iKG8dA/sendMessage',
                       data = {'chat_id' : '@trencitoboti', 'text' : message})
    #         return message
    #    if dia in interes_vuelta:
     #       requests.post('https://api.telegram.org/bot5056598073:AAHyhBvoMRztbzNyLldsDxbNzdqh8iKG8dA/sendMessage',
      #                data = {'chat_id': '@pujolboti', 'text': message})
       #     return message

def send_status():
    requests.post('https://api.telegram.org/bot5056598073:AAHyhBvoMRztbzNyLldsDxbNzdqh8iKG8dA/sendMessage',
                  data={'chat_id': '@trencitobotistatus', 'text': "BOT STATUS: ON"})

def get_days(soup):
    dias = soup.find_all("span", {"class": "dia_numero"})
    calendario_ida = soup.find_all("section", {"class": "calendario ida"})
    asientos_disponibles = soup.find_all("div", {"class": "disponibles"})
    n = soup.find_all("p", {"class": "m-0 cantidad"})
    return [dias, calendario_ida, asientos_disponibles, n]




            # output2 = message
            # return output2
        # else:
            # print("Mensaje ya enviado")


idx = 0


while True:

    send_status()

    # if idx == 10:
    #     send_status()
    #     idx = 0

    driver.get("https://webventas.sofse.gob.ar/")
    time.sleep(2)


    busqueda()


    html = driver.page_source
    html_obj = bs4.BeautifulSoup(html, "html.parser")

    # Busca los dias disponibles
    [dias, calendario_ida, asientos_disponibles, n] = get_days(html_obj)


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
            output = send_message("Para el dia: " + p + " hay: " + num + " disponibles", p)
            print("Para el dia:", p, "hay:", num, "disponibles")
    else:
        output = "NO HAY NADA MOSTRO"
        print(output)

    idx += 1


    time.sleep(2)

#logtest
