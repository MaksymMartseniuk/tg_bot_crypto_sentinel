🛡️ Crypto Sentinel Bot
An asynchronous Telegram bot designed for real-time cryptocurrency price monitoring and custom Signals (Alerts). Built with a focus on modular architecture, scalability, and full multi-language support.

🚀 Key Features
📈 Live Prices: Fetch real-time prices from the Binance API for any trading pair.

🔔 Signals (Alerts): Set personalized price threshold notifications (UP/DOWN).

🌍 Multi-language Support: Native support for English and Ukrainian using aiogram-i18n.

🕒 Background Monitoring: Powered by Taskiq for persistent price checking every minute, independent of bot uptime.

🗄️ Robust Storage: PostgreSQL integration for managing user accounts and active signals.

💡 Enhanced UX: Localized input field placeholders and intuitive FSM flows for seamless interaction.

🛠️ Tech Stack
Language: Python 3.14 (v3.14-dev)

Framework: aiogram 3.x

Database: PostgreSQL + SQLAlchemy (Async)

Task Management: Taskiq + Redis

Localization: GNU Gettext (Babel)

Infrastructure: Docker & Docker Compose

🏗️ Project Structure
Plaintext
├── app/
│   ├── broker/         # Taskiq broker and task definitions
│   ├── i18n/           # I18n setup and translation configurations
│   ├── database/       # SQLAlchemy models and repository requests
│   ├── handlers/       # Modular routers (user, settings, signals)
│   ├── keyboards/      # Dynamic Reply/Inline keyboard builders
│   ├── middlewares/    # Database and Localization middlewares
│   └── services/       # External APIs (Binance) and business logic
├── locales/            # Translation files (.po, .mo)
├── migrations/         # Database migration history (Alembic)
├── tests/              # Unit and integration tests for bot logic
├── bot.py              # Main entry point for the Telegram bot
├── tasks.py            # Background task definitions for Taskiq
├── Dockerfile          # Instructions for building the Docker image
├── docker-compose.yml  # Orchestration for Bot, DB, Redis, and Worker
└── .env.example        # Template for environment variables
📦 Installation & Deployment
1. Clone the Repository
Bash
git clone https://github.com/MaksymMartseniuk/tg_bot_crypto_sentinel.git
cd tg_bot_crypto_sentinel
2. Environment Setup
Create a .env file in the root directory using .env.example as a template.

3. Run with Docker
Bash
docker-compose up -d --build
🌍 Localization (Development)
To update translations or add new languages:

Bash
# Extract new strings
pybabel extract . -o locales/messages.pot

# Update translation files
pybabel update -d locales -i locales/messages.pot

# Compile into machine-readable format
pybabel compile -d locales
