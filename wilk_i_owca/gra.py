# laczenie macierzy z grafika - testy
# Zalczenie bibliotek
import numpy as np
import pygame, sys
import math
import json
import time

napis1 = 'Wybierz pozycję wilka: '
napis2 = 'Wybierz owce korzystając z myszki :) '
napis2_1 = 'Nie trafiłeś/aś w owce :)'
napis3 = 'Wybierz w którą strone chcesz sie poruszyć (<-- A , D -->): '
napis4 = 'Wybierz w którą strone chcesz sie poruszyć wilkiem'
napis5 = 'KEYPAD: 7 lewa góra, 9 prawa góra'
napis6 = '1 lewy dół   , 3 prawy dół'
menu1 = 'Nowa gra'
menu2 = 'Statystki'
menu3 = 'Zasady gry'
menu4 = 'Wyjscie z gry'
menu = [menu1, menu2, menu3, menu4]
opis = 'Sterowanie: '
opis1 = 'Wilk - cyfry 1,3,7,9 na klawiaturze KEYPAD.'
opis2 = 'Owca - klawisze: A i D (do poruszenia się w prawo lub w lewo),'
opis3 = '              myszka (wybierając owce którą chce się poruszyć)'

pygame.init()


# Funkcje Programu
#wybierz pozycje startowa wilka
def init(pozycja, stop):
    # wybierz pozycje startowa wilka
    poprawne_dane = False
    start_wilk = pozycja  # miejsce wilka na planszy na poczatku
    if start_wilk == 0 or start_wilk == 2 or start_wilk == 4 or start_wilk == 6:
        poprawne_dane = True
    else:
        stop = 0
        return stop

    if poprawne_dane == True:
        wilk[0] = 7
        wilk[1] = start_wilk
        akt_plansze(wilk, owce, plansza)
        stop = 1
        return stop


def akt_plansze(wilk, owce, plansza):
    for i in range(8):
        for j in range(8):
            plansza[i, j] = 0
    plansza[wilk[0], wilk[1]] = 1
    for i in range(4):
        plansza[owce[i][0], owce[i][1]] = 2


def spr_ruch(poz_x, poz_y, wilk, owce):
    if poz_x > 7 or poz_x < 0:
        return False
    if poz_y > 7 or poz_y < 0:
        return False
    if poz_x == wilk[0] and poz_x == wilk[1]:
        return False
    for i in range(4):
        if poz_x == owce[i][0] and poz_y == owce[i][1]:
            return False

    return True


# wyswietlanie wilka i owcy na planszy
def spr_pozycje(i, j):
    x = j * 100 + 20
    y = i * 100 + 20

    return (x, y)


def wyznaczenie_pozycji_owca(pozycja, strona):
    nr_owcy = pozycja
    kierunek_ruchu = strona

    # Wyznaczamy wsp wybranej pozycji którą będziemy sprawdzać
    if kierunek_ruchu == ("p" or "P"):
        pozx_spr = owce[nr_owcy][0] + 1
        pozy_spr = owce[nr_owcy][1] + 1

    if kierunek_ruchu == ("l" or "L"):
        pozx_spr = owce[nr_owcy][0] + 1
        pozy_spr = owce[nr_owcy][1] - 1
    return pozx_spr, pozy_spr


def wyznaczenie_pozycji_wilka(pozycja):
    kierunek_wilk = pozycja

    if kierunek_wilk == 1:
        pozx_spr = wilk[0] - 1
        pozy_spr = wilk[1] - 1
    if kierunek_wilk == 2:
        pozx_spr = wilk[0] - 1
        pozy_spr = wilk[1] + 1
    if kierunek_wilk == 3:
        pozx_spr = wilk[0] + 1
        pozy_spr = wilk[1] + 1
    if kierunek_wilk == 4:
        pozx_spr = wilk[0] + 1
        pozy_spr = wilk[1] - 1

    return pozx_spr, pozy_spr


def ruch_owca(owce, pozycja):
    nr_owcy = pozycja
    owce[nr_owcy][0] = pozx_spr
    owce[nr_owcy][1] = pozy_spr


