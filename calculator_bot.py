import logging
from math import sqrt
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

logging.basicConfig(filename='my_log', filemode='a', encoding='utf-8',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO
                    )
logger = logging.getLogger(__name__)

operation_keybord = [["Сложение", "Вычитание", "Умножение"],
                     ["Деление", "Возведение в степень", "Корень квадратный числа"],
                     ["Главное меню"]]

operation_keybord_main = "Сложение|Вычитание|Умножение|Деление|Возведение в степень|Корень квадратный числа|Главное меню"

MAINMENU, CHOOSING, OPERCHOISE, CATCHREPLY, CATCHREPLY2, CATCHREPLY3, CATCHREPLY4, DIVISION, CATCHREPLY5,\
CATCHREPLY6, CATCHREPLY7 = range(11)


def start(update, _):
    # Начинаем разговор с вопроса
    update.message.reply_text(
        'Здравствуйте, вас приветсвует телеграм-калькулятор. Для продолжения нажмите любую клавишу')

    return MAINMENU


def mainmenu(update, _):
    user = update.message.from_user
    logger.info("User %s started work with calculator.", user.first_name)
    # Список кнопок для ответа
    reply_keyboard = [['Рациональные', 'Комплексные', 'Выход']]
    # Создаем простую клавиатуру для ответа
    markup_key = ReplyKeyboardMarkup(reply_keyboard, True)
    # Начинаем разговор с вопроса
    update.message.reply_text(
        'Выберите с какими числами вы хотите работать',
        reply_markup=markup_key, )

    return CHOOSING


