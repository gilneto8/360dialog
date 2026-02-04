# 360dialog Chatbot

## Description

A Chatbot application for 360dialog.

## Setup

### Your Environment Variables

- Create an `.env` file with the following content. The content below will work as-is, as long as you create your API key. Follow [this documentation](https://docs.360dialog.com/docs/get-started/sandbox#how-to-get-started-with-sandbox) to get your API key.
```toml
# =============================
# 360DIALOG CONFIGS
# =============================
API_KEY="<YOUR_D360_API_KEY>"
WA_API_URL="https://waba-sandbox.360dialog.io/v1/messages"

# =============================
# DATABASE CONFIGS
# =============================
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=chatbot
```

### Install Dependencies
```bash
> python -m venv .venv
> source .venv/bin/activate
(.venv) > pip install poetry make
(.venv) > make install
(.venv) > make test
```

### Linting & Formatting
```bash
(.venv) > make lint    # Check for issues
(.venv) > make format  # Auto-fix issues
```

### Start App

1. We need to create a tunnel between our local machine and the 360Dialog sandbox:
```bash
# Two options here: ngrok
> ngrok http 8000
# Or localtunnel
> npx localtunnel --port 8000
# Both these commands will output a URL - copy it, and leave this terminal open
# Then, run the following command:
> curl -X POST https://waba-sandbox.360dialog.io/v1/configs/webhook \
    -H "D360-API-KEY: <YOUR_D360_API_KEY>" \
    -H "Content-Type: application/json" \
    -d '{"url": "<YOUR_TUNNEL_URL>/webhook"}'  # don't forget /webhook!
```

2. Now we can start the application:
```sh
(.venv) > docker compose up -d  # To start the database 
(.venv) > uvicorn src.app.main:app --reload --port 8000  # To start the server specifically on port 8000
```

3. Now, sending a message to the 360Dailog sandbox number (`+551146733492`) should yield results through the server logs.

## Structure

```
360dialog/
├── docker-compose.yml          # Docker composition (database)
├── Makefile                    # Make commands for install, test, lint
├── pyproject.toml              # Dependencies and config
├── README.md                   # This file
├── src/
│   └── app/
│       ├── bot/
│       │   ├── handlers/       # Command logic (add, list, update, remove, free, help)
│       │   ├── parsers/        # Argument parsing & NLP date parsing utils
│       │   └── ...
│       ├── clients/
│       │   └── whatsapp.py     # 360dialog WhatsApp API Wrapper
│       ├── db/
│       │   ├── models.py       # Database models (Event)
│       │   └── session.py      # Database session management
│       ├── config.py           # Application configuration
│       └── main.py             # FastAPI Entry Point & Webhook Handler
└── tests/                      # Pytest suite
```

## Implemented Features

- **WhatsApp Integration**:
    - Webhook endpoint (`/webhook`) to receive incoming messages.
    - `WhatsAppClient` to send text replies via 360dialog API.
- **Event Management**:
    - **Add Events**: `add --title "..." --start "..."` with smart date parsing (e.g., "Feb 7", "Tuesday 15:00", "2026-02-07 15:00").
    - **List Events**: View upcoming events formatted in a readable way.
    - **Update Events**: Update existing events by title (remove + add flow).
    - **Remove Events**: Delete specific events or all events.
    - **Free Time**: Free time between start and end dates.
    - **Help**: Display help message with available commands.
- **Smart Logic**:
    - **Clash Detection**: Warns if a new event overlaps with an existing one.
    - **Date Parsing**: Robust custom parser supporting various formats (ISO, relative days, month names).
- **Persistence**:
    - SQL Database storage using SQLAlchemy (supports SQLite/Postgres).

## Missing / Next Steps

- **Authentication & Security**:
    - Verify 360dialog webhook signatures.
    - User authentication (currently any sender can modify the DB).
- **Advanced Parsing**:
    - Integration with event platforms (e.g., Google Calendar) to parse events from URLs directly.
- **Production Readiness**:
    - Dockerize the application server (currently running `uvicorn` locally).
    - CI/CD pipeline.

