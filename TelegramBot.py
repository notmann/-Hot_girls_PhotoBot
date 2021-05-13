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
            #bot.send_message(message.chat.id, 'Фото')
            bot.send_message(message.chat.id, 'Ожидайте фотографию...')
            #photo = open('photo/photo.jpg', 'rb')
            #bot.send_photo(message.chat.id, photo)
            files = glob.glob('photo/*.jpg')
            with open(random.choice(files), 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
                print('Photo: ', photo , '|  User: ', message.chat.id, " |  {0.first_name}".format(message.from_user, bot.get_me()))
        else:
        	bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')
    	
@bot.message_handler(content_types=['photo'])
def photo(message):
    admin = 382889134
    user = message.chat.id
    if user == admin:
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        print ('Получена новая фотография | ',fileID)
        with open("photo/"+fileID+".jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, 'Фотография успешно загружена.')
        #else:
            #   bot.send_message(message.chat.id, 'Отказано в доступе!')
# RUN
bot.polling(none_stop=True)