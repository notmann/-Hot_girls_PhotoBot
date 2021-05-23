import telebot
import TOKEN
import random, glob

from telebot import types
from telebot.types import InputMediaPhoto

bot = telebot.TeleBot(TOKEN.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    print('REGISTR_USER | ', message.chat.id, " |  {0.first_name}".format(message.from_user, bot.get_me()))

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    photo = types.ReplyKeyboardMarkup(resize_keyboard=True)
    like = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item2 = types.KeyboardButton("Хочу фото🙀")
    item1 = types.KeyboardButton("/help")
    item3 = types.KeyboardButton("/developer")
    item4 = types.KeyboardButton("/photo_10")
    item5 = types.KeyboardButton("/photoX")

    markup.add(item1, item2, item3)
    photo.add(item4, item2, item5)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы показывать чудесные фотографии.\nСписок всех доступных команд: /help".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'Хочу фото🙀':
            #bot.send_message(message.chat.id, 'Фото')
            bot.send_message(message.chat.id, 'Ожидайте фотографию...')
            #photo = open('photo/photo.jpg', 'rb')
            #bot.send_photo(message.chat.id, photo)
            photo = (random.choice(list(open('photo.txt'))))
            bot.send_photo(message.chat.id, photo)
            print('Photo: ', '|  User: ', message.chat.id, " |  {0.first_name}".format(message.from_user, bot.get_me()))
        if message.text == '/photo':
            #bot.send_message(message.chat.id, 'Фото')
            bot.send_message(message.chat.id, 'Ожидайте фотографию...')
            #photo = open('photo/photo.jpg', 'rb')
            #bot.send_photo(message.chat.id, photo)
            photo = (random.choice(list(open('photo.txt'))))
            bot.send_photo(message.chat.id, photo)
            print('Photo: ', '|  User: ', message.chat.id, " |  {0.first_name}".format(message.from_user, bot.get_me()))

        #else:
        #    bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')       
        if message.text == '/photo_10':
            bot.send_message(message.chat.id, 'Загружаю 10 фотографий...')
            
            rand = [1,2,3,4,5,6,7,8,9,10]
            for i in range(len(rand)):
                rand[i] = (random.choice(list(open('photo.txt'))))
            media = [InputMediaPhoto(rand[1]), InputMediaPhoto(rand[2]), InputMediaPhoto(rand[3]), InputMediaPhoto(rand[4]), InputMediaPhoto(rand[5]), InputMediaPhoto(rand[6]), InputMediaPhoto(rand[7]), InputMediaPhoto(rand[8]), InputMediaPhoto(rand[9]), InputMediaPhoto(rand[0])]
            bot.send_media_group(message.chat.id, media)
            print('Альбом') 
        if message.text == '/developer':
            bot.send_message(message.chat.id,'Автор данного бота: 😵 Nikita 😵\n"Это мой один из первых Telegram Bot написанный на python."\nСсылка на автора: @bog_0001')
        if message.text == '/help':
            bot.send_message(message.chat.id, 'Доступные команды:\n/start\n/photo\n/photo_10\n/photoX\n/download_photo\n/developer')
            
        if message.text == '/download_photo':
            bot.send_message(message.chat.id,'Загрузка фотографий в Telegram Bot разрешена только админам данного бота!')
        if message.text == '/photoX':
            bot.send_message(message.chat.id, 'Ожидайте фотографии...')
            
            rand = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
            for i in range(len(rand)):
                rand[i] = (random.choice(list(open('photo.txt'))))
            media = [InputMediaPhoto(rand[0]), InputMediaPhoto(rand[1]), InputMediaPhoto(rand[2]), InputMediaPhoto(rand[3]), InputMediaPhoto(rand[4]), InputMediaPhoto(rand[5]), InputMediaPhoto(rand[6]), InputMediaPhoto(rand[7]), InputMediaPhoto(rand[8]), InputMediaPhoto(rand[9])]
            media2 = [InputMediaPhoto(rand[10]), InputMediaPhoto(rand[11]), InputMediaPhoto(rand[12]), InputMediaPhoto(rand[13]), InputMediaPhoto(rand[14]), InputMediaPhoto(rand[15]), InputMediaPhoto(rand[16]), InputMediaPhoto(rand[17]), InputMediaPhoto(rand[18]), InputMediaPhoto(rand[19])]
            media3 = [InputMediaPhoto(rand[20]), InputMediaPhoto(rand[21]), InputMediaPhoto(rand[22]), InputMediaPhoto(rand[23]), InputMediaPhoto(rand[24]), InputMediaPhoto(rand[25]), InputMediaPhoto(rand[26]), InputMediaPhoto(rand[27]), InputMediaPhoto(rand[28]), InputMediaPhoto(rand[29])]
            bot.send_message(message.chat.id, 'Загружаю 30 фотографий')
            bot.send_message(message.chat.id, 'Это может занять продолжительное время...')
            bot.send_media_group(message.chat.id, media)
            bot.send_media_group(message.chat.id, media2)
            bot.send_media_group(message.chat.id, media3)
            print('АльбомX')   

@bot.message_handler(content_types=['photo'])
def photo(message):
    admin = 382889134
    user = message.chat.id
    if user == admin:
        bot.send_message(message.chat.id,'Добро пожаловать хозяйн!')
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        print ('Получена новая фотография | ',fileID)
        with open("photo/"+fileID+".jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, 'Успешно загружено.')
        #else:
            #   bot.send_message(message.chat.id, 'Отказано в доступе!')
@bot.message_handler(content_types=['video'])
def video(message):
    admin = 382889134
    user = message.chat.id
    if user == admin:
        bot.send_message(message.chat.id,'Добро пожаловать хозяйн!')
        fileID = message.video.file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        print ('Получена новое видео | ',fileID)
        with open("video/"+fileID+".mp4", 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, 'Успешно загружено.')
    
# RUN
bot.polling(none_stop=True) 