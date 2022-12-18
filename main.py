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

#options = Options()
#options.add_experimental_option("detach", True)
#options.add_experimental_option('excludeSwitches', ['enable-logging'])
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
#actionChains = ActionChains(driver)


#driver.get("https://minesweeper.online/ru/new-game/ng")
#https://minesweeper.online/ru/start/1
#https://minesweeper.online/ru/new-game/ng
#top-area-face zoomable hd_top-area-face-unpressed
#top-area-face zoomable hd_top-area-face-win
#top-area-face zoomable hd_top-area-face-lose
      
class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.Button_easy.clicked.connect(self.easy_mod)  # Выполнить функцию browse_folder при нажатии кнопки
        self.Button_medium.clicked.connect(self.medium_mod)
        self.Button_hard.clicked.connect(self.hard_mod)
        #self.change_bt.clicked.connect(self.change_bt_func)
        #self.delete_bt.clicked.connect(self.delete_bt_func)

    def easy_mod(self):
        d_user = {}
        isgo = 0
        self.status_label.setText("Статус: " + "Парсинг в процессе")

        for i in range(0, 1):
            page = requests.get(f"https://kinocentr86.ru/events?facility=yugorskii-kinoprokat")
            page1 = page.content
            soup = BeautifulSoup(page1, "lxml")
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            count_name = 2
            count_description = 0
            u = 0
            driver.get('https://kinocentr86.ru/events?facility=yugorskii-kinoprokat')
            inf = soup.find_all("h2", class_="sc-1h5tg87-0 idrJef title")
            st = str(inf).split('href')
            l = 0
            for i in range(0, len(st)):
                #print(l)
                l +=1
        # записываем название фильмов
            for z in range(0, l-1):
                inf = soup.find_all("h2", class_="sc-1h5tg87-0 idrJef title")
                st = str(inf).split('>')
                d_user[isgo] = {}
                name = st[z+count_name][0:len(st[z+count_name])-3]
                d_user[isgo]['name'] = str(name)
        # записываем даты начала проката
                inf = soup.find_all("div", class_="sc-jp24ki-1 qqVem")
                st = str(inf).split('В прокате с')
                data_start = st[z+1][38:45]
                d_user[isgo]['data_start'] = str(data_start)
        # записываем даты конца проката
                inf = soup.find_all("div", class_="sc-jp24ki-1 qqVem")
                st = str(inf).split('В прокате до')
                data_finish = st[z+1][38:45]
                d_user[isgo]['data_finish'] = str(data_finish)
        # записываем хоронометраж, если есть
                inf = soup.find_all("div", class_="sc-jp24ki-1 qqVem")
                st = str(inf).split('Дата может быть изменена кинотеатром или прокатчиком')
                if st[z+1].find("Хронометраж") !=-1:
                    duration = st[z+1][1135:1145]
                else:
                    duration = "-"
                d_user[isgo]['duration'] = str(duration)
        # записываем режисера
                inf = soup.find_all("div", class_="sc-jp24ki-1 qqVem")
                st = str(inf).split('Дата может быть изменена кинотеатром или прокатчиком')
                if st[z+1].find("Режиссер") !=-1:
                    first_line = st[z+1].split('Режиссер')
                    second_line = first_line[1].split('</div>')
                    director = second_line[1][32:len(second_line[1])]
                else:
                    director = '-'
                d_user[isgo]['director'] = str(director)
        # записываем актеров
                inf = soup.find_all("div", class_="sc-jp24ki-1 qqVem")
                st = str(inf).split('Дата может быть изменена кинотеатром или прокатчиком')
                if st[z+1].find("В ролях") !=-1:
                    first_line = st[z+1].split('В ролях')
                    second_line = first_line[1].split('</div>')
                    roles = second_line[1][32:len(second_line[1])]
                else:
                    roles = '-'
                d_user[isgo]['roles'] = str(roles)
        # записываем описание
                inf = soup.find_all("div", class_="sc-bdvvtL sc-gsDKAQ sc-gp24bs-7 iiPQI hIxhWw bxXAEF")
                st = str(inf).split('sc-bdvvtL sc-gsDKAQ sc-gp24bs-7 iiPQI hIxhWw bxXAEF')
                if st[z+1].find("sc-gp24bs-8 fOqJFv") !=-1:
                    st = st[z+1].split('sc-gp24bs-8 fOqJFv')
                    first_line = st[1].split('><div>')
                    second_line = first_line[1].split('</div>')
                    description = second_line[0]
                else:
                    description = '-'
                d_user[isgo]['description'] = str(description.replace("\n", " "))
        # скачиваем постер
                #driver.execute_script("window.scrollTo(0, " + str(z*1000) + ");")
                u += 1000
                time.sleep(2)
                driver.execute_script("arguments[0].scrollIntoView();", (driver.find_elements(by=By.TAG_NAME, value="img")[z+2]))
                images = driver.find_elements(by=By.TAG_NAME, value="img")
                #print(images[z+1].get_attribute('src'))
                src = images[z+1].get_attribute('src')
                try:    
                    p = requests.get(src)
                    name_of_poster = (d_user[z]['name']).replace(":", "")
                    path_of_poster = "C:\practic\ "
                    file = path_of_poster[0:11] + name_of_poster +".jpg"
                    #print(file)
                    out = open(file = file, mode= 'wb')
                    out.write(p.content)
                    out.close()
                except :
                    a= 0
                
                count_name +=3
                count_description =2
                isgo += 1
        #print(d_user)
        path_of_poster = "C:\practic\ "
        name_of_file = "parse_result"
        file = path_of_poster[0:11] + name_of_file +".txt"
        with open(file = file, mode = "w", encoding = 'utf-8') as f:
            for i in range(0, l-1):
                f.write(d_user[i]['name'] + "$" + d_user[i]['data_start'] + "$" + d_user[i]['data_finish'] + "$" + d_user[i]['duration'] + "$" + d_user[i]['director'] + "$" + d_user[i]['roles']+ "$" + d_user[i]['description'] + "\n")
        self.status_label.setText("Статус: " + "Парсинг Завершён")
        if self.checkBox.isChecked():
            try:
                self.status_label.setText("Статус: " + "Загрузка в процессе")
                self.comboBox_of_film.clear()
                path_of_poster = "C:\practic\ "
                name_of_file = "parse_result"
                file = path_of_poster[0:11] + name_of_file +".txt"
                with open(file = file, mode = "r", encoding = 'utf-8') as f:
                    for line in f:
                        lines = line.split("$")
                        self.comboBox_of_film.addItem(lines[0])
                text = self.comboBox_of_film.currentText()
                path_of_poster = "C:\practic\ "
                name_of_file = "parse_result"
                name_of_poster = text.replace(":", "")
                file = path_of_poster[0:11] + name_of_file +".txt"
                with open(file = file, mode = "r", encoding = 'utf-8') as f:
                    for line in f:
                        if line.find(text) !=-1:
                            lines = line.split("$")
                            self.film.setText("Название: " + lines[0])
                            self.data_start.setText("Начало проката: " + lines[1])
                            self.data_end.setText("Конец проката: " + lines[2])
                            self.duration.setText("Хронометраж: " + lines[3])
                            self.director.setText("Режиссер: " + lines[4])
                            self.actors.setText("В ролях: " + lines[5])
                            self.discription.setText(lines[6])
                            self.discription.setFont(QtGui.QFont('SansSerif', 10)) # Изменение шрифта и размера
                            pixmap = QPixmap(path_of_poster[0:11] + name_of_poster +".jpg")
                            self.poster.setPixmap(pixmap)
                self.status_label.setText("Статус: " + "Парсинг и Загрузка завершена")
            except:
                self.film.setText("ОШИБКА")
    def medium_mod(self):
        try:
            self.status_label.setText("Статус: " + "Загрузка в процессе")
            self.comboBox_of_film.clear()
            path_of_poster = "C:\practic\ "
            name_of_file = "parse_result"
            file = path_of_poster[0:11] + name_of_file +".txt"
            with open(file = file, mode = "r", encoding = 'utf-8') as f:
                for line in f:
                    lines = line.split("$")
                    self.comboBox_of_film.addItem(lines[0])
            text = self.comboBox_of_film.currentText()
            path_of_poster = "C:\practic\ "
            name_of_file = "parse_result"
            name_of_poster = text.replace(":", "")
            file = path_of_poster[0:11] + name_of_file +".txt"
            with open(file = file, mode = "r", encoding = 'utf-8') as f:
                for line in f:
                    if line.find(text) !=-1:
                        lines = line.split("$")
                        self.film.setText("Название: " + lines[0])
                        self.data_start.setText("Начало проката: " + lines[1])
                        self.data_end.setText("Конец проката: " + lines[2])
                        self.duration.setText("Хронометраж: " + lines[3])
                        self.director.setText("Режиссер: " + lines[4])
                        self.actors.setText("В ролях: " + lines[5])
                        self.discription.setText(lines[6])
                        self.discription.setFont(QtGui.QFont('SansSerif', 10)) # Изменение шрифта и размера
                        pixmap = QPixmap(path_of_poster[0:11] + name_of_poster +".jpg")
                        self.poster.setPixmap(pixmap)
            self.status_label.setText("Статус: " + "Загрузка завершена")
        except:
            self.film.setText("ОШИБКА")
    def hard_mod(self):
        try:
            self.status_label.setText("Статус: " + "Удаление в процессе")
            text_new_desc = self.new_discription.text()
            text = self.comboBox_of_film.currentText()
            path_of_poster = "C:\practic\ "
            name_of_file = "parse_result"
            name_of_poster = text.replace(":", "")
            file = path_of_poster[0:11] + name_of_file +".txt"
            
            with open (file = file, mode = 'r',encoding = 'utf-8') as f:
                old_data = f.read()
            with open(file = file, mode = "r+", encoding = 'utf-8') as f:
                for line in f:
                    if line.find(text) !=-1:
                        line_to_change = line
            new_data = old_data.replace(line_to_change, "")

            with open (file = file, mode ='w',encoding = 'utf-8') as f:
                f.write(new_data)
            self.comboBox_of_film.clear()
            path_of_poster = "C:\practic\ "
            name_of_file = "parse_result"
            file = path_of_poster[0:11] + name_of_file +".txt"
            with open(file = file, mode = "r", encoding = 'utf-8') as f:
                for line in f:
                    lines = line.split("$")
                    self.comboBox_of_film.addItem(lines[0])
            text = self.comboBox_of_film.currentText()
            path_of_poster = "C:\practic\ "
            name_of_file = "parse_result"
            name_of_poster = text.replace(":", "")
            file = path_of_poster[0:11] + name_of_file +".txt"
            with open(file = file, mode = "r", encoding = 'utf-8') as f:
                for line in f:
                    if line.find(text) !=-1:
                        lines = line.split("$")
                        self.film.setText("Название: " + lines[0])
                        self.data_start.setText("Начало проката: " + lines[1])
                        self.data_end.setText("Конец проката: " + lines[2])
                        self.duration.setText("Хронометраж: " + lines[3])
                        self.director.setText("Режиссер: " + lines[4])
                        self.actors.setText("В ролях: " + lines[5])
                        self.discription.setText(lines[6])
                        self.discription.setFont(QtGui.QFont('SansSerif', 10)) # Изменение шрифта и размера
                        pixmap = QPixmap(path_of_poster[0:11] + name_of_poster +".jpg")
                        self.poster.setPixmap(pixmap)
            self.status_label.setText("Статус: " + "Удаление завершено")
        except:
            self.film.setText("ОШИБКА")




def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()