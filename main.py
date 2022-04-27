from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from difflib import SequenceMatcher
import unidecode

s = Service('D:\chromedriver\chromedriver.exe')
driver = webdriver.Chrome(service=s)


def scrap_casapariurilor(driver, teams_list, cote_list, url):
    driver.get(url)
    driver.maximize_window()
    ascunde = driver.find_element(By.XPATH, '//*[@id="checkbox_live_disabled"]')
    ascunde.click()
    time.sleep(2)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1300);")

        # Wait to load page
        time.sleep(1)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight-1300")
        if new_height == last_height:
            break
        last_height = new_height

    teams = driver.find_elements(By.XPATH, '//*[@class="market-name"]')

    for t in range(len(teams)):
        teams_list.append(teams[t].text)

    cote = driver.find_elements(By.XPATH, '//*[@class="odds-value"]')
    lista_cote = []
    for c in cote:
        lista_cote.append(c.text)

    # while "" in lista_cote:
    #     lista_cote.remove("")

    #
    # for c in lista_cote:
    #     cote_list.append(c)

    c = 0
    while c < len(lista_cote):
        while (lista_cote[c] == "" and c < len(lista_cote) - 1):
            c = c + 1
        cote_list.append(lista_cote[c])
        c = c + 1
        if (len(cote_list) % 3 == 0):
            c = c + 3


def scrap_betano(driver, teams_list, cote_list, url):
    driver.get(url)
    # driver.maximize_window()

    time.sleep(1)
    accept = driver.find_element(By.XPATH, '//*[@id="landing-page-modal"]/div/div[1]/button')
    accept.click()
    time.sleep(1)
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1500);")

        # Wait to load page
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight-1500")
        if new_height == last_height:
            break
        last_height = new_height

    teams = driver.find_elements(By.XPATH, '//*[@class="events-list__grid__event"]')

    lista = []
    for t in teams:
        lista.append(unidecode.unidecode(t.get_attribute("textContent")).splitlines())

    for l in lista:
        teams_list.append(l[5].strip() + " - " + l[7].strip())
        # if(len(l)==21):
        #     cote_list.append(l[15].strip())
        #     cote_list.append(l[17].strip())
        #     cote_list.append(l[19].strip())
        #
        # elif(len(l)==19):
        cote_list.append(l[13].strip())
        cote_list.append(l[15].strip())
        cote_list.append(l[17].strip())
        # else:
        #     cote_list.append(1)
        #     cote_list.append(1)
        #     cote_list.append(1)

    # teams=driver.find_elements(By.XPATH,'//*[@class="events-list__grid__info__main__participants__name"]')
    # for t in range(len(teams)):
    #     if t%2==0:
    #         teams_list.append(unidecode.unidecode(" ".join(teams[t].get_attribute('textContent').split())+" - "+" ".join(teams[t+1].get_attribute('textContent').split())))
    #
    #
    # cote=driver.find_elements(By.XPATH,'//*[@class="selections__selection selections__selection--columns-4 GTM-selection-add"]')
    #
    # for c in range(len(cote)):
    #         cote_list.append(cote[c].get_attribute('textContent').strip().replace("1  \n","").replace("X  \n","").replace("2  \n","").replace("\n","").strip())


def scrap_superbet(driver, teams_list, cote_list, url):
    driver.get(url)
    # driver.maximize_window()
    time.sleep(3)

    last_height = driver.execute_script("return document.body.scrollHeight")
    height = 2000

    while True:
        lista2 = []
        lista = driver.find_elements(By.XPATH, '//*[@class="event-row-container"]')

        for i in range(len(lista)):
            lista2.append(unidecode.unidecode(lista[i].text).splitlines())
        for i in lista2:
            if i[2] + " - " + i[3] not in teams_list:
                if (len(i) < 11):
                    teams_list.append(i[2] + " - " + i[3])
                    cote_list.append(1)
                    cote_list.append(1)
                    cote_list.append(1)

                else:
                    teams_list.append(i[2] + " - " + i[3])
                    cote_list.append(i[6])
                    cote_list.append(i[8])
                    cote_list.append(i[10])

        driver.execute_script("window.scrollBy(0,2000);")
        time.sleep(1)

        if height > last_height:
            break
        height = height + 2000


