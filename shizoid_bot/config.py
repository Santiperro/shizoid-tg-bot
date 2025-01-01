API_CONFIG = {
    "openai": {
        "base_url": None,
        "api_key_env": "OPENAI_KEY",
        "default_model": "gpt-4o-mini",
        "max_tokens": 200,
        "temperature": 0.7
    },
    "llama31_70": {
        "base_url": "https://openrouter.ai/api/v1",
        "api_key_env": "LLAMA31_70_OPEN_ROUTER_KEY",
        "default_model": "meta-llama/llama-3.1-70b-instruct:free",
        "max_tokens": None,
        "temperature": 0.7
    },
    "llama31_405": {
        "base_url": "https://openrouter.ai/api/v1",
        "api_key_env": "LLAMA31_405_OPEN_ROUTER_KEY",
        "default_model": "meta-llama/llama-3.1-405b-instruct:free",
        "max_tokens": None,
        "temperature": 0.7
    },
    "llama33_70": {
        "base_url": "https://api.groq.com/openai/v1",
        "api_key_env": "GROQ_KEY",
        "default_model": "llama-3.3-70b-versatile",
        "max_tokens": None,
        "temperature": 0.7
    },
}

REDIS_HOST = "localhost"
REDIS_PORT = 6379

SELECTED_API = "llama33_70"

DEFAULT_BOT_RIGHTS = [
    # "promote_members",
    # "delete_messages",
    # "restrict_members",
    # "invite_users",
    "pin_messages",
    # "manage_video_chats",
    # "manage_call",
    # "manage_topics",
    # "anonymous",
    # "add_admins",
    # 'post_stories',
    # 'delete_stories'
]

# Условия для того, чтобы бот ответил на случайное сообщение
# Шанс срабатывает при выполнение всех остальных условий

# Длина сообщения для ответа
REPLY_MESSAGE_LENGTH = 70
# Шанс ответа
REPLY_CHANCE = 0.2

# Длина forward сообщения для ответа
FORWARD_MESSAGE_LENGTH = 70
# Шанс ответа на forward сообщение
FORWARD_CHANCE = 0.5

# Длина истории сообщений, которую помнит бот
CHAT_HISTORY_LENGTH = 0

# Ограничения на ответ бота на его упоминание или reply

# Максимальное количество сообщений за время окна
MESSAGE_LIMIT = 2
# Временное окно в секундах
TIME_WINDOW_SECONDS = 600