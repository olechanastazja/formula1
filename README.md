# Formula 1

Zadanie zostało wykonane z wykorzystaniem Pythona 3.6. Jest on wymagany do uruchomienia.
Do obsługi komunikatów używany jest RabbitMQ. Do zarządzania wysyłaniem komunikatów celery.

Skrypt `formula1.py` wysyła co 15 sekund informacje z bolida. Są ona automatycznie generowanymi 
randomowymi liczbami z zakresu od 0 do 100. 
Co 17 sekund wysyłane jest pytanie od kierowcy do kierownika z prośbą o zjechanie do pitstopu.
Otrzymuje wylosowaną odpowiedź. (wzorzec Request-Reply)

Komunikaty z bolidu przetwarzane są przez dwóch niezależnych odbiorców. Logger zapisuje do pliku `logs.txt`
wszystkie otrzymane informacje. Część odpowiedzialna za monitoring na podstawie otrzymanych informacji wysyła je
do mechaników lub do kierowcy (wzorzec Message Router).

#### Instalacja 

##### virtualenv

```
$ sudo apt-get update
$ sudo apt-get install python-virtualenv
```
##### RabbitMQ

```
$ sudo apt-get install rabbitmq-server
```


```
$ cd formula1
$ virtualenv -p python3 venv/
$ source venv/bin/activate
$ pip install -r requirements.txt
```

#### Użytkowanie

###### Uruchomienie workera celery

```
$ celery -A formula1 worker --loglevel=DEBUG
```

###### Uruchomienie skryptu wysyłacjego wiadomości

W nowej karcie
```
$ python3 formula1.py
```

 

