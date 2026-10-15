# generate_post.py
import os
import requests
import random
from datetime import datetime

# --- НАСТРОЙКИ ИЗ СЕКРЕТОВ GITHUB ---
TG_TOKEN = os.environ.get("TG_BOT_TOKEN")
CHANNEL_ID = os.environ.get("TG_CHANNEL_ID")  # например @neurocard_cases
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# --- БИБЛИОТЕКА ТЕМ (меняй под себя) ---
TOPICS = [
    "кейс: как описание подняло просмотры товара на WB в 3 раза",
    "3 ошибки в описаниях товаров, из-за которых их не находят",
    "почему нейросеть пишет лучше, чем уставший селлер в 2 часа ночи",
    "как правильно составить ключевые слова для Ozon",
    "пример: до/после описания детского велосипеда для Авито",
    "что продавать на маркетплейсах в этом месяце — ИИ-анализ трендов",
    "шаблон продающего описания, который работает в 80% случаев",
    "как я сделал 50 описаний товаров за 1 час с помощью бота",
    "почему 'высокое качество' и 'отличный выбор' убивают продажи",
    "секретные ключевые слова, которые ищут покупатели, но не знают продавцы",
]

def generate_post_with_ai(topic):
    """Генерирует пост через бесплатный Groq"""
    system_prompt = """Ты — SMM-эксперт для Telegram-канала про продажи на маркетплейсах.
Пиши живо, с эмодзи, короткими абзацами. НЕ пиши как робот. 
Формат ответа:
[Заголовок с 1 эмодзи]

[Основной текст: 3-5 коротких абзацев, 400-600 знаков, разбитых пустой строкой]

[Призыв к действию: 1-2 предложения, мягко ведущие к боту @neurocard_mp_bot]

[3-5 хэштегов через пробел, например #авито #wb #маркетплейсы]"""
    
    user_prompt = f"Напиши пост на тему: {topic}"
    
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.9,
            "max_tokens": 500
        }
    )
    
    data = response.json()
    return data["choices"][0]["message"]["content"]

def post_to_telegram(text):
    """Отправляет пост в канал"""
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    response = requests.post(url, data=payload)
    result = response.json()
    
    if not result.get("ok"):
        raise Exception(f"Ошибка Telegram: {result}")
    print("✅ Пост успешно опубликован!")
    print(f"Текст: {text[:100]}...")

def main():
    topic = random.choice(TOPICS)
    print(f"📝 Тема поста: {topic}")
    
    try:
        post_text = generate_post_with_ai(topic)
        print(f"🤖 Сгенерировано {len(post_text)} символов")
        post_to_telegram(post_text)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        # Штатный пост на случай ошибки
        fallback = "🔥 Новый кейс уже в боте! Заходи: @neurocard_mp_bot\n\n#маркетплейсы #wb #авито"
        post_to_telegram(fallback)

if __name__ == "__main__":
    main()
