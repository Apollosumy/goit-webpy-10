import pymongo
import os
import django

# Устанавливаем переменную DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analog.settings')

# Инициализируем Django
django.setup()

from django.contrib.auth.models import User
from main.models import Author, Quote

# Подключение к MongoDB
MONGO_URI = "mongodb+srv://sumyultras88:Ghbdtn_123456@cluster0.4nl1k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo_client = pymongo.MongoClient(MONGO_URI)
mongo_db = mongo_client['quotes_db']

# Создаем фиктивного пользователя
default_user, created = User.objects.get_or_create(
    username='default_user',
    defaults={'password': 'default_password'}
)
if created:
    print("Создан фиктивный пользователь: default_user")

# Миграция авторов
for author_data in mongo_db.authors.find():
    author, created = Author.objects.get_or_create(
        name=author_data['name'],
        defaults={'bio': author_data.get('description', '')}
    )
    if created:
        print(f"Автор добавлен: {author.name}")
    else:
        print(f"Автор уже существует: {author.name}")

# Миграция цитат
for quote_data in mongo_db.quotes.find():
    author_name = quote_data.get('author', '')
    try:
        author = Author.objects.get(name=author_name)
        quote, created = Quote.objects.get_or_create(
            text=quote_data['quote'],
            defaults={
                'author': author,
                'created_by': default_user,
            }
        )
        if created:
            print(f"Цитата добавлена: {quote.text}")
        else:
            print(f"Цитата уже существует: {quote.text}")
    except Author.DoesNotExist:
        print(f"Автор для цитаты '{quote_data['quote']}' не найден. Пропускаем.")
