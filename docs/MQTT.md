# MQTT - komunikacja z balonem i prototyp przeplywu danych

Ten dokument opisuje, jak ma dzialac komunikacja po MQTT w projekcie Ground Station oraz jak dziala obecny prototyp przygotowany na kontenerach `AI` i `Test` w folderze test/MQTT_TEST.

## Cel komunikacji

Docelowy przeplyw danych wyglada tak:

1. Balon wysyla surowe dane telemetryczne.
2. Modul `Communication` odbiera dane z balonu.
3. `Communication` publikuje albo przekazuje dane dalej do systemu.
4. Backend odbiera dane, zapisuje je, udostepnia UI i przekazuje do dalszej analizy.
5. Modul `AI` moze analizowac odebrane dane i zwracac wynik analizy.

Na ten moment MQTT jest sprawdzony jako prototyp na dwoch kontenerach:

- `AI` - symuluje nadawce danych z balonu i publikuje dane na topic MQTT.
- `Test` - symuluje odbiorce, subskrybuje topic MQTT i przetwarza odebrana wiadomosc.
- `mqtt` - broker MQTT oparty o obraz `eclipse-mosquitto`.

## Czym jest MQTT w tym projekcie

MQTT dziala tutaj jak prosty system tematow:

- jeden kontener publikuje wiadomosci na konkretny topic,
- broker MQTT odbiera te wiadomosci,
- inne kontenery subskrybuja ten topic i dostaja kazda nowa wiadomosc.

W prototypie uzywamy topicu:

```text
balloon/raw
```

Ten topic oznacza surowe dane odebrane z balonu albo dane testowe udajace dane z balonu.

Broker MQTT jest dostepny w sieci Dockera pod nazwa:

```text
mqtt
```

i na porcie:

```text
1883
```

Dlatego w kodzie kontenery lacza sie tak:

```python
client.connect("mqtt", 1883)
```

## Aktualny przeplyw w prototypie

Aktualnie przeplyw wyglada tak:

```text
src/AI/main.py
    -> publikuje JSON na topic balloon/raw
    -> broker mqtt
    -> src/Test/main.py
    -> odbiera JSON i przelicza przykladowa wartosc strength
```

Wazne: w obecnym kodzie `Test` tylko wypisuje wynik w logach. Nie wysyla go jeszcze do backendu. To jest dobre miejsce na kolejny krok integracji, czyli dodanie requestu do `Backend` albo publikacji na osobny topic, np. `balloon/processed`.

## Kontener AI - nadawanie danych

Plik:

```text
src/AI/main.py
```

Ten kontener pelni teraz role generatora danych testowych. W prawdziwym systemie podobna logika moze zostac zastapiona danymi przychodzacymi z modulu `Communication`.

### Polaczenie z brokerem

```python
client = mqtt.Client()
client.connect("mqtt", 1883)
```

Co robi:

- tworzy klienta MQTT,
- laczy sie z brokerem MQTT,
- broker jest dostepny jako `mqtt`, bo taka nazwa serwisu jest ustawiona w `docker-compose.yml`,
- port `1883` to standardowy port MQTT.

### Funkcja `get_data()`

```python
def get_data():
    return {"rssi": -70, "signal": "raw", "time": time.time()}
```

Co robi:

- zwraca przykladowe dane telemetryczne,
- `rssi` oznacza sile sygnalu,
- `signal` ma wartosc `"raw"`, czyli dane sa surowe,
- `time` to aktualny czas wygenerowania probki.

Przykladowy wynik:

```json
{
  "rssi": -70,
  "signal": "raw",
  "time": 1730000000.123
}
```

Jak ja wywolac:

```python
data = get_data()
```

### Publikowanie danych

```python
client.publish(
    "balloon/raw",
    json.dumps(data)
)
```

Co robi:

- zamienia slownik Pythona na JSON przez `json.dumps(data)`,
- wysyla wiadomosc na topic `balloon/raw`,
- kazdy kontener subskrybujacy `balloon/raw` dostanie te dane.

### Petla wysylania

```python
while True:
    data = get_data()
    client.publish("balloon/raw", json.dumps(data))
    time.sleep(1)
```

Co robi:

- co sekunde generuje dane,
- publikuje je do MQTT,
- dziala caly czas, dopoki kontener jest uruchomiony.

## Kontener Test - odbieranie danych

Plik:

```text
src/Test/main.py
```

Ten kontener pelni role testowego odbiorcy danych MQTT.

### Funkcja `on_message(client, userdata, msg)`

```python
def on_message(client, userdata, msg):
    data = json.loads(msg.payload)

    print("Odebrano:", data)

    processed = {
        "strength": data["rssi"] * 2
    }

    print("Processed:", processed)
```

Ta funkcja jest callbackiem MQTT. Oznacza to, ze nie wywolujemy jej recznie w kodzie. Biblioteka `paho-mqtt` wywoluje ja automatycznie za kazdym razem, gdy przyjdzie nowa wiadomosc na subskrybowany topic.

Parametry:

- `client` - klient MQTT, ktory odebral wiadomosc,
- `userdata` - dodatkowe dane uzytkownika, w tym prototypie nieuzywane,
- `msg` - obiekt wiadomosci MQTT.

