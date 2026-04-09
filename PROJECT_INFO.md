# Liquid Protocol Launch Bot - Информация о проекте

## Описание

Полнофункциональный Telegram бот для автоматического мониторинга новых лаунчей токенов на Liquid Protocol (Base chain). Бот отслеживает события `TokenCreated` на контракте Liquid Protocol Factory и отправляет красивые уведомления в Telegram канал с полной информацией о новых токенах.

## Основные возможности

✅ **Автоматический мониторинг** - отслеживание новых лаунчей в реальном времени  
✅ **Полная информация** - название, описание, dev buy, картинка, блок  
✅ **Быстрые ссылки** - DEXScreener, BaseScan, транзакция  
✅ **IPFS интеграция** - загрузка изображений токенов  
✅ **Защита от дубликатов** - SQLite БД для отслеживания  
✅ **Docker контейнеризация** - легкое развертывание  
✅ **Асинхронная обработка** - быстрая обработка событий  
✅ **Обработка ошибок** - надежная работа 24/7  

## Технический стек

- **Python 3.11** - основной язык
- **Web3.py** - взаимодействие с блокчейном
- **python-telegram-bot** - Telegram API
- **SQLite** - хранение данных
- **Docker** - контейнеризация
- **asyncio** - асинхронная обработка

## Структура проекта

```
liquid-launch-bot/
├── src/
│   ├── main.py                 # Главный модуль (точка входа)
│   ├── config.py               # Конфигурация из .env
│   ├── blockchain/
│   │   ├── monitor.py          # Мониторинг событий
│   │   ├── token_parser.py     # Парсинг данных токена
│   │   └── contract_abi.py     # ABI контракта
│   ├── telegram/
│   │   ├── bot.py              # Telegram бот
│   │   └── formatter.py        # Форматирование сообщений
│   ├── utils/
│   │   ├── database.py         # SQLite БД
│   │   ├── ipfs.py             # IPFS загрузка
│   │   └── dexscreener.py      # Генерация ссылок
│   └── models/
│       └── token.py            # Модель TokenLaunch
├── docker-compose.yml          # Docker Compose конфигурация
├── Dockerfile                  # Docker образ
├── requirements.txt            # Python зависимости
├── .env.example                # Шаблон конфигурации
├── .gitignore                  # Git исключения
├── README.md                   # Основная документация
├── QUICKSTART.md               # Быстрый старт
├── DEPLOYMENT.md               # Инструкция развертывания
├── ARCHITECTURE.md             # Архитектура системы
├── EXAMPLES.md                 # Примеры использования
├── CHECKLIST.md                # Чек-лист развертывания
└── PROJECT_INFO.md             # Этот файл
```

## Быстрый старт

### 1. Подготовка

```bash
# Клонирование
git clone <repo>
cd liquid-launch-bot

# Создание .env
cp .env.example .env
```

### 2. Конфигурация

Отредактируйте `.env`:
```env
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=-1001234567890
START_BLOCK=19000000
```

### 3. Запуск

```bash
docker-compose up --build
```

## Компоненты

### LiquidMonitor
Отслеживает новые блоки и события `TokenCreated` на контракте Liquid Protocol Factory.

### TokenParser
Извлекает данные из события и преобразует их в модель `TokenLaunch`.

### TelegramNotifier
Отправляет уведомления в Telegram канал с информацией о новом токене.

### TokenDatabase
Хранит информацию об обработанных токенах для избежания дубликатов.

### IPFSHandler
Загружает изображения токенов из IPFS.

## Поток данных

```
Base RPC → LiquidMonitor → TokenParser → TokenLaunch
                                            ↓
                                    TokenDatabase (проверка)
                                            ↓
                                    IPFSHandler (изображение)
                                            ↓
                                    TelegramNotifier
                                            ↓
                                    Telegram Channel
                                            ↓
                                    TokenDatabase (сохранение)
```

## Конфигурация

