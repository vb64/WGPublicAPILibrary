# Примеры кода на Python

**papy.py** - модуль для работы с WG PAPI.

создать обьект _papi.Session_. Аргументы: адрес регионального сервера, ключ зарегистрированного приложения. Запросы к WG PAPI делать, вызывая метод _fetch_ с аргументами: url запроса, параметры запроса.

> import papi

> api = papi.Session(papi.Server.RU, 'demo')

> api.fetch('wot/account/list', 'search=Serb&limit=1')

Дополнительный метод _isClanDeleted_(ID_клана), проверяет существование клана с заданным айди, 
т.к. PAPI [не предоставляет надежных штатных механизмов](https://github.com/OpenWGPAPI/WGPublicAPILibrary/issues/2 ) для решения этой задачи. 
