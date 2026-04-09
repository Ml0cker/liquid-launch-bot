# Архитектура Liquid Protocol Launch Bot

## Обзор системы

```
┌─────────────────────────────────────────────────────────────┐
│                    Telegram Channel                          │
│                  (Публикация уведомлений)                    │
└────────────────────────────┬────────────────────────────────┘
                             │
                             │ send_message()
                             │
┌────────────────────────────▼────────────────────────────────┐
│                   TelegramNotifier                           │
│              (src/telegram/bot.py)                           │
│  - send_launch_notification()                               │
│  - send_test_message()                                      │
└────────────────────────────┬────────────────────────────────┘
                             │
                             │ format_message()
                             │
┌────────────────────────────▼────────────────────────────────┐
│                  MessageFormatter                            │
│           (src/telegram/formatter.py)                        │
│  - format_launch_message()                                  │
│  - format_error_message()                                   │
└────────────────────────────┬────────────────────────────────┘
                             │
                             │ token data
                             │
┌────────────────────────────▼────────────────────────────────┐
│                  LiquidLaunchBot                             │
│              (src/main.py)                                   │
│  - on_token_launch()                                        │
│  - start()                                                  │
└────────────────────────────┬────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Monitor    │    │  Database    │    │  IPFSHandler │
│              │    │              │    │              │
│ LiquidMonitor│    │TokenDatabase │    │ IPFSHandler  │
│              │    │              │    │              │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       │                   │                   │
       ▼                   ▼                   ▼
   Blockchain          SQLite DB          IPFS Gateway
   (Base RPC)          (tokens.db)         (ipfs.io)
```

## Компоненты

### 1. LiquidLaunchBot (src/main.py)
**Роль:** Главный оркестратор

**Ответственность:**
- Инициализация всех компонентов
- Управление жизненным циклом приложения
- Обработка callback'ов от монитора
- Координация между компонентами

**Методы:**
- `__init__()` - инициализация
- `on_token_launch(token)` - callback при новом лаунче
- `start()` - запуск бота
- `shutdown()` - корректное завершение

### 2. LiquidMonitor (src/blockchain/monitor.py)
**Роль:** Мониторинг блокчейна

**Ответственность:**
- Подключение к Base RPC
- Получение новых блоков
- Фильтрация событий TokenCreated
- Вызов callback'ов

**Методы:**
- `get_latest_block()` - получить последний блок
- `fetch_token_created_events()` - получить события
- `process_events()` - обработать события
- `start()` - запустить polling loop
- `add_callback()` - зарегистрировать callback

### 3. TokenParser (src/blockchain/token_parser.py)
**Роль:** Парсинг данных токена

**Ответственность:**
- Извлечение данных из события
- Получение on-chain метаданных
- Расчет market cap
- Преобразование в модель TokenLaunch

**Методы:**
- `parse_token_created_event()` - парсинг события
- `fetch_token_metadata()` - получить метаданные
- `calculate_market_cap()` - расчет market cap

### 4. TelegramNotifier (src/telegram/bot.py)
**Роль:** Отправка уведомлений в Telegram

**Ответственность:**
- Подключение к Telegram Bot API
- Отправка сообщений и фото
- Обработка ошибок отправки
- Форматирование сообщений

**Методы:**
- `send_launch_notification()` - отправить уведомление
- `send_test_message()` - отправить тестовое сообщение
- `_send_text_message()` - отправить текст
- `_send_photo_message()` - отправить фото

### 5. MessageFormatter (src/telegram/formatter.py)
**Роль:** Форматирование сообщений

**Ответственность:**
- Создание красивых сообщений
- Генерация ссылок
- Форматирование данных

**Методы:**
- `format_launch_message()` - форматировать сообщение о лаунче
- `format_error_message()` - форматировать ошибку

### 6. TokenDatabase (src/utils/database.py)
**Роль:** Управление SQLite БД

**Ответственность:**
- Инициализация БД
- Проверка дубликатов
- Сохранение обработанных токенов
- Получение статистики

**Методы:**
- `init_db()` - инициализировать БД
- `is_token_processed()` - проверить дубликат
- `mark_token_processed()` - сохранить токен
- `get_processed_count()` - получить количество

### 7. IPFSHandler (src/utils/ipfs.py)
**Роль:** Загрузка изображений из IPFS

**Ответственность:**
- Загрузка изображений
- Сохранение во временные файлы
- Обработка ошибок

**Методы:**
- `download_image()` - загрузить изображение
- `save_temp_image()` - сохранить файл
- `get_image_path()` - получить путь к изображению

### 8. DEXScreenerHelper (src/utils/dexscreener.py)
**Роль:** Генерация ссылок