def ruch_wilk(wilk, pozx_spr, pozy_spr):
    wilk[0] = pozx_spr
    wilk[1] = pozy_spr

# wykorzystanie funkcji do zakonczenia gry - kto wygral
def sprawdzenie_wilka():
    string = 'wilk'
    if wilk[0] == 0:
        return string
    owce_koniec = 0
    for i in range(4):
        if owce[i][0] == 7:
            owce_koniec = owce_koniec + 1
    if owce_koniec == 4:
        return string


def sprawdzenie_owce():
    string = 'owce'
    if spr_ruch(wilk[0] + 1, wilk[1] + 1, wilk, owce):
        return 0
    elif spr_ruch(wilk[0] + 1, wilk[1] - 1, wilk, owce):
        return 0
    elif spr_ruch(wilk[0] - 1, wilk[1] + 1, wilk, owce):
        return 0
    elif spr_ruch(wilk[0] - 1, wilk[1] - 1, wilk, owce):
        return 0
    else:
        return string


def koniecgry():
    if sprawdzenie_owce() == 'owce' or sprawdzenie_wilka() == 'wilk':
        return 1
    else:
        return 0


def rysowanie_planszy():
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(screen, grey, (0 + j * 200, 0 + i * 200, 100, 100))
            pygame.draw.rect(screen, grey, (100 + j * 200, 100 + i * 200, 100, 100))
            pygame.draw.rect(screen, (0, 0, 0), (100 + j * 200, 0 + i * 200, 100, 100))
            pygame.draw.rect(screen, (0, 0, 0), (0 + j * 200, 100 + i * 200, 100, 100))


def load_screen():
    rysowanie_planszy()

    for i in range(8):
        for j in range(8):
            (x, y) = spr_pozycje(i, j)
            if plansza[i][j] == 2:
                screen.blit(owceImg, (x, y))
            if plansza[i][j] == 1:
                screen.blit(wilkImg, (x, y))
    pygame.display.update()

#wyswietlanie napisow w pygame
def dolny_pasek(napis, napis1, napis2):
    pygame.draw.rect(screen, (250, 250, 250), (0, 800, 800, 200))
    czcionka = pygame.font.SysFont('arial', 20)
    poz_wilka = czcionka.render(napis, 1, (0, 0, 0), None)
    if len(napis1) > 1 or len(napis2) > 1:
        sterowanie = czcionka.render(napis1, 1, (0, 0, 0), None)
        sterowanie1 = czcionka.render(napis2, 1, (0, 0, 0), None)
        screen.blit(sterowanie, (10, 830))
        screen.blit(sterowanie1, (100, 850))
    screen.blit(poz_wilka, (10, 810))
    pygame.display.update()

#umiejscowenie wilka i owiec, liczby na szachownicy
def poczatek_gry():
    czcionka = pygame.font.SysFont('arial', 20)
    for i in range(4):
        plansza[owce[i][0], owce[i][1]] = 2
    dolny_pasek(napis1, '', '')
    load_screen()
    numerek = 0
    for i in range(4):
        numerek += 1
        pozycja_wilka = czcionka.render(str(numerek), 1, (250, 250, 250), None)
        screen.blit(pozycja_wilka, (200 * i + 5, 700))
        pygame.display.update()

#wyswietla gdzie idzie owca, przechwycenie
def wyswietlanie_napisow(litera, x):
    czcionka = pygame.font.SysFont('arial', 20)
    napis = czcionka.render(litera, 1, (0, 0, 0), None)
    screen.blit(napis, (x, 810))
    pygame.display.update()


def bledna_wiadomosc():
    dolny_pasek('', '', '')
    czcionka = pygame.font.SysFont('arial', 20)
    napis = czcionka.render("Błędne dane, spróbuj jeszcze raz ;)", 1, (0, 0, 0), None)
    screen.blit(napis, (220, 810))

    pygame.display.update()
    fpsClock.tick(FPS)