def scrap_netbet(driver, teams_list, cote_list, url):
    driver.get(url)
    driver.maximize_window()

    time.sleep(5)
    tip_cote = driver.find_element(By.XPATH, '//*[@class="page-header-dropdown-wrap page-header-dropdown-odds"]')
    tip_cote.click()
    cota_zecimala = driver.find_element(By.XPATH, '//*[@id="odd_style_1"]')
    cota_zecimala.click()

    colapse = driver.find_elements(By.XPATH, '//*[@class="rj-instant-collapsible__trigger"]')

    lista_colapse = []
    for c in colapse:
        lista_colapse.append(c.text)

    for i in range(0, 3):
        if (i + 1 > len(lista_colapse)):
            break
        colapse[i].click()
        time.sleep(0.1)

    box = driver.find_element(By.CLASS_NAME, 'rj-ev-list__content')
    colapse = box.find_elements(By.CLASS_NAME, 'rj-instant-collapsible__trigger')

    lista2 = []
    for c in colapse:
        driver.execute_script("arguments[0].scrollIntoView(true);", c)
        c.click()
        teams = driver.find_elements(By.XPATH, '//*[@class="rj-ev-list__ev-card__inner"]')
        time.sleep(0.1)
        for t in teams:
            lista2.append(t.text.splitlines())
        c.click()

    for i in lista2:
        teams_list.append(unidecode.unidecode(i[0]) + " - " + unidecode.unidecode(i[1]))
        cote_list.append(i[4])
        cote_list.append(i[5])
        cote_list.append(i[6])


def scrap_netbet_liga(driver, teams_list, cote_list, url):
    driver.get(url)
    driver.maximize_window()

    time.sleep(2)
    tip_cote = driver.find_element(By.XPATH, '//*[@class="page-header-dropdown-wrap page-header-dropdown-odds"]')
    tip_cote.click()
    cota_zecimala = driver.find_element(By.XPATH, '//*[@id="odd_style_1"]')
    cota_zecimala.click()

    box = driver.find_element(By.ID, 'eventsWrapper-Center_LeagueViewResponsiveBlock_30336')
    colapse = box.find_elements(By.CLASS_NAME, 'rj-instant-collapsible__trigger')
    lista2 = []
    for c in colapse:
        driver.execute_script("arguments[0].scrollIntoView(true);", c)
        time.sleep(1)
        teams = driver.find_elements(By.XPATH, '//*[@class="rj-ev-list__ev-card__inner"]')
        for t in teams:
            lista2.append(t.text.splitlines())

    for l in lista2:
        if (l[0] + " - " + l[1]) not in teams_list:
            teams_list.append(l[0] + " - " + l[1])
            cote_list.append(l[5])
            cote_list.append(l[7])
            cote_list.append(l[9])


def scrap_betfair(driver, teams_list, cote_list, url):
    driver.get(url)
    # driver.maximize_window()

    time.sleep(3)
    teams = driver.find_elements(By.XPATH, '//*[@class="team-name"]')

    for t in range(len(teams)):
        if t % 2 == 0:
            teams_list.append(unidecode.unidecode(
                " ".join(teams[t].get_attribute('textContent').split()) + " - " + " ".join(
                    teams[t + 1].get_attribute('textContent').split())))

    cote = driver.find_elements(By.XPATH, '//*[@class="details-market market-3-runners"]')
    for c in range(len(cote)):
        cote_list.append(" ".join(cote[c].get_attribute('textContent').replace("Suspendat", "1").split()).split())

    for c in range(len(cote_list)):
        while (len(cote_list[c]) < 3):
            cote_list[c].append("1")


