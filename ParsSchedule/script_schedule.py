import json

import unicodedata

from bs4 import BeautifulSoup

# TODO: Функция для парсинга html страницы с расписанием и зыписыванием готовых данных в json файл
def get_data():
     
     # * Открыл файл с html кодом и распарсил его в BeautifulSoup
     with open('schedule.html') as file:
          soup = BeautifulSoup(file.read(), 'lxml')
          
          
     # * Все классы от 5А до 11Б
     classes = soup.find_all('h2')
     result_classes = [i.text for i in classes]   # ? Сохраняю классы в список

          
     # * Дни от понедельника до субботы
     main = soup.findAll('table')
     
     for main_ in main:
          days = main_.find('tr')
          days = days.find_all('td')[2:]
          break
     
     result_days = [i.text for i in days]  # ? Сохраняю в список все дни
               
     
     # * Основной словарь с данными вида {Класс: {дни недели: [уроки]}}
     data = {key: {value: [] for value in result_days} for key in result_classes}
     
     
     # * Достаю уроки всех классов
     main = soup.findAll('caption')
     result_lessons = []
     
     for main_ in main:
          new = main_.parent
          search = new.find_all('td', class_='T1')
          
          # ? Сохраняю все уроки в список вида [ [уроки] ]
          result_lessons.append([unicodedata.normalize('NFKD', sc.get_text()) for sc in search])   
          
            
     # * Сортирую все уроки для каждого класса по дням
     for item in result_lessons:
          near = []   # ? В списке содержится расписание на неделю для каждого класса. Вид [уроки]
         
          for value in item:
               near.append(value)
               
          index = 0
          for class_ in result_classes:
               while index < len(near):
                    for d in data[class_].keys():
                         data[class_][d].append(near[index])   # ? В каждый день недели по очереди добавляю уроки
                         index += 1
                         
               result_classes.remove(class_)   # ? Удаляю класс чтобы в него не заносились все уроки
                    
               if index >= len(near):
                    break
     
     
     # * Сохраняю сортированные данные в файл json формата
     with open('data.json', 'w', encoding='utf-8') as file:
          json.dump(data, file, indent=1, ensure_ascii=False)      
          

def main():
     get_data()
     
     
if __name__ == '__main__':
     main()    


     


     