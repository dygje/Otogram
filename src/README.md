# Source Code Directory

This directory contains all the source code for the Telegram Automation System.

## Structure

```
src/
├── core/           # Core system components
│   ├── config.py   # Configuration management
│   └── database.py # Database connection and management
├── models/         # Data models (Pydantic)
│   ├── base.py     # Base model class
│   ├── message.py  # Message-related models
│   ├── group.py    # Group-related models
│   ├── blacklist.py# Blacklist-related models
│   ├── config.py   # Configuration models
│   └── log.py      # Logging models
├── services/       # Business logic layer
│   ├── message_service.py   # Message CRUD operations
│   ├── group_service.py     # Group CRUD operations
│   ├── blacklist_service.py # Blacklist management
│   └── config_service.py    # Configuration management
└── telegram/       # Telegram integration
    ├── bot_manager.py    # Main bot manager
    ├── management_bot.py # Telegram bot interface
    ├── userbot.py        # MTProto userbot
    └── handlers/         # Bot command handlers
        ├── message_handlers.py   # Message management
        ├── group_handlers.py     # Group management
        ├── blacklist_handlers.py # Blacklist management
        └── config_handlers.py    # Configuration management
```

## Key Components

- **core/**: Essential system components (config, database)
- **models/**: Data validation and structure using Pydantic
- **services/**: Business logic separated from presentation layer
- **telegram/**: All Telegram-related functionality (bot + userbot)

This follows clean architecture principles with clear separation of concerns.