#funkcja do umiejscowienia wilka na poczatku gry
def zdarzenia_klawiatura_poczatek(litera, pozycja, pozycja_x, poprawne, napis):
    if event.key == pygame.K_KP1:
        pozycja = 0
        litera = '1'
        pozycja_x += 10
    if event.key == pygame.K_KP2:
        pozycja = 2
        litera = '2'
        pozycja_x += 10
    if event.key == pygame.K_KP3:
        pozycja = 4
        litera = '3'
        pozycja_x += 10
    if event.key == pygame.K_KP4:
        pozycja = 6
        litera = '4'
        pozycja_x += 10
    if event.key == pygame.K_KP_ENTER:
        if pozycja_x == 220:
            poprawne = 1
        else:
            litera = ''
            pozycja_x = 210
            bledna_wiadomosc()
            dolny_pasek(napis, '', '')

    if event.key == pygame.K_BACKSPACE:
        litera = ''
        pozycja_x = 210
        dolny_pasek(napis, '', '')
    return litera, pozycja, pozycja_x, poprawne

#pozycja myszki xy i czy jest tam gdzie owca
def wybor_myszka():
    pos = pygame.mouse.get_pos()
    (x, y) = pos
    for i in range(4):
        for j in range(4):
            if x > 100 + j * 200 and x < 200 + j * 200:
                if y > i * 200 and y < 100 + i * 200:
                    return dostosowanie_pozycji(x, y)
            if x > j * 200 and x < 100 + j * 200:
                if y > 100 + i * 200 and y < 200 + i * 200:
                    return dostosowanie_pozycji(x, y)

#z pikseli na macierz pozycje owcy
def dostosowanie_pozycji(x, y):
    planszax = math.floor(x / 100)
    planszay = math.floor(y / 100)
    for i in range(4):
        if planszay == owce[i][0] and planszax == owce[i][1]:
            nr_owcy = i
            return nr_owcy


def zdarzenia_klawiatura_owca_strona(litera, pozycja_x, poprawne, strona, napis):
    if event.key == pygame.K_a:
        strona = 'l'
        litera = 'A'
        poprawne = 1
        pozycja_x += 10
    if event.key == pygame.K_d:
        strona = 'p'
        litera = 'D'
        poprawne = 1
        pozycja_x += 10
    if event.key != pygame.K_a and event.key != pygame.K_d and event.key != pygame.K_ESCAPE:
        litera = ''
        pozycja_x = 210
        bledna_wiadomosc()
        dolny_pasek(napis, '', '')

    return litera, pozycja_x, poprawne, strona


def zdarzenia_klawiatura_wilk(litera, pozycja, pozycja_x, poprawne):
    if event.key == pygame.K_KP7:
        pozycja = 1
        poprawne = 1
        litera = ''
    if event.key == pygame.K_KP9:
        pozycja = 2
        poprawne = 1
        litera = ''
    if event.key == pygame.K_KP3:
        pozycja = 3
        poprawne = 1
        litera = ''
    if event.key == pygame.K_KP1:
        pozycja = 4
        poprawne = 1
        litera = ''

    return litera, pozycja, pozycja_x, poprawne

#wyswietlanie owiec oprocz jednej ktora jest poruszana jako animacja
def load_screen_animacja(zwierze_x, zwierze_y):
    rysowanie_planszy()
    for i in range(8):
        for j in range(8):
            if i != zwierze_x or j != zwierze_y:
                (x, y) = spr_pozycje(i, j)
                if plansza[i][j] == 2:
                    screen.blit(owceImg, (x, y))
                if plansza[i][j] == 1:
                    screen.blit(wilkImg, (x, y))
    pygame.display.update()


