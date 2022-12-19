import sys  # sys нужен для передачи argv в QApplication
import os
#from tkinter.tix import TEXT  # Отсюда нам понадобятся методы для отображения содержимого директорий
from work_with_field import *
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap
from random import *
from bs4 import BeautifulSoup
import design  # Это наш конвертированный файл дизайна
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains

      
class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
       def __init__(self):
              # Это здесь нужно для доступа к переменным, методам
              # и т.д. в файле design.py
              super().__init__()
              self.setupUi(self)  # Это нужно для инициализации нашего дизайна
              self.Button_easy.clicked.connect(self.easy_mod)  # Выполнить функцию browse_folder при нажатии кнопки
              self.Button_medium.clicked.connect(self.medium_mod)
              self.Button_hard.clicked.connect(self.hard_mod)
              

       def play(zopa, level):
              try:
                     options = Options()
                     options.add_experimental_option("detach", True)
                     options.add_experimental_option('excludeSwitches', ['enable-logging'])
                     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
                     actionChains = ActionChains(driver)
                     url = f"https://minesweeper.online/ru/start/{level}" 
                     driver.implicitly_wait(30)                  # Ожидаем загрузки страницы если не дождались то timeout
                     driver.get(url = url)
                     time.sleep(3)

              
                     h,w = 0,0                                #Создание  переменных высоты и ширины поля в зависимости от выбранной сложности
                     if level == 1 or level % 10 == 1 :
                            h = 9
                            w = 9
                     elif level == 2 or level % 10 == 2 :
                            h = 16
                            w = 16
                     elif level == 3 or level % 10 == 3 :
                            h = 16
                            w = 30

                     win, lose = 0, 0
                     while(True):
                            html = driver.page_source                                                       # Из селениума получаем отрендереную html страницу что бы парсить её супом а не искать через find_element в selenium
                            soup = BeautifulSoup(html,"lxml")                                               # Передавая в конструктор супа, наш html мы получаем дерево элементов с помощью парсера lxml
                            elements = soup.find_all("div","cell")                                          # с помощью find_all находим все элементы div с CSS классом cell

                            ind = 0                                                                         # индекс для перебора элементов в elements
                            xMarkIndexY = None
                            xMarkIndexX = None
                            field = [[0] * w for i in range(h)] # Создание поля шириной w и высотой h
                            for j in range (h): 
                                   for i in range (w):
                                          elementClassLine = elements[ind]["class"] #bs4.element.ResultSet содержит внутри элементы типа Tag у которого с помощью ["class"] можно получить строку CSS классов
                                          ind += 1
                                          #field[j][i] = self.cellPars(elementClassLine)
                                          elementClassLine:list[str]
                                          if elementClassLine[2] == "hd_closed" and len(elementClassLine) == 3 : # Если ячейка закрыта
                                                 field[j][i] = "-9"
                                          elif elementClassLine[2] == "hd_closed" and elementClassLine[3] == "hd_flag": # Если ячейка закрыта, и на ней флаг
                                                 field[j][i] = "f"     #пока поставил '*' что бы не ломалась программа при победе
                                          elif elementClassLine[2] == "hd_closed" and elementClassLine[3] == "start": #Если ячейка закрыта и на ней крестик, это для режима без угадывания
                                                 field[j][i] = "x"
                                          elif elementClassLine[2] == "hd_opened" and elementClassLine[3] == "hd_type0": 
                                                 field[j][i] = "0"
                                          elif elementClassLine[2] == "hd_opened" and elementClassLine[3] == "hd_type1": 
                                                 field[j][i] = "1"
                                          elif elementClassLine[2] == "hd_opened" and elementClassLine[3] == "hd_type2": 
                                                 field[j][i] = "2"
                                          elif elementClassLine[2] == "hd_opened" and elementClassLine[3] == "hd_type3": 
                                                 field[j][i] = "3"
                                          elif elementClassLine[2] == "hd_opened" and elementClassLine[3] == "hd_type4": 
                                                 field[j][i] = "4"
                                          elif elementClassLine[2] == "hd_opened" and elementClassLine[3] == "hd_type5": 
                                                 field[j][i] = "5"
                                          elif elementClassLine[2] == "hd_opened" and elementClassLine[3] == "hd_type6": 
                                                 field[j][i] = "6"
                                          elif elementClassLine[2] == "hd_opened" and elementClassLine[3] == "hd_type7": 
                                                 field[j][i] = "7"
                                          elif elementClassLine[2] == "hd_opened" and elementClassLine[3] == "hd_type8": 
                                                 field[j][i] = "8"

                                          if field[j][i] == "x":
                                                 xMarkIndexY = j
                                                 xMarkIndexX = i
                            if xMarkIndexY != None and xMarkIndexY != None: 
                                   element = driver.find_element(By.XPATH, f"//*[@id=\"cell_{xMarkIndexX}_{xMarkIndexY}\"]")
                                   element.click()
                            else:
                                   sosedi(field,driver)
                                   print("тут КОД ДАЛЬШЕ ПИШИ")
                     

              except Exception as ex :
                     print(ex)

       def easy_mod(self):
              try:
                     if self.Guess_mo.isChecked():
                            level = 11
                     else:
                            level = 1
                     self.play(level)
              except Exception as ex :
                     print(ex)

       def medium_mod(self):
              try:
                     if self.Guess_mo.isChecked():
                            level = 12
                     else:
                            level = 2
                     self.play(level)
              except Exception as ex :
                     print(ex)
       def hard_mod(self):
              try:
                     if self.Guess_mo.isChecked():
                            level = 13
                     else:
                            level = 3
                     self.play(level)
              except Exception as ex :
                     print(ex)
       




def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()