# Liquid Protocol Launch Bot

Telegram бот для мониторинга новых лаунчей токенов на Liquid Protocol (Base chain).

## Быстрый старт

### 1. Подготовка

```bash
# Клонирование
git clone <repo>
cd liquid-launch-bot

# Создание .env
cp .env.example .env
```

### 2. Конфигурация .env

Отредактируйте `.env`:

```env
# Telegram Bot Token (от @BotFather)
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Chat ID для публичного канала
TELEGRAM_CHAT_ID=@liquid_launches

# Или для приватного канала
TELEGRAM_CHAT_ID=-1001234567890

# Начальный блок для мониторинга
START_BLOCK=19000000
```

### 3. Запуск

```bash
docker-compose up --build
```

## Что делает бот

✅ Отслеживает новые лаунчи на контракте Liquid Protocol  
✅ Извлекает: название, описание, dev buy, картинку  
✅ Генерирует ссылки на DEXScreener и BaseScan  
✅ Отправляет красивые уведомления в Telegram  
✅ Избегает дубликатов через SQLite БД  

## Структура

```
src/
├── main.py              # Точка входа
├── config.py            # Конфигурация
├── blockchain/          # Мониторинг блокчейна
├── telegram/            # Telegram интеграция
├── utils/               # Утилиты (IPFS, БД, ссылки)
└── models/              # Модели данных
```

## Логирование

```bash
# Просмотр логов
docker-compose logs -f

# Просмотр БД
sqlite3 data/tokens.db "SELECT * FROM processed_tokens;"
```

## Требования

- Docker & Docker Compose
- Telegram Bot Token
- Chat ID для публикации

Подробнее см. [README.md](README.md)
