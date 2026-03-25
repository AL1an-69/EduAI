# EduAI — Документация для разработчиков

## Информация о сервере
| | |
|---|---|
| **IP** | 89.208.97.45 |
| **ОС** | Ubuntu 24.04 |
| **RAM** | 2 GB |
| **CPU** | 1 core |
| **Хранилище** | 30 GB |

---

## Подключение к серверу

```bash
ssh root@89.208.97.45
```

Введи `ROOT_PASSWORD` когда запросит пароль.

---

## Работа с репозиторием на сервере

Подтянуть последние изменения с GitHub:

```bash
cd /путь/до/проекта
git pull origin master
```


---

## Локальная разработка

### 1. Установка uv

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Клонировать репозиторий

```bash
git clone https://github.com/your-repo/eduai.git
cd eduai
```

### 3. Установить зависимости из pyproject.toml

```bash
uv sync
```

### 4. Создать .env файл

```
TELEGRAM_TOKEN=твой_токен
CHATGPT_TOKEN=твой_токен_openrouter
```

### 5. Запустить бота

```bash
python bot/run.py
```

---

> Все ключи и пароли (ROOT_PASSWORD, TELEGRAM_TOKEN, DEEPSEEK_TOKEN) — спрашивать у @AL1an69