def choosing(update, _):
    user = update.message.from_user
    num_choiсe = update.message.text
    if num_choiсe == 'Рациональные':
        markup_key = ReplyKeyboardMarkup(operation_keybord, one_time_keyboard=True)
        update.message.reply_text('Какое действие вы хотите выполнить?', reply_markup=markup_key, )
        return OPERCHOISE
    elif num_choiсe == 'Комплексные':
        markup_key = ReplyKeyboardMarkup(operation_keybord, one_time_keyboard=True)
        update.message.reply_text('Какое действие вы хотите выполнить?', reply_markup=markup_key, )
        return OPERCHOISE
    elif num_choiсe == 'Выход':
        logger.info("User %s finished work with calculator.", user.first_name)
        update.message.reply_text(
            'Спасибо, что посетили нас',
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    else:
        pass


def oper_choice(update, _):
    oper = update.message.text
    if oper == "Сложение":
        update.message.reply_text('Введите два числа через пробел')
        return CATCHREPLY
    elif oper == "Вычитание":
        update.message.reply_text('Введите два числа через пробел')
        return CATCHREPLY2
    elif oper == "Возведение в степень":
        update.message.reply_text('Введите два числа через пробел')
        return CATCHREPLY3
    elif oper == "Деление":
        reply_keyboard = [['Остаток', 'Целочисленное', 'Обычное', 'Главное меню']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, True)
        update.message.reply_text('Выберите тип деления', reply_markup=markup_key)
        return DIVISION
    elif oper == "Корень квадратный числа":
        update.message.reply_text('Введите число')
        return CATCHREPLY4
    elif oper == "Главное меню":
        update.message.reply_text(
            'возвращение в главное меню',
        )
        return MAINMENU
    else:
        pass

def sum_oper(update, _):
    msg = update.message.text
    print(msg)
    items = msg.split()  # /sum 123 534543
    try:
        x = float(items[0])
        y = float(items[1])
        update.message.reply_text(f'{x}+{y} = {x + y}')
        return OPERCHOISE
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        return CATCHREPLY


def subtraction_oper(update, _):
    msg = update.message.text
    print(msg)
    items = msg.split()
    try:
        x = float(items[0])
        y = float(items[1])
        update.message.reply_text(f'{x}-{y} = {x - y}')
        return OPERCHOISE
    except:
        update.message.reply_text('Вы ввели неправильно, жмакните /start')
        return CATCHREPLY2


def power_oper(update, _):
    msg = update.message.text
    print(msg)
    items = msg.split()
    try:
        x = float(items[0])
        y = float(items[1])
        update.message.reply_text(f'{x}**{y} = {x ** y}')
        return OPERCHOISE
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        return CATCHREPLY3


def division_ch(update, _):
    msg = update.message.text
    if msg == 'Остаток':
        update.message.reply_text('Введите два числа через пробел')
        return CATCHREPLY5
    elif msg == 'Целочисленное':
        update.message.reply_text('Введите два числа через пробел')
        return CATCHREPLY6
    elif msg == 'Обычное':
        update.message.reply_text('Введите два числа через пробел')
        return CATCHREPLY7
    elif msg == "Главное меню":
        update.message.reply_text(
            'возвращение в главное меню',
        )
        return MAINMENU
    else:
        update.message.reply_text('Попобуйте еще раз выбрать')
        return DIVISION


def div_rem(update, _):
    msg = update.message.text
    items = msg.split()
    try:
        x = float(items[0])
        y = float(items[1])
        if y == 0:
            update.message.reply_text('На ноль делить нельзя! Попробуйте еще раз')
            return CATCHREPLY5
        else:
            update.message.reply_text(f'{x}%{y} = {x % y}')
            return DIVISION
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        return CATCHREPLY5


def division_int(update, _):
    msg = update.message.text
    items = msg.split()
    try:
        x = float(items[0])
        y = float(items[1])
        if y != 0:
            update.message.reply_text(f'{x}//{y} = {x // y}')
            return DIVISION
        else:
            update.message.reply_text('На ноль делить нельзя! Попробуйте еще раз')
            return CATCHREPLY6
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        return CATCHREPLY6


def division(update, _):
    msg = update.message.text
    items = msg.split()
    try:
        x = float(items[0])
        y = float(items[1])
        if y != 0:
            update.message.reply_text(f'{x}/{y} = {round((x / y),2)}')
            return DIVISION
        else:
            update.message.reply_text('На ноль делить нельзя! Попробуйте еще раз')
            return CATCHREPLY7
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        return CATCHREPLY7

def sqrt_oper(update, _):
    msg = update.message.text
    print(msg)
    items = msg
    try:
        x = float(items)
        update.message.reply_text(f'√{x}= {round(sqrt(x),2)}')
        return OPERCHOISE 
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        return CATCHREPLY4
         
    

def cancel(update, _):
    user = update.message.from_user
    logger.info("User %s finished work with calculator.", user.first_name)
    update.message.reply_text(
        'Спасибо, что посетили нас',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


if __name__ == '__main__':
    # Создаем Updater и передаем ему токен вашего бота.
    updater = Updater("5687323526:AAHmlKzSjgl91iqj59c7W9x0D35ULV1-URE")
    # получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Определяем обработчик разговоров `ConversationHandler` 
    conv_handler = ConversationHandler(  # здесь строится логика разговора
        # точка входа в разговор
        entry_points=[CommandHandler('start', start)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            MAINMENU: [MessageHandler(Filters.text & ~Filters.command, mainmenu)],
            CHOOSING: [MessageHandler(Filters.regex('^(Рациональные|Комплексные|Выход)$'), choosing)],
            OPERCHOISE: [MessageHandler(Filters.regex(f'^{operation_keybord_main}$'), oper_choice)],
            CATCHREPLY: [MessageHandler(Filters.text & ~Filters.command, sum_oper)],
            CATCHREPLY2: [MessageHandler(Filters.text & ~Filters.command, subtraction_oper)],
            CATCHREPLY3: [MessageHandler(Filters.text & ~Filters.command, power_oper)],
            CATCHREPLY4: [MessageHandler(Filters.text & ~Filters.command, sqrt_oper)],
            DIVISION: [MessageHandler(Filters.regex('^(Остаток|Целочисленное|Обычное|Главное меню)$'), division_ch)],
            CATCHREPLY5: [MessageHandler(Filters.text & ~Filters.command, div_rem)],
            CATCHREPLY6: [MessageHandler(Filters.text & ~Filters.command, division_int)],
            CATCHREPLY7: [MessageHandler(Filters.text & ~Filters.command, division)],
            

        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Добавляем обработчик разговоров `conv_handler`
    dispatcher.add_handler(conv_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()
