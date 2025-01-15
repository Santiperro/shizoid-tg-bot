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
        "temperature": 0.85
    },
    "llama32_90":{
        "base_url": "https://api.groq.com/openai/v1",
        "api_key_env": "GROQ_KEY",
        "default_model": "llama-3.2-90b-vision-preview",
        "max_tokens": 512,
        "temperature": 0.05
    }
}

SELECTED_TEXT_TO_TEXT_API = "llama33_70"
SELECTED_IMAGE_TO_TEXT_API = "llama32_90"

REDIS_HOST = "localhost"
REDIS_PORT = 6379

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

# Бот обрабатывает и отвечает на картинку, если текст меньше 
CAPTION_MAX_LENGTH = 100

# Минимальная длина сообщения без картинки для ответа
COMMON_MESSAGE_MIN_LENGTH = 100
# Максимальная длина сообщения для ответа
COMMON_MESSAGE_MAX_LENGTH = 2000
# Шанс ответа
COMMON_GROUP_MESSAGE_REPLY_CHANCE = 0.1

# Минимальная длина forward сообщения без картинки для ответа
FORWARD_MESSAGE_MIN_LENGTH = 100
# Максимальная длина forward сообщения для ответа
FORWARD_MESSAGE_MAX_LENGTH = 2000
# Шанс ответа на forward сообщение
FORWARD_MESSAGE_REPLY_CHANCE = 1

# Разрешить ответ на reply или упоминание
ALLOW_REPLY_OR_MENTION = False
# Минимальная длина сообщения с reply или упоминанием без картинки для ответа
REPLY_OR_MENTION_MESSAGE_MIN_LENGTH = 100
# Максимальная длина сообщения с reply или упоминанием для ответа
REPLY_OR_MENTION_MESSAGE_MAX_LENGTH = 2000
# Шанс ответа на reply или упоминание
REPLY_OR_MENTION_MESSAGE_REPLY_CHANCE = 1

# Длина истории сообщений, которую помнит бот
CHAT_HISTORY_LENGTH = 0

# Временное окно в секундах для взаимодействия с пользователем в групповом чате
GROUP_CHAT_TIME_WINDOW_SECONDS = 600
# Максимальное количество сообщений за время окна
GROUP_CHAT_MESSAGE_LIMIT = 20

# Временное окно в секундах для взаимодействия с пользователем в личном чате
PRIVATE_CHAT_TIME_WINDOW_SECONDS = 60
# Максимальное количество сообщений за время окна
PRIVATE_CHAT_MESSAGE_LIMIT = 30