# Shizoid Telegram Bot (в разработке)

Шизоид — это ТГ-бот на aiogram 3 и тот самый интернет-тролль, который все знает и пытается навязать<br>
вам свое мнение по любому поводу. У него всегда найдется время и силы ответить на ваши сообщения <br>
в чате, прокомментировать новости и даже картинки с мемами, чтобы внести небольшой хаос в групповой чат.<br>

Для работы с текстом бот может использовать gpt4o-mini или модели Llama, <br>
которые указаны в конфигурации. Для работы с изображениями пока изначально доступна <br>
только Llama-3.2 90b Vision Preview. Также бот имеет Rate Limit систему по чатам <br>
и пользователям, использующую Redis, которая позволит ограничивать запросы и сохранить ваши токены.

## Основные функции
Бот может отвечать на reply или упоминания в групповом чате, обычные сообещния <br>
с заданным шансом и Forward сообщения с текстом и картинками. <br>
При общении бот помнит вашу историю сообщений.

## Настройка
При желании вы можете сами внести любого провайдера API для модели в config.py, <br>
если он совместим с библиотекой OpenAI. Еще вы можете указать другие тонкие настройки, например, <br>
минимальную длину сообщения для ответа или шанс ответа бота на какой-либо тип сообщения в чате.<br>
Наилучшее качество ответов из текущих моделей в конфигурации предоставляют gpt4-mini <br>
и Llama-3.3 70B.<br>
Ну и главный секрет бота - вы можете написать свой промпт в text/system_message.py <br>
и превратить Шизоида в любого другого ролевого бота!