def scrap_unibet(driver, teams_list, cote_list, url):
    driver.get(url)
    # driver.maximize_window()

    time.sleep(2)
    try:
        accept = driver.find_element(By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')
        accept.click()
        time.sleep(1)
    except:
        print("")

    ligi = driver.find_elements(By.XPATH, '//*[@data-test-name="accordionLevel1"]')
    for l in ligi:
        l.click()

    teams = driver.find_elements(By.XPATH, '//*[@data-test-name="event"]')
    lista2 = []
    for t in teams:
        lista2.append(unidecode.unidecode(t.text).splitlines())

    print(lista2)

    for l in lista2:
        if (l[1] + " - " + l[2]) not in teams_list and len(l) == 11:
            teams_list.append(l[1] + " - " + l[2])
            cote_list.append(l[3])
            cote_list.append(l[4])
            cote_list.append(l[5])
        if (l[1] + " - " + l[2]) not in teams_list and len(l) == 11:
            teams_list.append(l[1] + " - " + l[2])
            cote_list.append(l[5])
            cote_list.append(l[6])
            cote_list.append(l[7])

    # colapse=driver.find_elements(By.XPATH,'//*[@data-test-name="accordionLevel1"]')
    #
    #
    # for c in colapse:
    #     c.click()

    # colapse=driver.find_elements(By.XPATH,'//*[@data-test-name="accordionLevel2"]')
    # for c in colapse:
    #     print(c.get_attribute('textContent'))
    #     #driver.execute_script("arguments[0].scrollIntoView(true);",c)
    #     time.sleep(3)
    #     c.click()
    # teams=driver.find_elements(By.XPATH,'//*[@data-test-name="teamName"]')
    # for t in teams:
    #     print(unidecode.unidecode(t.get_attribute('textContent')))


def creeaza_lista_meciuri_casa(lista_meciuri, teams_list, cote_list, nume_casa):
    lista_meci = []
    c = 0
    for t in teams_list:
        lista_meci.append(t)
        for _ in range(3):
            lista_meci.append(cote_list[c])
            c = c + 1
        lista_meci.append(nume_casa)
        lista_meci.append(nume_casa)
        lista_meci.append(nume_casa)
        lista_meciuri.append(lista_meci[0:7])
        lista_meci.clear()


def creeaza_lista_meciuri_betfair(lista_meciuri, teams_list, cote_list, nume_casa):
    lista_meci = []
    c = 0
    for t in teams_list:
        lista_meci.append(t)
        for i in range(3):
            lista_meci.append(cote_list[c][i])
        c = c + 1
        lista_meci.append(nume_casa)
        lista_meci.append(nume_casa)
        lista_meci.append(nume_casa)
        lista_meciuri.append(lista_meci[0:7])
        lista_meci.clear()


def creeaza_lista_meciuri_superbet(lista_meciuri, teams_list, cote_list, nume_casa):
    lista_meci = []
    c = 0
    for t in teams_list:
        lista_meci.append(t)
        for _ in range(3):
            lista_meci.append(cote_list[c])
            c = c + 1
        lista_meci.append(nume_casa)
        lista_meci.append(nume_casa)
        lista_meci.append(nume_casa)
        lista_meciuri.append(lista_meci[0:7])
        lista_meci.clear()


def creeaza_lista_meciuri_netbet(lista_meciuri, teams_list, cote_list, nume_casa):
    lista_meci = []
    c = 0
    for t in teams_list:
        lista_meci.append(t)
        for _ in range(3):
            lista_meci.append(cote_list[c])
            c = c + 1
        lista_meci.append(nume_casa)
        lista_meci.append(nume_casa)
        lista_meci.append(nume_casa)
        lista_meciuri.append(lista_meci[0:7])
        lista_meci.clear()


def creeaza_lista_meciuri_betano(lista_meciuri, teams_list, cote_list, nume_casa):
    lista_meci = []
    c = 0
    for t in range(len(teams_list)):
        lista_meci.append(teams_list[t])
        for _ in range(3):
            lista_meci.append(cote_list[c])
            c = c + 1
        lista_meci.append(nume_casa)
        lista_meci.append(nume_casa)
        lista_meci.append(nume_casa)
        lista_meciuri.append(lista_meci[0:7])
        lista_meci.clear()


def max_cote(lista_meciuri, lista_finala):
    for i in lista_meciuri:
        listameci = i[:]
        for j in lista_meciuri:
            if SequenceMatcher(None, listameci[0], j[0]).ratio() > 0.65:
                if float(listameci[1]) < float(j[1]):
                    listameci[1] = j[1]
                    listameci[4] = j[4]
                if (float(listameci[1]) == float(j[1])):
                    listameci[4] = listameci[4] + " " + j[4]

                if float(listameci[2]) < float(j[2]):
                    listameci[2] = j[2]
                    listameci[5] = j[5]
                if (float(listameci[2]) == float(j[2])):
                    listameci[5] = listameci[5] + " " + j[5]

                if float(listameci[3]) < float(j[3]):
                    listameci[3] = j[3]
                    listameci[6] = j[6]
                if (float(listameci[3]) == float(j[3])):
                    listameci[6] = listameci[6] + " " + j[6]

                if (1 / float(listameci[1]) + 1 / float(listameci[2]) + 1 / float(listameci[3])) * 100 < 99 and (
                        1 / float(listameci[1]) + 1 / float(listameci[2]) + 1 / float(listameci[3])) * 100 > 97:
                    print(listameci)
                    print((1 / float(listameci[1]) + 1 / float(listameci[2]) + 1 / float(listameci[3])) * 100)
                    print('\n\n')

        # lista_finala.append(listameci[:])


def gaseste(listabuna):
    for i in listabuna:
        if (1 / float(i[1]) + 1 / float(i[2]) + 1 / float(i[3])) * 100 < 100:
            print(i)
            print((1 / float(i[1]) + 1 / float(i[2]) + 1 / float(i[3])) * 100)
            print('\n')


# CASA
#####################################################################################################################################
lista_casa = []
teams_casa = []
cote_casa = []


def creeaza_lista_casa(url):
    scrap_casapariurilor(driver, teams_casa, cote_casa, url)
    creeaza_lista_meciuri_casa(lista_casa, teams_casa, cote_casa, "casa")

    print(teams_casa)
    print(cote_casa)
    print(lista_casa)
    print('\n\n')


#####################################################################################################################################


# BETANO
#####################################################################################################################################
lista_betano = []
teams_betano = []
cote_betano = []


def creeaza_lista_betano(url):
    scrap_betano(driver, teams_betano, cote_betano, url)
    creeaza_lista_meciuri_betano(lista_betano, teams_betano, cote_betano, "betano")

    print(teams_betano)
    print(cote_betano)
    print(lista_betano)
    print('\n\n')


#####################################################################################################################################


# SUPERBET
#####################################################################################################################################
lista_superbet = []
teams_superbet = []
cote_superbet = []


def creeaza_lista_superbet(url):
    scrap_superbet(driver, teams_superbet, cote_superbet, url)
    creeaza_lista_meciuri_superbet(lista_superbet, teams_superbet, cote_superbet, "superbet")

    print(teams_superbet)
    print(cote_superbet)
    print(lista_superbet)
    print('\n\n')


#####################################################################################################################################


# BETFAIR
#####################################################################################################################################
lista_betfair = []
teams_betfair = []
cote_betfair = []


def creeaza_lista_betfair(url):
    scrap_betfair(driver, teams_betfair, cote_betfair, url)
    creeaza_lista_meciuri_betfair(lista_betfair, teams_betfair, cote_betfair, "betfair")

    print(teams_betfair)
    print(cote_betfair)
    print(lista_betfair)
    print('\n\n')


#####################################################################################################################################


# NETBET
#####################################################################################################################################
lista_netbet = []
teams_netbet = []
cote_netbet = []


def creeaza_lista_netbet(url):
    scrap_netbet(driver, teams_netbet, cote_netbet, url)
    # scrap_netbet_liga(driver,teams_netbet,cote_netbet,url)

    creeaza_lista_meciuri_netbet(lista_netbet, teams_netbet, cote_netbet, "netbet")

    print(teams_netbet)
    print(cote_netbet)
    print(lista_netbet)
    print('\n\n')


#####################################################################################################################################


# UNIBET
#####################################################################################################################################
lista_unibet = []
teams_unibet = []
cote_unibet = []


def creeaza_lista_unibet(url):
    scrap_unibet(driver, teams_unibet, cote_unibet, url)
    creeaza_lista_meciuri_netbet(lista_unibet, teams_unibet, cote_unibet, "unibet")

    print(teams_unibet)
    print(cote_unibet)
    print(lista_unibet)
    print('\n\n')


#####################################################################################################################################


# LISTA CARE CONTINE MECIURILE DE PE TOATE CASELE
#####################################################################################################################################
lista_meciuri = []


def creeaza_lista_toate_meciuri():
    for l in lista_casa:
        lista_meciuri.append(l)

    for l in lista_betano:
        lista_meciuri.append(l)

    for l in lista_superbet:
        lista_meciuri.append(l)

    for l in lista_betfair:
        lista_meciuri.append(l)

    for l in lista_netbet:
        lista_meciuri.append(l)

    for l in lista_unibet:
        lista_meciuri.append(l)

    for i in lista_meciuri:
        print(i)
    print('\n\n')


#####################################################################################################################################


# LISTA CARE CONTINE MECIURILE CU COTELE MAXIME
#####################################################################################################################################
lista_cote_max = []


def creeaza_lista_cote_max():
    max_cote(lista_meciuri, lista_cote_max)


#####################################################################################################################################


# LISTA CARE CONTINE MECIURI SIGURE
#####################################################################################################################################
def creeaza_lista_meciuri_sigure():
    gaseste(lista_cote_max)


#####################################################################################################################################


# MAIN
#####################################################################################################################################
creeaza_lista_betano("https://ro.betano.com/sport/fotbal/meciurile-urmatoare-de-azi/")
creeaza_lista_casa("https://www.casapariurilor.ro/pariuri-online/fotbal?date=2022-04-27")
creeaza_lista_superbet("https://superbet.ro/pariuri-sportive/fotbal/astazi")
creeaza_lista_betfair("https://www.betfair.ro/sport/football")
creeaza_lista_netbet("https://sport.netbet.ro/fotbal/")
# creeaza_lista_unibet("https://www.unibet.ro/betting/sports/filter/football/all/matches")
creeaza_lista_toate_meciuri()
creeaza_lista_cote_max()

# creeaza_lista_meciuri_sigure()
# ####################################################################################################################################



