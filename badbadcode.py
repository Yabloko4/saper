import sys  # sys нужен для передачи argv в QApplication
import os
#from tkinter.tix import TEXT  # Отсюда нам понадобятся методы для отображения содержимого директорий

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap

import design  # Это наш конвертированный файл дизайна
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains

options = Options()
options.add_experimental_option("detach", True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
actionChains = ActionChains(driver)


driver.get("https://minesweeper.online/ru/new-game/ng")
#https://minesweeper.online/ru/start/1
#https://minesweeper.online/ru/new-game/ng
#top-area-face zoomable hd_top-area-face-unpressed
#top-area-face zoomable hd_top-area-face-win
#top-area-face zoomable hd_top-area-face-lose
      
wincount = 0
losecount =0
isnt_finished = 0
for lol in range(20):
    i = 9 #строки
    j = 9 #столбцы  
    start_is_clicked = False   
    mas = [0] * 9 
    for i in range(9): 
            mas[i] = [0] * 9 
    driver.implicitly_wait(5)
    time.sleep(2)
    list_of_right_clicks = []
    list_of_left_clicks = []
    row = 0
    column = 0
    id = 1
    for hz in range(0,2):
        for row in range(0,9):
            if (start_is_clicked == True):
                start_is_clicked = False
                break
            print("новая строка")
            for column in range(0,9):
                str = (f'//*[@id="cell_{column}_{row}"]')
                cell = driver.find_element(By.XPATH, str)
                if hz == 1:
                    mas[row][column] = f'{id} {cell.get_attribute("class")}'
                    id += 1
                #mas[j][row] = cell.get_attribute
                #print(cell.get_attribute("class"))
                #print(f'column = {column}, row = {row}')
                if (cell.get_attribute("class") == "cell size24 hd_closed start"):
                    mas[row][column] = {cell.get_attribute("class")}
                    cell.click()
                    if row != 8:
                        start_is_clicked = True
                        break
    fake_mas = [0] * 9 
    for i in range(9): 
        fake_mas[i] = [0] * 9

    #print(len(mas[0][0]))
    def update_fake_mas():
        global id
        for row in range(9):
            for column in range(9):
                if mas[row][column].find('cell size24 hd_closed') != -1:
                    fake_mas[row][column]= '-9'
                if mas[row][column].find('cell size24 hd_opened hd_type0') != -1:
                    fake_mas[row][column]= '0'
                if mas[row][column].find('cell size24 hd_opened hd_type1') != -1:
                    fake_mas[row][column]= '1'
                if mas[row][column].find('cell size24 hd_opened hd_type2') != -1:
                    fake_mas[row][column]= '2'
                if mas[row][column].find('cell size24 hd_opened hd_type3') != -1:
                    fake_mas[row][column]= '3'
                if mas[row][column].find('cell size24 hd_opened hd_type4') != -1:
                    fake_mas[row][column]= '4'
                if mas[row][column].find('cell size24 hd_opened hd_type5') != -1:
                    fake_mas[row][column]= '5'
                if mas[row][column].find('cell size24 hd_closed hd_flag') != -1:
                    fake_mas[row][column]= 'f'
                id += 1
    update_fake_mas()
    for row in fake_mas:
        print(*row)
    
    def set_flags(list_of_right_clicks):
            for item in list_of_right_clicks:
                    cell = driver.find_element(By.XPATH, item)
                    if cell.get_attribute("class") != 'cell size24 hd_closed hd_flag':
                        actionChains.context_click(cell).perform()
    
    def search_for_flags(fake_mas:list):
        list_of_right_clicks = []
        count = 0
        offsetList = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
        xIndex,yIndex = 0,0
        for row in fake_mas:
            for column in row:
                for offset in offsetList:
                    if yIndex + offset[0] >= 0 and xIndex + offset[1] >=0 and yIndex + offset[0] <= len(fake_mas) - 1 and xIndex + offset[1] <= len(row) - 1 : # первый and проверка на отрицательность смещённых индексов, что бы не получать значения с конца. Третий and для определения вышли мы за предел листа и если вышли то пропускаем такое смещение
                        if fake_mas[xIndex + offset[1]][yIndex + offset[0]] == "-9":
                            count +=1
                            coordinates_of_flags = (f'//*[@id="cell_{[yIndex + offset[0]]}_{[xIndex + offset[1]]}"]')
                            list_of_right_clicks.append(coordinates_of_flags)
                if count <= int(fake_mas[xIndex][yIndex]):
                    print(list_of_right_clicks)
                    set_flags(list_of_right_clicks)
                xIndex += 1
            xIndex = 0                            #Обнуляем счётчик что бы не словить out of range
            yIndex += 1 
                        #container.append([cell, xIndex, yIndex, field[yIndex + offset[0]][xIndex + offset[1]], xIndex + offset[1], yIndex + offset[0]]) # Состав одного элемента listOfneighborCells: [Ячейка, Координата X, Координата Y, Содержимое соседней ячейки, Координата Х соседа, Координата У соседа]
#Состав одного элта listOfneighborCells: [Ячейка, Координата X, Координата Y, Содержимое соседней ячейки, Координата Х соседа, Координата У соседа]
                    
    search_for_flags(fake_mas)
    # print(list_of_right_clicks)
    #Функия расстановки флагов
    
    #set_flags()
    #Функция собиранния данных об ячейках
    def look_in_field():
            global id
            for row in range(0,9):
                        print("новая строка")
                        for column in range(0,9):
                                str = (f'//*[@id="cell_{column}_{row}"]')
                                cell = driver.find_element(By.XPATH, str)
                                if hz == 1:
                                        mas[row][column] = f'{id} {cell.get_attribute("class")}'
                                        id += 1
                                #mas[j][row] = cell.get_attribute
                                #print(cell.get_attribute("class"))
                                print(f'column = {column}, row = {row}')

    look_in_field()
    update_fake_mas()
    def search_for_cells():
            count =0
            for row in range(9):
                    for column in range(9):
                        current_cell = fake_mas[row][column]
                                # Если угловые клетки с 1 и вокруг одна -1
                        if (fake_mas[row][column].find('-9') == -1 and fake_mas[row][column].find('f') == -1 and row == 0 and column == 0):
                                if fake_mas[row][column+1].find('f') != -1:
                                        count +=1
                                for y in range(2):
                                        if fake_mas[row+1][column+y].find('f') != -1:
                                                count +=1

                        elif (fake_mas[row][column].find('-9') == -1 and fake_mas[row][column].find('f') == -1 and row == 0 and column == 8):
                                if fake_mas[row][column-1].find('f') != -1:
                                        count +=1
                                for y in range(-1,1):
                                        if fake_mas[row+1][column+y].find('f') != -1:
                                                count +=1

                        elif (fake_mas[row][column].find('-9') == -1 and fake_mas[row][column].find('f') == -1 and row == 8 and column == 0):
                                if fake_mas[row][column+1].find('f') != -1:
                                        count +=1
                                for y in range(2):
                                        if fake_mas[row-1][column+y].find('f') != -1:
                                                count +=1

                        elif (fake_mas[row][column].find('-9') == -1 and fake_mas[row][column].find('f') == -1 and row == 8 and column == 8):
                                if fake_mas[row][column-1].find('f') != -1:
                                        count +=1
                                for y in range(-1,1):
                                        if fake_mas[row-1][column+y].find('f') != -1:
                                                count +=1
                        # Если клетка в первом ряду И не угловая И 1 И вокруг одна -1
                        elif (fake_mas[row][column].find('-9') == -1 and fake_mas[row][column].find('f') == -1 and row == 0 and column !=0 and column != 8):
                                if fake_mas[row][column - 1].find('f') !=-1:
                                        count +=1
                                if fake_mas[row][column + 1].find('f') !=-1:
                                        count +=1
                                for y in range(-1,2):
                                        if fake_mas[row+1][column + y].find('f') !=-1:
                                                count +=1
                        # Если клетка в последнем ряду И не угловая И 1 И вокруг одна -1
                        elif (fake_mas[row][column].find('-9') == -1 and fake_mas[row][column].find('f') == -1 and row == 8 and column !=0 and column != 8):
                                if fake_mas[row][column - 1].find('f') !=-1:
                                        count +=1
                                if fake_mas[row][column + 1].find('f') !=-1:
                                        count +=1
                                for y in range(-1,2):
                                        if fake_mas[row-1][column + y].find('f') !=-1:
                                                count +=1
                        # Если клетка в первом столбце И не угловая И 1 И вокруг одна -1
                        elif (fake_mas[row][column].find('-9') == -1 and fake_mas[row][column].find('f') == -1 and row != 0 and row != 8 and column == 0):
                                if fake_mas[row - 1][column].find('f') !=-1:
                                        count +=1
                                if fake_mas[row + 1][column].find('f') !=-1:
                                        count +=1
                                for y in range(-1,2):
                                        if fake_mas[row+y][column + 1].find('f') !=-1:
                                                count +=1
                        # Если клетка в последнем столбце И не угловая И 1 И вокруг одна -1
                        elif (fake_mas[row][column].find('-9') == -1 and fake_mas[row][column].find('f') == -1 and row != 0 and row != 8 and column == 8):
                                if fake_mas[row - 1][column].find('f') !=-1:
                                        count +=1
                                if fake_mas[row + 1][column].find('f') !=-1:
                                        count +=1
                                for y in range(-1,2):
                                        if fake_mas[row+y][column - 1].find('f') !=-1:
                                                count +=1
                        elif(fake_mas[row][column].find('-9') == -1 and fake_mas[row][column].find('f') == -1 and row != 0 and  column != 0 and row != 8 and  column != 8):
                                for x in range(-1,2):
                                        for y in range(-1,2):
                                                if fake_mas[row + x][column+y].find('f') !=-1:
                                                    count +=1
            #=======================================================================================================================
            #============================================================================================================================
                                # Если угловые клетки с 1 и вокруг одна -1
                        if current_cell != 'f':
                                if count == int(current_cell):
                                        if (fake_mas[row][column].find('-9') == -1 and fake_mas[row][column].find('f') == -1 and row == 0 and column == 0):
                                                if fake_mas[row][column+1].find('-9') != -1 and count == 1:
                                                    list_of_left_clicks.append((f'//*[@id="cell_{column+1}_{row}"]'))
                                                if fake_mas[row+1][column].find('-9') != -1 and count == 1:
                                                    list_of_left_clicks.append((f'//*[@id="cell_{column}_{row+1}"]'))
                                                if fake_mas[row+1][column+1].find('-9') != -1 and count == 1:
                                                    list_of_left_clicks.append((f'//*[@id="cell_{column+1}_{row+1}"]'))

                                        if (fake_mas[row][column].find('-9') == -1 and fake_mas[row][column].find('f') == -1 and row == 0 and column == 8):
                                                if fake_mas[row][column-1].find('-9') != -1 and count == 1:
                                                    list_of_left_clicks.append((f'//*[@id="cell_{column-1}_{row}"]'))
                                                if fake_mas[row+1][column].find('-9') != -1 and count == 1:
                                                    list_of_left_clicks.append((f'//*[@id="cell_{column}_{row+1}"]'))
                                                if fake_mas[row+1][column-1].find('-9') != -1 and count == 1:
                                                    list_of_left_clicks.append((f'//*[@id="cell_{column-1}_{row+1}"]'))

                                        if (fake_mas[row][column].find('-9') == -1 and fake_mas[row][column].find('f') == -1 and row == 8 and column == 0):
                                                if fake_mas[row][column+1].find('-9') != -1 and count == 1:
                                                    list_of_left_clicks.append((f'//*[@id="cell_{column+1}_{row}"]'))
                                                if fake_mas[row-1][column].find('-9') != -1 and count == 1:
                                                    list_of_left_clicks.append((f'//*[@id="cell_{column}_{row-1}"]'))
                                                if fake_mas[row-1][column+1].find('-9') != -1 and count == 1:
                                                    list_of_left_clicks.append((f'//*[@id="cell_{column+1}_{row-1}"]'))

                                        if (fake_mas[row][column].find('-9') == -1 and fake_mas[row][column].find('f') == -1 and row == 8 and column == 8):
                                                if fake_mas[row][column-1].find('-9') != -1 and count == 1:
                                                    list_of_left_clicks.append((f'//*[@id="cell_{column-1}_{row}"]'))
                                                if fake_mas[row-1][column].find('-9') != -1 and count == 1:
                                                    list_of_left_clicks.append((f'//*[@id="cell_{column}_{row-1}"]'))
                                                if fake_mas[row-1][column-1].find('-9') != -1 and count == 1:
                                                    list_of_left_clicks.append((f'//*[@id="cell_{column-1}_{row-1}"]'))
                                        # Если клетка в первом ряду И не угловая И 1 И вокруг одна -1
                                        if (fake_mas[row][column].find('-9') == -1 and fake_mas[row][column].find('f') == -1 and row == 0 and column !=0 and column != 8):
                                                if fake_mas[row][column - 1].find('-9') !=-1 and count == 1:
                                                    list_of_left_clicks.append((f'//*[@id="cell_{column-1}_{row}"]'))
                                                if fake_mas[row][column + 1].find('-9') !=-1 and count == 1:
                                                    list_of_left_clicks.append((f'//*[@id="cell_{column+1}_{row}"]'))
                                                for y in range(-1,1):
                                                    if fake_mas[row+1][column + y].find('-9') !=-1 and count == 1:
                                                            list_of_left_clicks.append((f'//*[@id="cell_{column+y}_{row+1}"]'))
                                        # Если клетка в последнем ряду И не угловая И 1 И вокруг одна -1
                                        if (fake_mas[row][column].find('-9') == -1 and fake_mas[row][column].find('f') == -1 and row == 8 and column !=0 and column != 8):
                                                if fake_mas[row][column - 1].find('-9') !=-1 and count == 1:
                                                    list_of_left_clicks.append((f'//*[@id="cell_{column-1}_{row}"]'))
                                                if fake_mas[row][column + 1].find('-9') !=-1 and count == 1:
                                                    list_of_left_clicks.append((f'//*[@id="cell_{column+1}_{row}"]'))
                                                for y in range(-1,1):
                                                    if fake_mas[row-1][column + y].find('-9') !=-1 and count == 1:
                                                            list_of_left_clicks.append((f'//*[@id="cell_{column+y}_{row-1}"]'))
                                        # Если клетка в первом столбце И не угловая И 1 И вокруг одна -1
                                        if (fake_mas[row][column].find('-9') == -1 and fake_mas[row][column].find('f') == -1 and row != 0 and row != 8 and column == 0):
                                                if fake_mas[row - 1][column].find('-9') !=-1 and count == 1:
                                                    list_of_left_clicks.append((f'//*[@id="cell_{column}_{row-1}"]'))
                                                if fake_mas[row + 1][column].find('-9') !=-1 and count == 1:
                                                    list_of_left_clicks.append((f'//*[@id="cell_{column}_{row+1}"]'))
                                                for y in range(-1,1):
                                                    if fake_mas[row+y][column + 1].find('-9') !=-1 and count == 1:
                                                            list_of_left_clicks.append((f'//*[@id="cell_{column+1}_{row+y}"]'))
                                        # Если клетка в последнем столбце И не угловая И 1 И вокруг одна -1
                                        if (fake_mas[row][column].find('-9') == -1 and fake_mas[row][column].find('f') == -1 and row != 0 and row != 8 and column == 8):
                                                if fake_mas[row - 1][column].find('-9') !=-1 and count == 1:
                                                    list_of_left_clicks.append((f'//*[@id="cell_{column}_{row-1}"]'))
                                                if fake_mas[row + 1][column].find('-9') !=-1 and count == 1:
                                                    list_of_left_clicks.append((f'//*[@id="cell_{column}_{row+1}"]'))
                                                for y in range(-1,1):
                                                    if fake_mas[row+y][column - 1].find('-9') !=-1 and count == 1:
                                                            list_of_left_clicks.append((f'//*[@id="cell_{column-1}_{row+y}"]'))
                                        elif(fake_mas[row][column].find('-9') == -1 and fake_mas[row][column].find('f') == -1 and row != 0 and  column != 0 and row != 8 and  column != 8):
                                                for x in range(-1,2):
                                                    for y in range(-1,2):
                                                            if fake_mas[row + x][column+y].find('-9') !=-1:
                                                                    list_of_left_clicks.append((f'//*[@id="cell_{column+y}_{row+x}"]'))
                                count = 0
    search_for_cells()
    def clicks_on_cells():
            for item in list_of_left_clicks:
                    cell = driver.find_element(By.XPATH, item)
                    if cell.get_attribute("class") != 'cell size24 hd_closed hd_flag':
                        cell.click()
    clicks_on_cells()
    for i in range(15):
            if driver.find_element(By.XPATH, '//*[@id="top_area_face"]').get_attribute('class')=='top-area-face zoomable hd_top-area-face-unpressed':
                    look_in_field()
                    update_fake_mas()
                    search_for_flags()
                    set_flags()

                    look_in_field()
                    update_fake_mas()
                    search_for_cells()
                    clicks_on_cells()
            elif driver.find_element(By.XPATH, '//*[@id="top_area_face"]').get_attribute('class')=='top-area-face zoomable hd_top-area-face-lose':
                    time.sleep(2)
                    driver.find_element(By.XPATH, '//*[@id="top_area_face"]').click()
                    losecount +=1
                    break
            elif driver.find_element(By.XPATH, '//*[@id="top_area_face"]').get_attribute('class')=='top-area-face zoomable hd_top-area-face-win':
                    time.sleep(2)
                    driver.find_element(By.XPATH, '//*[@id="top_area_face"]').click()
                    wincount +=1
                    break
    driver.find_element(By.XPATH, '//*[@id="top_area_face"]').click()
    isnt_finished += 1
print(f'Количество побед: {wincount}')
print(f'Количество поражений: {losecount}')
print(f'Всего сыграно: {isnt_finished}')