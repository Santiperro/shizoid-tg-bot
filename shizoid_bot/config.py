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

SELECTED_API = "llama33_70"

REPLY_CHANCE = 0.1

CHAT_HISTORY_LENGTH = 3

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