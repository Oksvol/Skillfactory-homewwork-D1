import sys
import requests  
  
# Данные авторизации в API Trello
auth_params = {    
    'key': "71b9e1cacf2d896ecee3cfd81c89336a",    
    'token': "a82d053eb3d963089887911bdcf935f31d380e0cb1d6620c5581346a9fde2762",
}
  
#Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.  
base_url = "https://api.trello.com/1/{}"

board_id = "HSAU1gXX"

'''
Первым делом научимся получать данные с нашей доски. 
PI Trello отправляет ответы в формате JSON. Это очень удобный формат для обработки и чтения. 
Для того чтобы превратить этот JSON в словари внутри Python, мы будем вызывать метод json() 
у каждого объекта, полученного при помощи модуля requests. Это облегчит задачу парсинга ответов.

'''

def read():      
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:      
        print(column['name'])    
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()      
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:      
            print('\t' + task['name'])
        print('\t' + "Количество задач: ", len(task_data)) 
    
def create(name, column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна      
    for column in column_data:      
        if column['name'] == column_name:      
            # Создадим задачу с именем _name_ в найденной колонке      
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})

def create_column(column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

      
    # Переберём данные обо всех колонках и посмотрим, нет ли там с таким же именем    
    for column in column_data:      
        if column['name'] != column_name:      
            # Создадим колонку с именем _column_name_     
            id_board = column['idBoard']
            requests.post(base_url.format('lists'), data={'name': column_name, 'idBoard': id_board, 'pos': 'bottom',  **auth_params})
            break   
    # Если есть колонка с таким именем, выведем сообщение:
        else:
            print("Колонка с таким именем уже существует")


    
def move(name, column_name):    
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
        
    # Среди всех колонок нужно найти задачу по имени и получить её id    
    task_id = None    
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:    
            if task['name'] == name:    
                task_id = task['id']    
                break    
        if task_id:    
            break    
       
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    for column in column_data:    
        if column['name'] == column_name:    
            # И выполним запрос к API для перемещения задачи в нужную колонку    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
            break    
    
if __name__ == "__main__":    
    if len(sys.argv) <= 2:    
        read()    
    elif sys.argv[1] == 'create':    
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'create_column':
        create_column(sys.argv[2])   
    elif sys.argv[1] == 'move':    
        move(sys.argv[2], sys.argv[3])  

