# Примеры кода на Python

**papi.py** - модуль для работы с WG PAPI.

создать обьект _papi.Session_. Аргументы: адрес регионального сервера, ключ зарегистрированного на этом сервере приложения. Запросы к WG PAPI делать, вызывая метод _fetch_ с аргументами: url запроса, параметры запроса.

> import papi

> api = papi.Session(papi.Server.RU, 'demo')

> api.fetch('wot/account/list', 'search=Serb&limit=1')

Дополнительный метод _isClanDeleted_(ID_клана), проверяет существование клана с заданным айди, 
т.к. PAPI [не предоставляет надежных штатных механизмов](https://github.com/OpenWGPAPI/WGPublicAPILibrary/issues/2 ) для решения этой задачи. 

**hello_serb.py** - пример использования модуля _papi.py_

**Пример реализации авторизации через Wargaming OpenID на своем сайте.** Python, Django, Google App Engine.

[Действующий пример](http://openid-gae.appspot.com/)

[Код примера](https://github.com/vb64/gae-openid)

[Поясняющая статья](http://blog.vitaly-bogomolov.ru/2014/09/openid-wargamingnet-django.html)

Публиковал код не тут, т.к. осваивал технологию PushToDeploy, предоставленную gihub и GoogleAppEngine. Там требуется отдельный репозитарий с админскими правами.

**replay.py** - обработка файлов .wotreplay.

Использование:
_python replay.py имя-файла.wotreplay [dump]_

выводит: версию, дату, карту, ник и технику игрока, тип боя, составы команд. Если реплей записан до конца боя, выводится какая команда победила. Если задан последний аргумент _dump_, выводится полное содержимое секции[й] с json данными.

См.также [статью](https://github.com/OpenWGPAPI/WGPublicAPILibrary/wiki/%D0%A4%D0%BE%D1%80%D0%BC%D0%B0%D1%82-%D1%84%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2-.wotreplay-%D0%B8%D0%B3%D1%80%D1%8B-WorldOfTanks) про формат файлов wotreplay.