**Ответственность:**
- Создание ссылок на DEXScreener
- Создание ссылок на BaseScan

**Методы:**
- `generate_dexscreener_link()` - ссылка на DEXScreener
- `generate_basescan_link()` - ссылка на контракт
- `generate_basescan_tx_link()` - ссылка на транзакцию

### 9. Config (src/config.py)
**Роль:** Управление конфигурацией

**Ответственность:**
- Загрузка переменных окружения
- Валидация конфигурации
- Предоставление констант

**Методы:**
- `validate()` - проверить конфигурацию

### 10. TokenLaunch (src/models/token.py)
**Роль:** Модель данных

**Ответственность:**
- Хранение данных о токене
- Типизация данных

**Поля:**
- address, name, symbol, description
- image_uri, market_cap, dev_buy
- block_number, transaction_hash
- pool_address, deployer, hook_address, locker_address

## Поток данных

```
1. LiquidMonitor.start()
   ↓
2. get_latest_block() → Base RPC
   ↓
3. fetch_token_created_events() → Base RPC
   ↓
4. process_events()
   ↓
5. TokenParser.parse_token_created_event()
   ↓
6. TokenLaunch model
   ↓
7. LiquidLaunchBot.on_token_launch()
   ↓
8. TokenDatabase.is_token_processed()
   ↓
9. IPFSHandler.get_image_path() → IPFS Gateway
   ↓
10. TelegramNotifier.send_launch_notification()
    ↓
11. MessageFormatter.format_launch_message()
    ↓
12. Telegram Bot API → Telegram Channel
    ↓
13. TokenDatabase.mark_token_processed()
    ↓
14. SQLite DB
```

## Взаимодействие компонентов

### Инициализация
```
main()
  ↓
LiquidLaunchBot.__init__()
  ├─ Web3(RPC_URL)
  ├─ LiquidMonitor(w3)
  ├─ TelegramNotifier()
  ├─ TokenDatabase()
  ├─ IPFSHandler()
  └─ monitor.add_callback(on_token_launch)
```

### Обработка события
```
LiquidMonitor.start()
  ↓
fetch_token_created_events()
  ↓
process_events()
  ↓
TokenParser.parse_token_created_event()
  ↓
on_token_launch(token)
  ├─ is_token_processed()
  ├─ get_image_path()
  ├─ send_launch_notification()
  │  └─ format_launch_message()
  └─ mark_token_processed()
```

## Обработка ошибок

```
try:
  fetch_token_created_events()
except Exception:
  logger.error()
  return []

try:
  send_launch_notification()
except TelegramError:
  logger.error()
  fallback to text message

try:
  download_image()
except Exception:
  logger.warning()
  return None
```

## Масштабируемость

### Текущие ограничения
- Один процесс Python
- Один Telegram канал
- Polling каждые 12 секунд

### Возможные улучшения
- Несколько экземпляров с разными START_BLOCK
- Webhook вместо polling
- Кэширование данных
- Асинхронная обработка событий
- Метрики и мониторинг

## Безопасность

### Текущие меры
- Переменные окружения для чувствительных данных
- Валидация конфигурации
- Обработка исключений
- Логирование ошибок

### Рекомендации
- Использовать отдельный бот для каждого окружения
- Ограничить доступ к .env файлу
- Регулярно ротировать токены
- Мониторить логи на ошибки
- Использовать VPN для RPC подключения

## Производительность

### Текущие метрики
- Время обработки события: <1 сек
- Загрузка изображения: 1-5 сек
- Отправка сообщения: <1 сек
- Использование памяти: ~100-150 MB
- Использование диска: ~10 MB

### Оптимизация
- Кэширование изображений
- Батчинг событий
- Асинхронная загрузка изображений
- Сжатие БД

## Развертывание

### Docker
```
Dockerfile
  ├─ FROM python:3.11-slim
  ├─ COPY requirements.txt
  ├─ pip install
  ├─ COPY src/
  └─ CMD python -m src.main

docker-compose.yml
  ├─ build: .
  ├─ env_file: .env
  ├─ volumes: ./data:/app/data
  └─ restart: unless-stopped
```

### Локально
```
pip install -r requirements.txt
python -m src.main
```

## Мониторинг

### Логирование
- INFO: основные события
- DEBUG: детальная информация
- ERROR: ошибки
- WARNING: предупреждения

### Метрики
- Количество обработанных токенов
- Время обработки события
- Ошибки отправки
- Использование ресурсов

## Тестирование

### Unit тесты
- TokenParser
- MessageFormatter
- DEXScreenerHelper

### Интеграционные тесты
- LiquidMonitor + Web3
- TelegramNotifier + Telegram API
- TokenDatabase + SQLite

### E2E тесты
- Полный цикл от события до уведомления