def animacja_owca(pozycja, strona):
    (x, y) = spr_pozycje(owce[pozycja][0], owce[pozycja][1]) #piksele gdzie owca jest
    if strona == 'l':
        z = x - 100
        w = y + 100
        while x > z and y < w:
            x -= 2
            y += 2
            load_screen_animacja(owce[pozycja][0], owce[pozycja][1]) #wybranie owcy ktora sie porusza
            screen.blit(owceImg, (x, y))
            pygame.display.update()
            fpsClock.tick(90)
    if strona == 'p':
        z = x + 100
        w = y + 100
        while x < z and y < w:
            x += 2
            y += 2
            load_screen_animacja(owce[pozycja][0], owce[pozycja][1])
            screen.blit(owceImg, (x, y))
            pygame.display.update()
            fpsClock.tick(90)


def animacja_wilk(pozycja):
    (x, y) = spr_pozycje(wilk[0], wilk[1])
    if pozycja == 1:
        z = x - 100
        w = y - 100
        while x > z and y > w:
            x -= 2
            y -= 2
            load_screen_animacja(wilk[0], wilk[1])
            screen.blit(wilkImg, (x, y))
            pygame.display.update()
            fpsClock.tick(90)
    if pozycja == 2:
        z = x + 100
        w = y - 100
        while x < z and y > w:
            x += 2
            y -= 2
            load_screen_animacja(wilk[0], wilk[1])
            screen.blit(wilkImg, (x, y))
            pygame.display.update()
            fpsClock.tick(90)
    if pozycja == 3:
        z = x + 100
        w = y + 100
        while x < z and y < w:
            x += 2
            y += 2
            load_screen_animacja(wilk[0], wilk[1])
            screen.blit(wilkImg, (x, y))
            pygame.display.update()
            fpsClock.tick(90)
    if pozycja == 4:
        z = x - 100
        w = y + 100
        while x > z and y < w:
            x -= 2
            y += 2
            load_screen_animacja(wilk[0], wilk[1])
            screen.blit(wilkImg, (x, y))
            pygame.display.update()
            fpsClock.tick(90)

#statystyki, otwiera plik i wczytuje do pythona
def wczytanie_json(lista):
    with open('statystyki.txt') as json_file:
        lista = json.load(json_file)
    return lista

#tworzenie slownikow, lista i nadpisanie pliku
def statystyki(m, d, h, zwyciezca):
    lista = []
    data = {'miesiac': m, 'dzien': d, 'godzina': h}
    dane = {'wygrana': zwyciezca, 'data': data}
    lista = wczytanie_json(lista)
    lista.append(dane)
    with open('statystyki.txt', 'w') as outfile:
        json.dump(lista, outfile)


def menu_statystyki():
    lista = []
    miejsce = 0
    czcionka = pygame.font.SysFont('arial', 50)
    czcionka1 = pygame.font.SysFont('arial', 30)
    pygame.draw.rect(screen, (0, 0, 0), (0, 800, 800, 100))
    pygame.draw.rect(screen, grey, (0, 0, 800, 800))
    napis1 = czcionka.render('Statystyki', 1, (0, 0, 0))
    screen.blit(napis1, (10, 10))
    lista = wczytanie_json(lista)
    for i in range(len(lista) - 1, -1, -1):
        if i < 10:
            napis = czcionka1.render(str(miejsce + 1) + '. Wygrał: ' + str(lista[i]['wygrana']) + ', w dniu: ' + str(
                lista[i]['data']['miesiac'] + '.' + lista[i]['data']['dzien'] + '.' + lista[i]['data']['godzina']), 1,
                                     (250, 250, 250))
            screen.blit(napis, (10, 90 + 40 * miejsce))
            miejsce += 1

    pygame.display.update()

#wypisuje
def zasady_gry(opis1, i):
    czcionka = pygame.font.SysFont('arial', 20)
    opis = czcionka.render(opis1, 1, (250, 250, 250))
    screen.blit(opis, (20, 20 + 30 * i))
    pygame.display.update()


def napis_zasady_gry():
    zasady_gry(opis, 0)
    zasady_gry(opis1, 2)
    zasady_gry(opis2, 3)
    zasady_gry(opis3, 4)
    plik = open('zasady_gry.txt')
    napis_zasady = plik.read().split('\n')
    for i in range(len(napis_zasady)):
        zasady_gry(napis_zasady[i], 6 + i)
    plik.close()


