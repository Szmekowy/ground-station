# Docker - Ground Station Cheatsheet

## 1. Uruchomienie projektu

Uruchomienie wszystkich kontenerów:

```bash
docker compose up
```
Po zmianie plików

```bash
docker compose up --build
```

## 2. Sprawdzenie działających kontenerów

```bash
docker compose ps
```

## 3. Uruchamianie plików w kontenerze

Jak już kontenery są uruchomione możemy odpalić konkretne pliki w kontenerze.

```bash
docker compose exec backend python main.py
```

Możemy współdzielić foldery aby np backend odrazu miał dostęp do testów.

```bash
backend:

  volumes:
    - ./src/Backend:/workspace
    - ./tests:/workspace/tests
    - ./data:/workspace/data
```

Dzięki temu można odpalić testy w kontenerze za pomocą takiej komendy 

```bash
docker compose exec backend python tests/test_database.py
```

## 4. Baza danych

Wejćie do bazy danych i wtedy można pisać różne komendy np SELECT itd

```bash
docker compose exec postgres psql -U postgres -d ground_station
```