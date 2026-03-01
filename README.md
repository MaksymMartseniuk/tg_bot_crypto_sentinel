<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">


# TG_BOT_CRYPTO_SENTINEL

<em>Empowering Smarter Crypto Decisions in Real Time</em>

<!-- BADGES -->
<img src="https://img.shields.io/github/last-commit/MaksymMartseniuk/tg_bot_crypto_sentinel?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/MaksymMartseniuk/tg_bot_crypto_sentinel?style=flat&color=0080ff" alt="repo-top-language">
<img src="https://img.shields.io/github/license/MaksymMartseniuk/tg_bot_crypto_sentinel?style=flat&color=0080ff" alt="license">

<em>Built with the tools and technologies:</em>

<img src="https://img.shields.io/badge/Python-3.14-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/aiogram-3.x-2C5BB4.svg?style=flat&logo=telegram&logoColor=white" alt="aiogram">
<img src="https://img.shields.io/badge/PostgreSQL-4169E1.svg?style=flat&logo=PostgreSQL&logoColor=white" alt="PostgreSQL">
<img src="https://img.shields.io/badge/Redis-FF4438.svg?style=flat&logo=Redis&logoColor=white" alt="Redis">
<img src="https://img.shields.io/badge/SQLAlchemy-D71F00.svg?style=flat&logo=SQLAlchemy&logoColor=white" alt="SQLAlchemy">
<img src="https://img.shields.io/badge/Taskiq-0A9EDC.svg?style=flat&logo=python&logoColor=white" alt="Taskiq">
<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=Docker&logoColor=white" alt="Docker">
<img src="https://img.shields.io/badge/Pytest-0A9EDC.svg?style=flat&logo=Pytest&logoColor=white" alt="Pytest">
<img src="https://img.shields.io/badge/AIOHTTP-2C5BB4.svg?style=flat&logo=AIOHTTP&logoColor=white" alt="AIOHTTP">

</div>
<br>

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Environment Configuration](#environment-configuration)
    - [Usage](#usage)
    - [Testing](#testing)
    - [Localization](#localization)

---

## Overview

TG_BOT_CRYPTO_SENTINEL is a robust, asynchronous Telegram bot designed for real-time cryptocurrency price monitoring and automated Signals (Alerts). It utilizes a modular architecture to orchestrate data fetching from Binance, persistent storage in PostgreSQL, and background task scheduling.

**Key Features:**

This project empowers developers to create reliable, multilingual crypto monitoring solutions with ease. The core features include:

- 🧩 **Modular Architecture:** Clear separation of concerns between database logic, handlers, and external services.

- 🌐 **Internationalization:** Full English and Ukrainian support using aiogram-i18n and Babel.

- 🚀 **Real-Time Signals:** High-performance price monitoring powered by Taskiq and Redis.

- 🐳 **Dockerized:** Ready for production with multi-container Docker Compose orchestration.

- 📱 **Intuitive UI:** Advanced FSM flows and localized input field placeholders for a seamless user experience.

---

## Project Structure
```
├── app/
│   ├── broker/         # Taskiq broker and task definitions
│   ├── i18n/           # I18n setup and translation configurations
│   ├── database/       # SQLAlchemy models and repository requests
│   ├── handlers/       # Modular routers (user, settings, alerts)
│   ├── keyboards/      # Dynamic Reply/Inline keyboard builders
│   ├── middlewares/    # Database and Localization middlewares
│   └── services/       # External APIs (Binance) and business logic
├── locales/            # Translation files (.po, .mo)
├── migrations/         # Database migration history (Alembic)
├── tests/              # Unit and integration tests for bot logic
├── bot.py              # Main bot entry point
├── Dockerfile          # Bot container definition
└── docker-compose.yml  # Full stack orchestration
```

## Getting Started

### Prerequisites

This project requires the following dependencies:

- **Programming Language:** Python: 3.12 or higher (developed on 3.14-dev)
- **Tools:** Docker & Docker Compose and Pip
- **Services:** Access to a PostgreSQL database and Redis

### Installation

Build tg_bot_crypto_sentinel from the source and install dependencies:

1. **Clone the repository:**

    ```sh
    ❯ git clone https://github.com/MaksymMartseniuk/tg_bot_crypto_sentinel
    ```

2. **Navigate to the project directory:**

    ```sh
    ❯ cd tg_bot_crypto_sentinel
    ```

3. **Install the dependencies:**

**Using [pip](https://pypi.org/project/pip/):**

```sh
❯ pip install -r requirements.txt
```
4. **Setup environment variables:**

```Create a .env file based on .env.example```

5 **Deploy using Docker (Recommended):**
```sh
❯ docker-compose up -d --build
```

### Environment Configuration

Create a `.env` file in the root directory using the template below:
```env
# Telegram Bot Configuration
BOT_TOKEN=your_telegram_bot_token

# Database Configuration
DATABASE=postgresql+asyncpg://user:password@localhost:5432/db_name

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```



### Usage

Run the project with:

**Using [docker](https://www.docker.com/):**

```sh
docker run -it {image_name}
```
**Using [pip](https://pypi.org/project/pip/):**

```sh
python bot.py
```

### Testing

Tg_bot_crypto_sentinel uses the pytest test framework. Run the test suite with:

**Using [docker](https://www.docker.com/):**

```sh
pytest tests/
```

---

### Localization

Update translations on your development machine:
```sh
# Extract new strings
pybabel extract . -o locales/messages.pot

# Update .po files
pybabel update -d locales -i locales/messages.pot

# Compile to .mo
pybabel compile -d locales
```

<div align="left"><a href="#top">⬆ Return</a></div>

---