Co robi funkcja:

1. Odczytuje payload wiadomosci:

   ```python
   data = json.loads(msg.payload)
   ```

   `msg.payload` zawiera bajty odebrane z MQTT. `json.loads(...)` zamienia je na slownik Pythona.

2. Wypisuje odebrane dane:

   ```python
   print("Odebrano:", data)
   ```

3. Tworzy przykladowy wynik przetwarzania:

   ```python
   processed = {
       "strength": data["rssi"] * 2
   }
   ```

   Aktualnie `strength` jest tylko demonstracja. Liczymy ja jako `rssi * 2`.

4. Wypisuje wynik:

   ```python
   print("Processed:", processed)
   ```

Jak ta funkcja jest wywolywana:

```python
client.on_message = on_message
```

Ta linia podpina funkcje `on_message` do klienta MQTT. Od tego momentu klient wie, co zrobic po odebraniu wiadomosci.

### Subskrypcja topicu

```python
client.subscribe("balloon/raw")
```

Co robi:

- zapisuje klienta jako odbiorce topicu `balloon/raw`,
- wszystkie wiadomosci wyslane na ten topic trafia do funkcji `on_message`.

### Uruchomienie odbioru

```python
client.loop_forever()
```

Co robi:

- uruchamia petle MQTT,
- utrzymuje polaczenie z brokerem,
- odbiera wiadomosci,
- automatycznie wywoluje `on_message`.

Bez `loop_forever()` program by sie zakonczyl i nie odbieralby zadnych danych.

## Uruchomienie prototypu

Najprosciej uruchomic wszystko przez Docker Compose:

```bash
docker compose up --build
```

Wtedy startuja m.in.:

- `mqtt` - broker MQTT,
- `ai` - generator danych,
- `test` - odbiorca danych.

Podglad logow kontenera `test`:

```bash
docker compose logs -f test
```

W logach powinno byc widac cos w tym stylu:

```text
Odebrano: {'rssi': -70, 'signal': 'raw', 'time': 1730000000.123}
Processed: {'strength': -140}
```

Podglad logow kontenera `ai`:

```bash
docker compose logs -f ai
```

Zatrzymanie srodowiska:

```bash
docker compose down
```

## Jak wyslac testowa wiadomosc recznie w kodzie

Minimalny przyklad publikacji:

```python
import json
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("mqtt", 1883)

data = {
    "rssi": -65,
    "signal": "raw"
}

client.publish("balloon/raw", json.dumps(data))
```

Ten kod trzeba uruchomic w kontenerze, ktory jest w tej samej sieci Dockera co broker `mqtt`. Poza Dockerem adres `mqtt` nie zadzialalby bez dodatkowej konfiguracji DNS. Z hosta mozna laczyc sie przez `localhost:1883`, bo port jest wystawiony w `docker-compose.yml`.

## Jak odebrac wiadomosc recznie w kodzie

Minimalny przyklad subskrypcji:

```python
import json
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    print(data)

client = mqtt.Client()
client.on_message = on_message

client.connect("mqtt", 1883)
client.subscribe("balloon/raw")

client.loop_forever()
```

## Planowany kierunek integracji z backendem

Obecny prototyp pokazuje tylko droge:

```text
AI/Test data generator -> MQTT -> Test receiver
```

Docelowo powinno to isc w kierunku:

```text
Balloon -> Communication -> MQTT/backend -> Backend -> UI/AI
```

Proponowany kolejny krok:

1. `Communication` odbiera prawdziwe dane z balonu.
2. `Communication` publikuje dane na `balloon/raw`.
3. Backend albo osobny worker subskrybuje `balloon/raw`.
4. Backend zapisuje dane i wystawia je dla UI.
5. `AI` dostaje dane z backendu albo subskrybuje MQTT i publikuje wynik analizy na osobny topic.

Mozliwe dodatkowe topiki:

```text
balloon/raw
balloon/processed
balloon/ai/result
balloon/status
```

## Najwazniejsze miejsca w kodzie

```text
src/AI/main.py
```

- `get_data()` - generuje testowe dane.
- `client.publish("balloon/raw", json.dumps(data))` - wysyla dane do MQTT.

```text
src/Test/main.py
```

- `on_message(...)` - odbiera i przetwarza wiadomosc.
- `client.subscribe("balloon/raw")` - slucha topicu z danymi.
- `client.loop_forever()` - utrzymuje odbior wiadomosci.

```text
docker-compose.yml
```

- `mqtt` - broker MQTT.
- `ai` - kontener publikujacy dane testowe.
- `test` - kontener odbierajacy dane testowe.

## Uwagi dla zespolu

- Wiadomosci MQTT wysylamy jako JSON.
- Topic `balloon/raw` traktujemy jako dane surowe.
- Funkcja `on_message` jest wywolywana automatycznie przez MQTT, nie recznie.
- Obecne przeliczanie `strength = rssi * 2` jest tylko testem dzialania przeplywu.
- Integracja z backendem nie jest jeszcze podpieta w prototypie MQTT.
