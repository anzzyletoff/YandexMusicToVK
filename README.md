# :o: Установка

## :black_medium_square: Установка программ :black_medium_square:

> :loudspeaker:  Данный этап можно пропустить, если у вас уже стоят данные программы

#### :arrow_right: Python (сам я/п)
```
>   apt install python3.8
>   apt install -y python3-pip
```

#### :arrow_right: PM2 (для запуска скрипта в фон)
 ```
>   apt install npm
>   npm install pm2@latest -g
```

## :black_medium_square: Установка необходимых модулей :black_medium_square:

```
>   pip3 install vk_api
>   pip3 install git+https://github.com/MarshalX/yandex-music-api@development
```

## :black_medium_square: Установка самого скрипта :black_medium_square:

```
>   git clone https://github.com/AnzzyLetoff/YandexMusicToVK
```

# :o: Настройка

> :loudspeaker: Настройка проводится путём редактирования файла config.json, иные файлы редактировать не требуется!

+ Открываем файл config.json в репозитории скрипта
+ Меняем поля в соответствии с приложенным ниже описанием

![alt text](/config_screen.png)

##### * afkTime = Время в секундах, поделённое на 10, через которое бот уйдёт в афк-режим, если песня останется одной и той же на протяжении этого времени (пример: 10 минут = 600 секунд // 10 = 60)*

+ Получить токен ВК можно [тут](https://vkhost.github.io/), просто выберите Kate Mobile в списке сервисов, авторизуйтесь, а затем скопируйте символы из адресной строки, как это показано на фото ниже
![alt text](/token_screen.png)

# :o: Запуск
> :loudspeaker:  Ниже будет продемонстрировано, как с помощью PM2 запустить программу в фон, проверено было на Ubuntu 18.04, за остальные ОС не ручаюсь

+ Устанавливаем PM2 из первого пункта
+ Заходим в папку со скриптом
+ Прописываем команду ниже
```
>   pm2 start YandexMusicToVK.py --interpreter=python3.8          (в конце ставьте версию Python, установленную у вас)
```
