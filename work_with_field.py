from selenium import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains

def clicks_on_flags(list_of_right_clicks, driver:webdriver.Chrome):
    actionChains = ActionChains(driver)
    for item in list_of_right_clicks:
        string = f'//*[@id="cell_{list_of_right_clicks[1]}_{list_of_right_clicks[0]}"]'
        cell = driver.find_element(By.XPATH, item)
        if cell.get_attribute("class") != 'cell size24 hd_closed hd_flag':
            actionChains.context_click(cell).perform()
def sosedi(field:list, driver:webdriver.Chrome):
    list_of_right_clicks = []
    list_of_left_clicks = []
    count_of_free_cells = 0
    count_of_flags = 0
    listOfneighborCells = []          #лист соседов                                                                             #-1,-1 -1,0   -1,1
    container = []                    #лист для заполнения листа соседов                                                        # 0,1    0     0,1
    offsetList = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]] #Все возможные смещения для соседей клетки Рисунок:    # 1,-1  1,0    1,1  координаты в формате (y,x)
    xIndex,yIndex = 0,0                 # Индексы ячейки для которой ищем соседей, используем это потому что list.index работает немного кривовато для нас
    for row in field:                   # берём каждую строчку из поля
        for cell in row:                # к каждой ячейке в строчке применяем код ниже:
            for offset in offsetList:   # Применяем к индексам ячейки смещение
                if yIndex + offset[0] >= 0 and xIndex + offset[1] >=0 and yIndex + offset[0] <= len(field) - 1 and xIndex + offset[1] <= len(row) - 1 : # первый and проверка на отрицательность смещённых индексов, что бы не получать значения с конца. Третий and для определения вышли мы за предел листа и если вышли то пропускаем такое смещение
                    container.append([cell, xIndex, yIndex, field[yIndex + offset[0]][xIndex + offset[1]], xIndex + offset[1], yIndex + offset[0]]) 
# Состав одного элемента listOfneighborCells: [Ячейка, Координата X, Координата Y, Содержимое соседней ячейки, Координата Х соседа, Координата У соседа]
                    listOfneighborCells.append(container)   # добавляем соседа ячейки в лист соседов                                                                                                0         1              2                      3                        4                   5
                    if field[yIndex + offset[0]][xIndex + offset[1]] == "-9":
                        count_of_free_cells += 1
                        list_of_right_clicks.append([xIndex + offset[1], yIndex + offset[0]])
                    if field[yIndex + offset[0]][xIndex + offset[1]] == "f":
                        count_of_flags += 1
                    list_of_left_clicks.append([xIndex + offset[1], yIndex + offset[0]])
                    container = []                          #Пересоздаём контейнер что бы не получать повторение одного массива
            if count_of_free_cells <= int(cell):
                clicks_on_flags(list_of_right_clicks, driver)
            #if count_of_flags != int(cell):
                #li
            count_of_free_cells = 0
            xIndex += 1                       #rowIndex - счётчик символа в строке
        xIndex = 0                            #Обнуляем счётчик что бы не словить out of range
        yIndex += 1                         #columnindex - счётчик строки
    return listOfneighborCells