### Обязательные переменные

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=-1001234567890
```

### Опциональные переменные

```env
BASE_RPC_URL=https://mainnet.base.org
LIQUID_FACTORY_ADDRESS=0x04f1a284168743759be6554f607a10cebdb77760
START_BLOCK=19000000
IPFS_GATEWAY=https://ipfs.io/ipfs/
POLL_INTERVAL=12
```

## Требования

- Docker & Docker Compose
- Telegram Bot Token (от @BotFather)
- Chat ID для публикации
- Интернет соединение

## Установка зависимостей

```bash
pip install -r requirements.txt
```

### Основные зависимости

- web3==6.11.3 - взаимодействие с блокчейном
- python-telegram-bot==20.7 - Telegram API
- python-dotenv==1.0.0 - загрузка .env
- requests==2.31.0 - HTTP запросы
- Pillow==10.1.0 - работа с изображениями

## Использование

### Docker Compose (рекомендуется)

```bash
# Запуск
docker-compose up --build

# Запуск в фоне
docker-compose up -d --build

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

### Локальный запуск

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск
python -m src.main
```

## Логирование

Логи выводятся в консоль с форматом:
```
2026-04-09 12:34:56,789 - src.blockchain.monitor - INFO - Found 1 TokenCreated events
```

Уровни логирования:
- `INFO` - основные события
- `DEBUG` - детальная информация
- `WARNING` - предупреждения
- `ERROR` - ошибки

## База данных

SQLite база хранится в `data/tokens.db` с таблицей:

```sql
CREATE TABLE processed_tokens (
    token_address TEXT PRIMARY KEY,
    block_number INTEGER NOT NULL,
    transaction_hash TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

## Производительность

- **Время обработки события:** <1 сек
- **Загрузка изображения:** 1-5 сек
- **Отправка сообщения:** <1 сек
- **Использование памяти:** ~100-150 MB
- **Использование диска:** ~10 MB (без изображений)
- **Интервал проверки:** ~12 сек (время блока Base ~2 сек)

## Безопасность

- Переменные окружения для чувствительных данных
- Валидация конфигурации при запуске
- Обработка исключений для всех операций
- Логирование ошибок для отладки
- .gitignore для исключения .env файла

## Мониторинг

### Проверка статуса

```bash
# Статус контейнера
docker-compose ps

# Использование ресурсов
docker stats

# Размер БД
du -h data/tokens.db

# Количество обработанных токенов
sqlite3 data/tokens.db "SELECT COUNT(*) FROM processed_tokens;"
```

## Решение проблем

### Бот не отправляет сообщения
1. Проверьте TELEGRAM_BOT_TOKEN
2. Проверьте TELEGRAM_CHAT_ID
3. Убедитесь, что бот добавлен в канал
4. Проверьте логи: `docker-compose logs -f`

### Нет подключения к RPC
1. Проверьте интернет соединение
2. Проверьте BASE_RPC_URL
3. Попробуйте альтернативный RPC

### Изображения не загружаются
1. Это нормально, если IPFS недоступен
2. Сообщение все равно будет отправлено
3. Попробуйте другой IPFS gateway

## Обновление

```bash
# Получить последние изменения
git pull

# Пересобрать контейнер
docker-compose up --build
```

## Лицензия

MIT

## Автор

Создано для Liquid Protocol

## Поддержка

Для вопросов и проблем:
1. Проверьте документацию (README.md, DEPLOYMENT.md)
2. Проверьте логи: `docker-compose logs -f`
3. Создайте Issue в репозитории

## Дополнительные ресурсы

- [Liquid Protocol](https://liquidprotocol.org)
- [Base Chain](https://base.org)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Web3.py Documentation](https://web3py.readthedocs.io)
- [IPFS](https://ipfs.io)

## История версий

### v1.0.0 (2026-04-09)
- Первый релиз
- Основной функционал мониторинга
- Интеграция с Telegram
- Docker поддержка

## Планы развития

- [ ] Webhook вместо polling
- [ ] Кэширование данных
- [ ] Метрики и мониторинг
- [ ] Веб-интерфейс
- [ ] Поддержка нескольких каналов
- [ ] Фильтрация по параметрам
- [ ] Уведомления по email
- [ ] Интеграция с другими сервисами

## Благодарности

Спасибо Liquid Protocol за отличный протокол!

---

**Последнее обновление:** 2026-04-09  
**Версия:** 1.0.0  
**Статус:** Production Ready
