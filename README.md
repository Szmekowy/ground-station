# Ground Station

Prosta aplikacja podzielona na kilka części uruchamianych w Dockerze:

- `Communication` - moduł komunikacji
- `Backend` - logika backendu
- `AI` - moduł AI
- `UI` - interfejs użytkownika

Każda część ma swój własny `Dockerfile`, więc można uruchamiać moduły osobno. Całą aplikację najwygodniej odpala się przez `docker compose`.

## Wymagania

Przed uruchomieniem trzeba mieć zainstalowane:

- Docker
- Docker Compose

Sprawdzenie instalacji:

```bash
docker --version
docker compose version
```

## Uruchamianie pojedynczej części

Każdy użytkownik może odpalić tylko swoją część aplikacji. Schemat jest taki sam dla wszystkich modułów:

```bash
docker build -t nazwa-obrazu ./src/NazwaModulu
docker run --rm -p port:port nazwa-obrazu
```

Przykłady dla konkretnych modułów:

### Communication

```bash
docker build -t ground-communication ./src/Communication
docker run --rm -p 8001:8001 ground-communication
```

### Backend

```bash
docker build -t ground-backend ./src/Backend
docker run --rm -p 8002:8002 ground-backend
```

### AI

```bash
docker build -t ground-ai ./src/AI
docker run --rm -p 8003:8003 ground-ai
```

### UI

```bash
docker build -t ground-ui ./src/UI
docker run --rm -p 8000:8000 ground-ui
```

Po uruchomieniu kontener wypisuje logi w terminalu. Zatrzymanie kontenera: `Ctrl+C`.

## Uruchamianie całej aplikacji

Do uruchomienia wszystkich części naraz służy plik `docker-compose.yml`.

Start aplikacji:

```bash
docker compose up --build
```

Ta komenda:

- buduje obrazy dla wszystkich modułów,
- uruchamia `communication`, `backend`, `ai` i `ui`,
- wystawia porty:
  - `UI`: `8000`
  - `Communication`: `8001`
  - `Backend`: `8002`
  - `AI`: `8003`

Zatrzymanie aplikacji:

```bash
docker compose down
```

Uruchomienie w tle:

```bash
docker compose up --build -d
```

Podgląd logów:

```bash
docker compose logs -f
```

Podgląd logów tylko jednego modułu:

```bash
docker compose logs -f ui
docker compose logs -f backend
docker compose logs -f communication
docker compose logs -f ai
```

## Jak działa Docker Compose w tym projekcie

`docker-compose.yml` opisuje cztery serwisy:

- `communication` budowany z `./src/Communication` i dostępny na porcie `8001`
- `backend` budowany z `./src/Backend`, dostępny na porcie `8002` i uruchamiany po `communication`
- `ai` budowany z `./src/AI`, dostępny na porcie `8003` i uruchamiany po `backend`
- `ui` budowany z `./src/UI`, dostępny na porcie `8000` i uruchamiany po `backend`

Dzięki temu nie trzeba ręcznie uruchamiać każdego kontenera osobno. Compose tworzy wspólną sieć dla serwisów i startuje je w odpowiedniej kolejności.
