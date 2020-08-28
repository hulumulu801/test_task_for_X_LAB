# Описание файлов:
  **requirement.txt** - зависимости
  
  Папка: Exercise_1 - Задание 1. В этой папке содержится:
    
    1.wav, 2.wav, 3.wav, 4.wav - голосовые сообщения
    
    main.py - скрипт. Скрипт создаст файлы:
    
     - log_fail.txt - лог-файл ошибок(если будут ошибки)
     
     - log_file.csv - лог-файл распознования
    
    sql_query.csv - sql-запрос
    
 Папка: Exercise_2 - Задание 2. В этой папке содержится:
 
    database_query.py - скрипт запроса в СУБД. Скрипт создаст файл:
    
     - sql_query.csv - sql-запрос 
    
 Папка: example_pict - пример запроса с СУБД(jpg). В этой папке содержится:
 
    Снимок экрана от 2020-08-28 10-12-34.png
    
 **Пример запроса и СУБД:**
 
 ![Image alt](https://github.com/hulumulu801/test_task_for_X_LAB/blob/master/example_pict/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%20%D0%BE%D1%82%202020-08-28%2010-12-34.png)

# Установка:
 pip3 install --upgrade pip
 
 pip3 install --upgrade setuptools
 
 pip3 install -r requirement.txt
 
# Использование:
- переходим в папку Exercise_1

- в консоли пишем:

**python main.py 1.wav 8909055555 1 stage-1**

1.wav - голосовое сообщение

8909055555 - номер телефона

1 или 0 - флаг необходимости записи в СУБД. 1 - запись. 0 - не записывать в СУБД

