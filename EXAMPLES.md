# Примеры использования Liquid Protocol Launch Bot

## Пример 1: Базовый запуск

```bash
# Клонирование
git clone <repo>
cd liquid-launch-bot

# Конфигурация
cp .env.example .env
# Отредактируйте .env с вашими данными

# Запуск
docker-compose up --build
```

## Пример 2: Проверка конфигурации перед запуском

```bash
# Проверка подключения к RPC
python -c "
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('https://mainnet.base.org'))
print(f'Connected: {w3.is_connected()}')
print(f'Latest block: {w3.eth.block_number}')
"

# Проверка Telegram бота
python -c "
import asyncio
from src.config import Config
from src.telegram.bot import TelegramNotifier

async def test():
    Config.validate()
    notifier = TelegramNotifier()
    result = await notifier.send_test_message()
    print(f'Test message sent: {result}')

asyncio.run(test())
"
```

## Пример 3: Локальный запуск для разработки

```bash
# Установка зависимостей
pip install -r requirements.txt

# Создание .env
cp .env.example .env

# Редактирование .env
# TELEGRAM_BOT_TOKEN=your_token
# TELEGRAM_CHAT_ID=your_chat_id

# Запуск
python -m src.main
```

## Пример 4: Просмотр логов

```bash
# Все логи
docker-compose logs -f

# Только последние 100 строк
docker-compose logs --tail=100

# Логи конкретного сервиса
docker-compose logs -f bot

# Сохранение логов в файл
docker-compose logs > logs.txt
```

## Пример 5: Работа с БД

```bash
# Просмотр всех обработанных токенов
sqlite3 data/tokens.db "SELECT * FROM processed_tokens;"

# Количество обработанных токенов
sqlite3 data/tokens.db "SELECT COUNT(*) FROM processed_tokens;"

# Последние 5 токенов
sqlite3 data/tokens.db "
SELECT token_address, block_number, created_at 
FROM processed_tokens 
ORDER BY created_at DESC 
LIMIT 5;
"

# Удаление конкретного токена (если нужно переобработать)
sqlite3 data/tokens.db "DELETE FROM processed_tokens WHERE token_address = '0x...';"

# Очистка всей БД
sqlite3 data/tokens.db "DELETE FROM processed_tokens;"
```

## Пример 6: Изменение START_BLOCK

Если хотите обработать исторические лаунчи:

```bash
# Отредактируйте .env
START_BLOCK=18000000  # Более ранний блок

# Очистите БД (опционально)
rm data/tokens.db

# Перезапустите
docker-compose up --build
```

## Пример 7: Использование альтернативного RPC

```env
# В .env используйте другой RPC
BASE_RPC_URL=https://base.publicnode.com
# или
BASE_RPC_URL=https://base-rpc.publicnode.com
```

## Пример 8: Изменение интервала проверки

```env
# В .env измените интервал (в секундах)
POLL_INTERVAL=6   # Проверка каждые 6 секунд (быстрее)
POLL_INTERVAL=30  # Проверка каждые 30 секунд (медленнее)
```

## Пример 9: Использование другого IPFS gateway

```env
# В .env используйте другой gateway
IPFS_GATEWAY=https://gateway.pinata.cloud/ipfs/
# или
IPFS_GATEWAY=https://cloudflare-ipfs.com/ipfs/
```

## Пример 10: Запуск нескольких экземпляров

```bash
# Создайте несколько .env файлов
cp .env.example .env.prod
cp .env.example .env.dev

# Отредактируйте каждый с разными TELEGRAM_CHAT_ID
# .env.prod: TELEGRAM_CHAT_ID=@liquid_launches_prod
# .env.dev: TELEGRAM_CHAT_ID=@liquid_launches_dev

# Запустите с разными именами сервисов
docker-compose -f docker-compose.yml -p liquid-prod up -d
docker-compose -f docker-compose.yml -p liquid-dev up -d

# Просмотр обоих
docker ps | grep liquid
```

## Пример 11: Отладка проблем

```bash
# Проверка подключения к контракту
python -c "
from web3 import Web3
from src.blockchain.contract_abi import LIQUID_FACTORY_ABI
from src.config import Config

w3 = Web3(Web3.HTTPProvider(Config.BASE_RPC_URL))
factory = w3.eth.contract(
    address=Web3.to_checksum_address(Config.LIQUID_FACTORY_ADDRESS),
    abi=LIQUID_FACTORY_ABI
)
print(f'Contract loaded: {factory.address}')
"

# Проверка последних событий
python -c "
from web3 import Web3
from src.blockchain.contract_abi import LIQUID_FACTORY_ABI
from src.config import Config

w3 = Web3(Web3.HTTPProvider(Config.BASE_RPC_URL))
factory = w3.eth.contract(
    address=Web3.to_checksum_address(Config.LIQUID_FACTORY_ADDRESS),
    abi=LIQUID_FACTORY_ABI
)

latest = w3.eth.block_number
events = factory.events.TokenCreated.get_logs(
    from_block=latest - 100,
    to_block=latest
)
print(f'Found {len(events)} events in last 100 blocks')
for event in events[-5:]:
    print(f'  Block {event[\"blockNumber\"]}: {event[\"args\"][\"name\"]}')
"
```

## Пример 12: Резервная копия БД

```bash
# Создание резервной копии
cp data/tokens.db data/tokens.db.backup

# Восстановление из резервной копии
cp data/tokens.db.backup data/tokens.db

# Архивирование
tar -czf tokens_backup_$(date +%Y%m%d).tar.gz data/tokens.db
```

## Пример 13: Мониторинг ресурсов

```bash
# Использование памяти и CPU
docker stats liquid-launch-bot_bot_1

# Размер контейнера
docker ps --size | grep liquid

# Размер БД
du -h data/tokens.db
```

## Пример 14: Обновление кода

```bash
# Получить последние изменения
git pull

# Пересобрать контейнер
docker-compose up --build

# Или с очисткой
docker-compose down
docker-compose up --build
```

## Пример 15: Полная переустановка

```bash
# Остановить и удалить все
docker-compose down --rmi all -v

# Удалить данные
rm -rf data/

# Переустановить
git pull
docker-compose up --build
```

## Полезные команды

```bash
# Проверка статуса
docker-compose ps

# Перезагрузка
docker-compose restart

# Просмотр конфигурации
docker-compose config

# Валидация docker-compose.yml
docker-compose config --quiet && echo "Valid"

# Удаление неиспользуемых образов
docker image prune -a

# Удаление неиспользуемых томов
docker volume prune
```

## Переменные окружения

```env
# Blockchain
BASE_RPC_URL              # URL RPC ноды Base
LIQUID_FACTORY_ADDRESS    # Адрес контракта Liquid Factory
START_BLOCK              # Начальный блок для мониторинга

# Telegram
TELEGRAM_BOT_TOKEN       # Токен бота (от @BotFather)
TELEGRAM_CHAT_ID         # @channel_username или -100123456 для приватного

# IPFS
IPFS_GATEWAY             # URL IPFS gateway

# Polling
POLL_INTERVAL            # Интервал проверки в секундах
```

## Контакты и поддержка

- GitHub Issues: [Создать issue](https://github.com/your-repo/issues)
- Telegram: [@YourHandle](https://t.me/YourHandle)
- Email: your-email@example.com
