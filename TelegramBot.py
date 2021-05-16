import telebot
import TOKEN
import random, glob
 
from telebot import types
 
bot = telebot.TeleBot(TOKEN.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    print('REGISTR_USER | ', message.chat.id, " |  {0.first_name}".format(message.from_user, bot.get_me()))
 
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Хочу фото🙀")
 
    markup.add(item1)
 
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы показывать чудесные фотографии.".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup)
 
@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'Хочу фото🙀':
            bot.send_message(message.chat.id, 'Ожидайте фотографию...')
            photo = (random.choice(list(open('photo.txt'))))
            bot.send_photo(message.chat.id, photo)
            print('Photo: ', '|  User: ', message.chat.id, " |  {0.first_name}".format(message.from_user, bot.get_me()))
        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')
bot.polling(none_stop=True)
