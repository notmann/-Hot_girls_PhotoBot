import telebot
import TOKEN
import random
import glob
import os
from telebot import types
from telebot.types import InputMediaPhoto

bot = telebot.TeleBot(TOKEN.TOKEN)

# Константы
ADMIN_ID = 382889134
PHOTOS_FILE = 'photo.txt'
PHOTOS_DIR = 'photo'
VIDEOS_DIR = 'video'

# Создаем директории если их нет
os.makedirs(PHOTOS_DIR, exist_ok=True)
os.makedirs(VIDEOS_DIR, exist_ok=True)

def get_random_photos(count=1):
    """Получает случайные фотографии из файла"""
    with open(PHOTOS_FILE, 'r') as f:
        photos = [line.strip() for line in f.readlines()]
    return random.sample(photos, min(count, len(photos))) if count > 1 else random.choice(photos)

def create_media_group(photos, start_index=0):
    """Создает группу медиа для отправки"""
    return [InputMediaPhoto(photo) for photo in photos]

@bot.message_handler(commands=['start'])
def welcome(message):
    # Отправка стикера
    with open('static/sticker.webp', 'rb') as sti:
        bot.send_sticker(message.chat.id, sti)
    
    print(f'REGISTR_USER | {message.chat.id} | {message.from_user.first_name}')
    
    # Создание клавиатуры
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Хочу фото🙀"),
        types.KeyboardButton("/help"),
        types.KeyboardButton("/developer")
    )
    
    bot.send_message(
        message.chat.id,
        f"Добро пожаловать, {message.from_user.first_name}!\n"
        f"Я - {bot.get_me().first_name}, бот созданный чтобы показывать чудесные фотографии.\n"
        "Список всех доступных команд: /help",
        parse_mode='html',
        reply_markup=markup
    )

@bot.message_handler(commands=['photo'])
def send_photo(message):
    bot.send_message(message.chat.id, 'Ожидайте фотографию...')
    photo = get_random_photos()
    bot.send_photo(message.chat.id, photo)
    print(f'Photo | User: {message.chat.id} | {message.from_user.first_name}')

@bot.message_handler(commands=['photo_10'])
def send_10_photos(message):
    bot.send_message(message.chat.id, 'Загружаю 10 фотографий...')
    photos = get_random_photos(10)
    media = create_media_group(photos)
    bot.send_media_group(message.chat.id, media)
    print('Альбом (10 фото)')

@bot.message_handler(commands=['photoX'])
def send_30_photos(message):
    bot.send_message(message.chat.id, 'Загружаю 30 фотографий...')
    bot.send_message(message.chat.id, 'Это может занять продолжительное время...')
    
    photos = get_random_photos(30)
    
    # Отправляем по 10 фото в группе
    for i in range(0, 30, 10):
        media = create_media_group(photos[i:i+10])
        bot.send_media_group(message.chat.id, media)
    
    print('АльбомX (30 фото)')

@bot.message_handler(commands=['developer'])
def developer_info(message):
    bot.send_message(
        message.chat.id,
        'Автор данного бота: 😵 Nikita 😵\n'
        '"Это мой один из первых Telegram Bot написанный на python."\n'
        'Ссылка на автора: @bog_0001'
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        'Доступные команды:\n'
        '/start\n'
        '/photo\n'
        '/photo_10\n'
        '/photoX\n'
        '/download_photo\n'
        '/developer'
    )
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['download_photo'])
def download_info(message):
    bot.send_message(
        message.chat.id,
        'Загрузка фотографий в Telegram Bot разрешена только админам данного бота!'
    )

def handle_file_upload(message, file_type):
    """Общий обработчик загрузки файлов"""
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id, 'Отказано в доступе!')
        return
    
    bot.send_message(message.chat.id, 'Добро пожаловать, хозяин!')
    
    if file_type == 'photo':
        file_id = message.photo[-1].file_id
        file_extension = 'jpg'
        directory = PHOTOS_DIR
    else:  # video
        file_id = message.video.file_id
        file_extension = 'mp4'
        directory = VIDEOS_DIR
    
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    filename = f"{file_id}.{file_extension}"
    filepath = os.path.join(directory, filename)
    
    with open(filepath, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    print(f'Получен новый {file_type} | {file_id}')
    bot.send_message(message.chat.id, f'Успешно загружено как {filename}')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    handle_file_upload(message, 'photo')

@bot.message_handler(content_types=['video'])
def handle_video(message):
    handle_file_upload(message, 'video')

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.chat.type != 'private':
        return
    
    text_handlers = {
        'Хочу фото🙀': send_photo,
        '/photo': send_photo,
        '/photo_10': send_10_photos,
        '/photoX': send_30_photos,
        '/developer': developer_info,
        '/help': help_command,
        '/download_photo': download_info
    }
    
    if message.text in text_handlers:
        # Создаем имитацию объекта message для обработчика
        class FakeMessage:
            def __init__(self, original, command):
                self.chat = original.chat
                self.from_user = original.from_user
                self.text = command
        
        fake_msg = FakeMessage(message, message.text)
        text_handlers[message.text](fake_msg)
    else:
        bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')

# Запуск бота
if __name__ == '__main__':
    print('Бот запущен...')
    bot.polling(none_stop=True)
