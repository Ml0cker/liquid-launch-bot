# Инструкция: Запуск бота для публичного Telegram канала

## Шаг 1: Создание публичного канала

1. Откройте Telegram
2. Нажмите на меню (три полоски)
3. Выберите "Создать канал"
4. Введите название (например: "Liquid Launches")
5. Выберите "Публичный канал"
6. Введите username (например: `liquid_launches`)
7. Нажмите "Создать"

**Важно:** Username должен быть уникальным и содержать только буквы, цифры и подчеркивания.

## Шаг 2: Получение Telegram Bot Token

1. Откройте Telegram и найдите **@BotFather**
2. Отправьте команду `/newbot`
3. Следуйте инструкциям:
   - Введите имя бота (например: "Liquid Launch Bot")
   - Введите username (должен заканчиваться на "_bot", например: "liquid_launch_bot")
4. Скопируйте полученный токен (выглядит как: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

## Шаг 3: Добавление бота в канал

1. Откройте ваш канал (например: @liquid_launches)
2. Нажмите на название канала (вверху)
3. Выберите "Администраторы"
4. Нажмите "Добавить администратора"
5. Найдите вашего бота (например: @liquid_launch_bot)
6. Выберите его
7. Дайте права:
   - ✅ Отправлять сообщения
   - ✅ Редактировать сообщения
   - ✅ Удалять сообщения
   - ✅ Отправлять медиа
8. Нажмите "Готово"

## Шаг 4: Конфигурация бота

```bash
# Перейдите в директорию проекта
cd "c:\2026\Liquid deploys"

# Создайте .env файл
cp .env.example .env
```

Отредактируйте `.env`:

```env
# Blockchain
BASE_RPC_URL=https://mainnet.base.org
LIQUID_FACTORY_ADDRESS=0x04f1a284168743759be6554f607a10cebdb77760
START_BLOCK=19000000

# Telegram
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=@liquid_launches

# IPFS
IPFS_GATEWAY=https://ipfs.io/ipfs/

# Polling
POLL_INTERVAL=12
```

**Замените:**
- `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` на ваш токен от @BotFather
- `@liquid_launches` на username вашего канала

## Шаг 5: Запуск бота

```bash
# Сборка и запуск
docker-compose up --build

# Или запуск в фоне
docker-compose up -d --build
```

## Шаг 6: Проверка работы

1. **Проверьте логи:**
```bash
docker-compose logs -f
```

Должны увидеть:
```
INFO - Initializing Liquid Launch Bot...
INFO - Bot initialized successfully
INFO - Starting Liquid Protocol monitor from block 19000000
INFO - Test message sent successfully
```

2. **Проверьте канал:**
   - Откройте ваш канал (@liquid_launches)
   - Должно появиться сообщение: "✅ Liquid Protocol Launch Bot is running!"

3. **Проверьте БД:**
```bash
sqlite3 data/tokens.db "SELECT COUNT(*) FROM processed_tokens;"
```

## Шаг 7: Тестирование с реальным лаунчем

1. Дождитесь нового лаунча на Liquid Protocol
2. Проверьте, что уведомление пришло в канал в течение 30 секунд
3. Проверьте, что все данные корректны:
   - Название и символ токена
   - Описание
   - Dev buy
   - Блок
   - Ссылки на DEXScreener и BaseScan
   - Изображение (если доступно)

## Полезные команды

```bash
# Просмотр логов в реальном времени
docker-compose logs -f

# Просмотр последних 100 строк логов
docker-compose logs --tail=100

# Остановка бота
docker-compose down

# Перезагрузка бота
docker-compose restart

# Удаление всех данных (осторожно!)
docker-compose down -v
rm -rf data/
```

## Решение проблем

### Бот не отправляет сообщения в канал

1. **Проверьте токен:**
   - Убедитесь, что TELEGRAM_BOT_TOKEN скопирован полностью
   - Проверьте, что нет пробелов в начале/конце

2. **Проверьте username канала:**
   - Убедитесь, что TELEGRAM_CHAT_ID = `@liquid_launches` (с @)
   - Проверьте, что username написан правильно

3. **Проверьте права бота:**
   - Откройте канал → Администраторы
   - Убедитесь, что бот есть в списке
   - Убедитесь, что у бота есть права на отправку сообщений

4. **Проверьте логи:**
```bash
docker-compose logs -f | grep -i error
```

### Ошибка: "Chat not found"

- Убедитесь, что канал публичный
- Убедитесь, что username канала правильный
- Попробуйте добавить бота в канал вручную

### Ошибка: "Bot was kicked from the supergroup"

- Откройте канал → Администраторы
- Добавьте бота заново
- Дайте ему необходимые права

### Нет подключения к RPC

1. Проверьте интернет соединение
2. Попробуйте альтернативный RPC:
```env
BASE_RPC_URL=https://base.publicnode.com
```

## Мониторинг

### Просмотр обработанных токенов

```bash
sqlite3 data/tokens.db "
SELECT token_address, block_number, created_at 
FROM processed_tokens 
ORDER BY created_at DESC 
LIMIT 10;
"
```

### Статистика

```bash
sqlite3 data/tokens.db "SELECT COUNT(*) as total_tokens FROM processed_tokens;"
```

### Использование ресурсов

```bash
docker stats
```

## Обновление бота

```bash
# Получить последние изменения
git pull

# Пересобрать контейнер
docker-compose up --build
```

## Остановка и удаление

```bash
# Остановить контейнер
docker-compose down

# Удалить контейнер и образ
docker-compose down --rmi all

# Удалить все данные (осторожно!)
docker-compose down -v
rm -rf data/
```

## Безопасность

⚠️ **Важно:**
- Никогда не коммитьте `.env` файл с реальным токеном
- Используйте отдельный бот для каждого канала
- Ограничьте доступ к файлу `.env`
- Регулярно ротируйте токены (если нужно)

## Поддержка

Если возникли проблемы:
1. Проверьте логи: `docker-compose logs -f`
2. Убедитесь, что все переменные в `.env` заполнены
3. Проверьте документацию: `README.md`, `DEPLOYMENT.md`
4. Создайте Issue в репозитории

## Дополнительные ресурсы

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegram Bot Features](https://core.telegram.org/bots/features)
- [Liquid Protocol](https://liquidprotocol.org)
- [Base Chain](https://base.org)

---

**Готово!** Ваш бот теперь будет автоматически публиковать новые лаунчи в канал 🚀
