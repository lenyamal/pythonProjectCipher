import telebot

from token import API_TOKEN
import library as lib

if __name__ == '__main__':
    bot = telebot.TeleBot(API_TOKEN)
    bot.cipher_mode = None
    bot.cipher_type = None
    bot.cipher_key = None
    bot.cipher_language = None
    bot.cipher_text = None

    @bot.message_handler(commands=['help'])
    def command_help(message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
        markup.add(*upd_buttons())
        bot.send_message(message.chat.id,
                         'Для работы бота нужно указать несколько параметров. Обязательные: язык, '
                         'режим и текст.\nДля того, чтобы выбрать язык, используйте команду '
                         '/language.\nДля того, чтобы выбрать режим, напишите /mode: cipher - '
                         'зашифровать, decipher - расшифровать, hack - автоматический взлом шифра '
                         'Цезаря.\nЕсли выбран режим cipher или decipher, то необходимо так же '
                         'указать тип с помощью команды /type, а также ввести ключ в виде "/key '
                         '[ключевое слово]", причём для шифра Цезаря это должно быть целое число, а '
                         'для шифра Виженера - строка из букв выбранного языка.\n После того, как все '
                         'параметры указаны, можно делать запрос с текстом в виде "/text [текст]" и '
                         'бот отправит в ответ результат работы, если всё указано верно.',
                         reply_markup=markup)

    def upd_buttons():
        buttons = []
        if bot.cipher_language is None:
            buttons.append(telebot.types.KeyboardButton('/language'))
        if bot.cipher_mode is None:
            buttons.append(telebot.types.KeyboardButton('/mode'))
        if not bot.cipher_mode is None and bot.cipher_mode != 'hack' and bot.cipher_type is None:
            buttons.append(telebot.types.KeyboardButton('/type'))
        if not bot.cipher_mode is None and bot.cipher_mode != 'hack' and bot.cipher_key is None:
            buttons.append(telebot.types.KeyboardButton('/key'))
        return buttons

    def send_go_next(message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
        markup.add(*upd_buttons())
        bot.send_message(message.chat.id, 'Отлично, переходите к следующему шагу', reply_markup=markup)

    @bot.message_handler(commands=['start'])
    def command_start(message):
        bot.cipher_mode = None
        bot.cipher_type = None
        bot.cipher_key = None
        bot.cipher_language = None
        bot.cipher_text = None
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
        markup.add(*upd_buttons())
        bot.send_message(message.chat.id,
                         'Добра пожаловать в бота-шифровщика! Бот может зашифровать и расшифровать '
                         'тексты на русском или английском языке с помощью шифров Цезаря и Виженера '
                         'по заданному ключу. Кроме того, он может автоматически взломать шифр '
                         'Цезаря, используя метод частотного анализа (но необязательно '
                         'правильно).\nЧтобы получить дополнительную информацию, воспользуйтесь '
                         'коммандой /help.',
                         reply_markup=markup)

    @bot.message_handler(commands=['mode'])
    def update_mode(message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
        cipher = telebot.types.KeyboardButton('/cipher')
        decipher = telebot.types.KeyboardButton('/decipher')
        hack = telebot.types.KeyboardButton('/hack')
        markup.add(cipher, decipher, hack)
        bot.send_message(message.chat.id, 'Выберите режим', reply_markup=markup)

    @bot.message_handler(commands=['cipher'])
    def do_cipher(message):
        bot.cipher_mode = 'c'
        send_go_next(message)

    @bot.message_handler(commands=['decipher'])
    def do_decipher(message):
        bot.cipher_mode = 'd'
        send_go_next(message)

    @bot.message_handler(commands=['hack'])
    def do_decipher(message):
        bot.cipher_mode = 'hack'
        send_go_next(message)

    @bot.message_handler(commands=['language'])
    def update_language(message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        en = telebot.types.KeyboardButton('/english')
        ru = telebot.types.KeyboardButton('/russian')
        markup.add(ru, en)
        bot.send_message(message.chat.id, 'Выберите язык текста', reply_markup=markup)

    @bot.message_handler(commands=['russian'])
    def do_ru(message):
        bot.cipher_language = 'ru'
        send_go_next(message)

    @bot.message_handler(commands=['english'])
    def do_en(message):
        bot.cipher_language = 'en'
        send_go_next(message)

    @bot.message_handler(commands=['type'])
    def update_type(message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        caesar = telebot.types.KeyboardButton('/caesar')
        vigenere = telebot.types.KeyboardButton('/vigenere')
        markup.add(caesar, vigenere)
        bot.send_message(message.chat.id, 'Выберите тип шифра', reply_markup=markup)

    @bot.message_handler(commands=['caesar'])
    def do_caesar(message):
        bot.cipher_type = 'caesar'
        send_go_next(message)

    @bot.message_handler(commands=['vigenere'])
    def do_vigenere(message):
        bot.cipher_type = 'vigenere'
        send_go_next(message)

    @bot.message_handler(commands=['key'])
    def update_key(message):
        ind = message.text.find('/key')
        bot.cipher_key = message.text[ind + 5:]
        print(bot.cipher_key)
        if bot.cipher_key is None or bot.cipher_key.rstrip() == '':
            bot.send_message(message.chat.id, 'Ошибка!\nПовторите ввод в виде "/key [ключевое слово]"')
            return
        send_go_next(message)

    def check_arguments(message):
        if bot.cipher_language is None:
            bot.send_message(message.chat.id, 'Ошибка!\nВведите язык текста с помощью команды /language')
            return True
        if bot.cipher_mode is None:
            bot.send_message(message.chat.id, 'Ошибка!\nВведите режим с помощью команды /mode')
            return True
        if bot.cipher_mode != 'hack' and bot.cipher_type is None:
            bot.send_message(message.chat.id, 'Ошибка!\nВведите тип шифра с помощью команды /type')
            return True
        if bot.cipher_mode != 'hack' and bot.cipher_key is None:
            bot.send_message(message.chat.id, 'Ошибка!\nВведите ключ шифрования с помощью команды /key')
            return True
        return False

    @bot.message_handler(commands=['text'])
    def processing(message):
        if check_arguments(message):
            return
        ind = message.text.find('/text')
        bot.cipher_text = message.text[ind + 6:]
        if bot.cipher_text is None or bot.cipher_text.rstrip() == '':
            bot.send_message(message.chat.id, 'Ошибка!\nПовторите ввод в виде "/text [ключевое слово]"')
            return
        if bot.cipher_language == 'en':
            alphabet = lib.AlphabetEN()
        elif bot.cipher_language == 'ru':
            alphabet = lib.AlphabetRU()
        else:
            bot.send_message(message.chat.id, 'Что-то пошло не так. Проверьте правильность ввода языка.')
            return

        if bot.cipher_type is not None:
            if bot.cipher_type.lower() == "caesar":
                executor = lib.Caesar(alphabet)
                try:
                    key = int(bot.cipher_key)
                except:
                    bot.send_message(message.chat.id, 'Что-то пошло не так. Проверьте правильность ввода ключа.')
                    return
            elif bot.cipher_type.lower() == "vigenere":
                executor = lib.Vigenere(alphabet)
                key = bot.cipher_key
            else:
                bot.send_message(message.chat.id, 'Что-то пошло не так. Проверьте правильность ввода ключа.')
                return

        try:
            if bot.cipher_mode == "c":
                execute = executor.cipher
            elif bot.cipher_mode == "d":
                execute = executor.decipher
            elif bot.cipher_mode == "hack":
                hacker = lib.Hack(alphabet)
                bot.send_message(message.chat.id, hacker.hack(bot.cipher_text))
                return

            bot.send_message(message.chat.id, execute(bot.cipher_text, key))
        except:
            bot.send_message(message.chat.id, 'Что-то пошло не так. Проверьте правильность ввода данных.')

    @bot.message_handler()
    def processing(message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
        markup.add(telebot.types.KeyboardButton('/start'), telebot.types.KeyboardButton('/help'))
        bot.send_message(message.chat.id,
                         'Команда не распознана. Чтобы начать заново, нажмите /start. Чтобы узнать дополнительную '
                         'информацию, нажмите /help.',
                         reply_markup=markup)

    bot.polling(none_stop=True)