def menu_napis():
    pygame.draw.rect(screen, (0, 0, 0), (0, 800, 800, 100))
    pygame.draw.rect(screen, grey, (0, 0, 800, 800))
    czcionka = pygame.font.SysFont('arial', 20)
    czcionka1 = pygame.font.SysFont('arial', 40)
    tytul = czcionka.render('GRA WILK I OWCE', 1, (250, 250, 250))
    menu_gra = czcionka1.render('MENU', 1, (0, 0, 0))
    screen.blit(menu_gra, (300, 160))
    screen.blit(tytul, (300, 830))
    for i in range(4):
        menu_napis = czcionka.render(str(i + 1) + '. ' + menu[i], 1, (250, 250, 250), None)
        screen.blit(menu_napis, (300, 220 + i * 30))
    pygame.display.update()

#ustawia owce i wilka, dla nowej gry
def inicjalizacja_planszy():
    # Macierze pozycji owiec i wilka
    wilk = [7, 0]
    owce = np.array([[0, 1], [0, 3], [0, 5], [0, 7]])
    # Macierz planszy wypełnionej pionkami 0 - puste miejsca; 1- wilk ; 2 - owce
    plansza = np.zeros((8, 8), int)
    return wilk, owce, plansza


# -----------------PROGRAM---------------

# kolor planszy
grey = (128, 128, 128)

# okno, tytul, ikonka
screen = pygame.display.set_mode((800, 900))
pygame.display.set_caption('Wilk i Owce')
icon = pygame.image.load('pawprint.png')
pygame.display.set_icon(icon)
# obraz wilka i owcy
owceImg = pygame.image.load('lamb.png')
wilkImg = pygame.image.load('wolf.png')

# PRZYDATNE ZMIENNE

wyjscie_z_gry = 0
wyjscie = 0
menu_petla = 0
stop = 0
gra_owca_pozycja = 0
gra_wilk = 0
gra_owca_strona = 0
litera = ''
strona = ''
wilk_pozycja = 0
pozycja = 1
poprawne = 0
pozycja_x = 210
FPS = 0.2
fpsClock = pygame.time.Clock()
while True:
    wilk, owce, plansza = inicjalizacja_planszy()
    while menu_petla != 1:
        menu_napis()
        gra_owca_pozycja = 0
        gra_wilk = 0
        gra_owca_strona = 0
        stop = 0
        poprawne = 0
        wyjscie_z_gry = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    menu_petla = 1
                if event.key == pygame.K_2:
                    while wyjscie != 1:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                wyjscie = 1
                        menu_statystyki()
                    wyjscie = 0
                if event.key == pygame.K_3:
                    pygame.draw.rect(screen, grey, (0, 0, 800, 800))
                    i = 0
                    while wyjscie != 1:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                wyjscie = 1
                        if i == 0:
                            napis_zasady_gry()
                            i = 1

                    wyjscie = 0
                if event.key == pygame.K_4:
                    pygame.quit()
                    sys.exit()

    poczatek_gry()
    # Poczatek gry - ustawienie
    while stop != 1:
        while poprawne != 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    stop = 1
                    poprawne = 1
                    wyjscie_z_gry = 1
                    menu_petla = 0
                if event.type == pygame.KEYDOWN:
                    (litera, pozycja, pozycja_x, poprawne) = zdarzenia_klawiatura_poczatek(litera, pozycja, pozycja_x,
                                                                                           poprawne, napis1)
                    wyswietlanie_napisow(litera, pozycja_x)
        if wyjscie_z_gry != 1:
            stop = init(pozycja, stop)

    while wyjscie_z_gry != 1:
        load_screen()

        # RUCHY OWIEC
        litera = ''
        pozycja_x = 210
        dolny_pasek(napis2, '', '')
        if gra_owca_pozycja == 0:
            while gra_owca_pozycja != 1: #ktora owca wybrac
                gra_wilk = 0
                gra_owca_strona = 0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        gra_owca_pozycja = 1
                        gra_owca_strona = 1
                        gra_wilk = 1
                        wyjscie_z_gry = 1
                        menu_petla = 0
                    if event.type == pygame.MOUSEBUTTONUP:
                        pozycja = wybor_myszka()
                        if pozycja == None:
                            dolny_pasek(napis2, napis2_1, '')
                            pygame.display.update()
                            fpsClock.tick(0.2)
                            dolny_pasek(napis2, '', '')
                        else:
                            gra_owca_pozycja = 1

            litera = ''
            pozycja_x = 210
            dolny_pasek(napis3, '', '')
            while gra_owca_strona != 1:#gdzie idzie
                gra_owca_pozycja = 0
                gra_wilk = 0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        gra_owca_pozycja = 1
                        gra_owca_strona = 1
                        gra_wilk = 1
                        wyjscie_z_gry = 1
                        menu_petla = 0
                    if event.type == pygame.KEYDOWN:
                        (litera, pozycja_x, gra_owca_strona, strona) = zdarzenia_klawiatura_owca_strona(litera,
                                                                                                        pozycja_x,
                                                                                                        gra_owca_strona,
                                                                                                        strona, napis3)
                        wyswietlanie_napisow(litera, pozycja_x + 310)

            if wyjscie_z_gry != 1:
                (pozx_spr, pozy_spr) = wyznaczenie_pozycji_owca(pozycja, strona)#ktore miejsce, mozliwy ruch i animacje
                if spr_ruch(pozx_spr, pozy_spr, wilk, owce):
                    animacja_owca(pozycja, strona)
                    status_ruch = ruch_owca(owce, pozycja)#ruch owcy, macierze
                else:
                    gra_wilk = 1

        # ------------

        akt_plansze(wilk, owce, plansza)
        load_screen()
        pygame.display.update()
        if wyjscie_z_gry == 0:
            wyjscie_z_gry = koniecgry()
            if wyjscie_z_gry == 1:

                if sprawdzenie_owce() == 'owce':
                    zwyciezca = 'owce'
                elif sprawdzenie_wilka() == 'wilk':
                    zwyciezca = 'wilk'
                miesiac = time.strftime("%m")
                dzien = time.strftime("%d")
                godzina = time.strftime("%H:%M")
                statystyki(miesiac, dzien, godzina, zwyciezca)
                menu_petla = 0

        # RUCHY WILKA
        pozycja_x = 210
        dolny_pasek(napis4, napis5, napis6)
        if gra_wilk == 0 and wyjscie_z_gry == 0:
            while gra_wilk != 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        gra_wilk = 1
                        wyjscie_z_gry = 1
                        menu_petla = 0
                    if event.type == pygame.KEYDOWN:
                        (litera, pozycja_wilk, pozycja_x, gra_wilk) = zdarzenia_klawiatura_wilk(litera, pozycja,
                                                                                                pozycja_x,
                                                                                                gra_wilk)
            if wyjscie_z_gry != 1:
                (pozx_spr, pozy_spr) = wyznaczenie_pozycji_wilka(pozycja_wilk)
                if spr_ruch(pozx_spr, pozy_spr, wilk, owce):
                    animacja_wilk(pozycja_wilk)
                    status_ruch = ruch_wilk(wilk, pozx_spr, pozy_spr)
                    gra_owca_pozycja = 0
                else:
                    gra_owca_pozycja = 1
                    gra_wilk = 0

        # ------------

        akt_plansze(wilk, owce, plansza)
        pygame.display.update()
        if wyjscie_z_gry == 0:
            wyjscie_z_gry = koniecgry()
            if wyjscie_z_gry == 1:

                if sprawdzenie_owce() == 'owce':
                    zwyciezca = 'owce'
                elif sprawdzenie_wilka() == 'wilk':
                    zwyciezca = 'wilk'
                miesiac = time.strftime("%m")
                dzien = time.strftime("%d")
                godzina = time.strftime("%H:%M")
                statystyki(miesiac, dzien, godzina, zwyciezca)
                menu_petla = 0
