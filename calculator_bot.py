import logging
from math import sqrt
from cmath import sqrt as sc
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

MAINMENU, CHOOSING, OPERCHOICE,SUM, SUB, POWER, SQRT, DIVISION, DIVREM, DIVINT, DIV,MULTIPLY, \
COMPLOPERCHOICE,COMPLSUB,COMPLSUM,COMPLDIV,COMPLMULT,COMPLPOW,COMPLSQRT = range(19)


def start(update, _): # начало работы
    start_key = [['Начать работу']] # Список кнопок для ответа
    markup_key = ReplyKeyboardMarkup(start_key, True)# Создаем простую клавиатуру для ответа
    update.message.reply_text(f'Здравствуйте {update.message.from_user.first_name}!\nBас приветсвует телеграм-калькулятор.', 
                                reply_markup=markup_key)
    return MAINMENU


def mainmenu(update, _): #основное меню
    user = update.message.from_user
    logger.info("Пользователь %s начал работу с калькулятором.", user.first_name)
    # Список кнопок для ответа
    reply_keyboard = [['Рациональные', 'Комплексные', 'Выход']]
    # Создаем простую клавиатуру для ответа
    markup_key = ReplyKeyboardMarkup(reply_keyboard, True)
    # Начинаем разговор с вопроса
    update.message.reply_text('Выберите с какими числами вы хотите работать', reply_markup=markup_key, )
    return CHOOSING # выбор вида чисел


def choosing(update, _): # выбор вида числа
    user = update.message.from_user
    num_choiсe = update.message.text
    if num_choiсe == 'Рациональные':
        markup_key = ReplyKeyboardMarkup(operation_keybord, one_time_keyboard=True)
        update.message.reply_text('Какое действие вы хотите выполнить?', reply_markup=markup_key, )
        logger.info("Пользователь %s выбрал рациональные числа.", user.first_name)
        return OPERCHOICE # меню выбора оператора
    elif num_choiсe == 'Комплексные':
        markup_key = ReplyKeyboardMarkup(operation_keybord, one_time_keyboard=True)
        update.message.reply_text('Какое действие вы хотите выполнить?', reply_markup=markup_key, )
        logger.info("Пользователь %s выбрал комплексные числа.", user.first_name)
        return COMPLOPERCHOICE # меню выбора оператора
    elif num_choiсe == 'Выход':
        logger.info("Пользователь %s вышел", user.first_name)
        update.message.reply_text('Спасибо, что посетили нас', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


def oper_choice(update, _): # меню для комплексных
    user = update.message.from_user
    oper = update.message.text
    logger.info("Пользователь %s выбрал %s.", user.first_name,oper)
    if oper == "Сложение":
        update.message.reply_text('Введите два числа через пробел')
        return SUM # сложение рациональных чисел
    elif oper == "Вычитание":
        update.message.reply_text('Введите два числа через пробел')
        return SUB # вычитание рациональных чисел
    elif oper == "Возведение в степень":
        update.message.reply_text('Введите два числа через пробел')
        return POWER # возведение в степень рациональных чисел
    elif oper == "Деление":
        reply_keyboard = [['Остаток', 'Целочисленное', 'Обычное', 'Главное меню']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, True)
        update.message.reply_text('Выберите тип деления', reply_markup=markup_key)
        return DIVISION # выбор вида деления 
    elif oper == "Корень квадратный числа":
        update.message.reply_text('Введите число')
        return SQRT # вычисляет квадратный корень числа
    elif oper == "Умножение":
        update.message.reply_text('Введите два числа через пробел')
        return MULTIPLY # вычисляет квадратный корень числа
    elif oper == "Главное меню":
        update.message.reply_text('возвращение в главное меню')
        return MAINMENU


def oper_choice_compl(update, _): # меню для рациональных
    oper = update.message.text
    if oper == "Сложение":
        update.message.reply_text('Введите действительную часть и мнимую часть двух чисел через пробелы')
        return COMPLSUM 
    elif oper == "Вычитание":
        update.message.reply_text('Введите действительную часть и мнимую часть двух чисел через пробелы')
        return COMPLSUB 
    elif oper == "Возведение в степень":
        update.message.reply_text('Введите действительную часть и мнимую часть двух чисел через пробелы')
        return COMPLPOW 
    elif oper == "Деление":
        update.message.reply_text('Введите действительную часть и мнимую часть двух чисел через пробелы')
        return COMPLDIV 
    elif oper == "Корень квадратный числа":
        update.message.reply_text('Введите действительную часть и мнимую часть чиселa через пробел')
        return COMPLSQRT 
    elif oper == "Умножение":
        update.message.reply_text('Введите действительную часть и мнимую часть двух чисел через пробелы')
        return COMPLMULT 
    elif oper == "Главное меню":
        update.message.reply_text('возвращение в главное меню')
        return MAINMENU       


def division_ch(update, _): # подменю деления рациональных
    msg = update.message.text
    if msg == 'Остаток':
        update.message.reply_text('Введите два числа через пробел')
        return DIVREM
    elif msg == 'Целочисленное':
        update.message.reply_text('Введите два числа через пробел')
        return DIVINT
    elif msg == 'Обычное':
        update.message.reply_text('Введите два числа через пробел')
        return DIV
    elif msg == "Главное меню":
        update.message.reply_text('возвращение в главное меню')
        return MAINMENU

def sum_oper(update, _): # сумма рац.
    user = update.message.from_user
    msg = update.message.text
    items = msg.split()  
    try:
        x = float(items[0])
        y = float(items[1])
        update.message.reply_text(f'{x}+{y} = {x + y}')
        logger.info("Пример пользователя %s: %s + %s = %s ", user.first_name, x, y, x+y)
        return OPERCHOICE # меню выбора оператора
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return SUM


def subtraction_oper(update, _): # разность рац.
    user = update.message.from_user
    msg = update.message.text
    items = msg.split()
    try:
        x = float(items[0])
        y = float(items[1])
        update.message.reply_text(f'{x}-{y} = {round((x - y),3)}')
        logger.info("Пример пользователя %s: %s - %s = %s ", user.first_name, x, y, x-y)
        return OPERCHOICE # меню выбора оператора
    except:
        update.message.reply_text('Вы ввели неправильно, попробуйте еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return SUB


def power_oper(update, _): # степень рац.
    user = update.message.from_user
    msg = update.message.text
    items = msg.split()
    try:
        x = float(items[0])
        y = float(items[1])
        update.message.reply_text(f'{x}**{y} = {x ** y}')
        logger.info("Пример пользователя %s: %s ** %s = %s ", user.first_name, x, y, x**y)
        return OPERCHOICE # меню выбора оператора
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return POWER


def div_rem(update, _): # остаток от деления рац.
    user = update.message.from_user
    msg = update.message.text
    items = msg.split()
    try:
        x = float(items[0])
        y = float(items[1])
    except:
        update.message.reply_text('Ошибка ввода')
        logger.error("Ошибка ввода", exc_info = True) # вот тут я применил метод error модуля logging и здесь я остановился с включением логов
        return DIVREM
    try:
        update.message.reply_text(f'{x}%{y} = {x % y}')
        logger.info("Пример пользователя %s: %s '%' %s = %s ", user.first_name, x, y, x%y)
        return DIVISION
    except:
        update.message.reply_text('На ноль делить нельзя! Попробуйте еще раз')
        logger.error("Попытка деления на ноль", exc_info = True)
        return DIVREM


def division_int(update, _): # целочисленное деление рац.
    user = update.message.from_user
    msg = update.message.text
    items = msg.split()
    try:
        x = float(items[0])
        y = float(items[1])
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return DIVINT        
    try:
        update.message.reply_text(f'{x}//{y} = {x // y}')
        logger.info("Пример пользователя %s: %s // %s = %s ", user.first_name, x, y, x//y)
        return DIVISION
    except:
        update.message.reply_text('На ноль делить нельзя! Попробуйте еще раз')
        logger.error("Попытка деления на ноль", exc_info = True)
        return DIVINT


def division(update, _): # деление рац.
    user = update.message.from_user
    msg = update.message.text
    items = msg.split()
    try:
        x = float(items[0])
        y = float(items[1])
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return DIV    
    try:
        update.message.reply_text(f'{x}/{y} = {round((x / y),2)}')
        logger.info("Пример пользователя %s: %s / %s = %s ", user.first_name, x, y, x/y)
        return DIVISION
    except:
        update.message.reply_text('На ноль делить нельзя! Попробуйте еще раз')
        logger.error("Попытка деления на ноль", exc_info = True)
        return DIV


def sqrt_oper(update, _): # корень рац.
    user = update.message.from_user
    msg = update.message.text
    try:
        x = float(msg)
        update.message.reply_text(f'√{x}= {round(sqrt(x),2)}')
        logger.info("Пример пользователя %s: √%s = %s ", user.first_name, x, sqrt(x))
        return OPERCHOICE # меню выбора оператора 
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return SQRT


def multiply(update, _): # умножение рац.
    user = update.message.from_user
    msg = update.message.text
    items = msg.split()
    try:
        x = float(items[0])
        y = float(items[1])
        update.message.reply_text(f'{x}*{y} = {x * y}')
        logger.info("Пример пользователя %s: %s * %s = %s ", user.first_name, x, y, x*y)
        return OPERCHOICE # меню выбора оператора
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return MULTIPLY
    
    
def sum_compl(update, _): # сумма компл.
    user = update.message.from_user
    msg = update.message.text
    items = msg.split() 
    try:
        x = complex(float(items[0]), float(items[1]))
        y = complex(float(items[2]), float(items[3]))
        update.message.reply_text(f'{x}+{y} = {x + y}')
        logger.info("Пример пользователя %s: %s + %s = %s ", user.first_name, x, y, x+y)
        return COMPLOPERCHOICE # меню выбора оператора
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return COMPLSUM


def sub_compl(update, _): # разность компл.
    user = update.message.from_user
    msg = update.message.text
    items = msg.split() 
    try:
        x = complex(float(items[0]), float(items[1]))
        y = complex(float(items[2]), float(items[3]))
        update.message.reply_text(f'{x}-{y} = {x - y}')
        logger.info("Пример пользователя %s: %s - %s = %s ", user.first_name, x, y, x-y)
        return COMPLOPERCHOICE # меню выбора оператора
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return COMPLSUB


def mult_compl(update, _): # умножение компл.
    user = update.message.from_user
    msg = update.message.text
    items = msg.split()  
    try:
        x = complex(float(items[0]), float(items[1]))
        y = complex(float(items[2]), float(items[3]))
        update.message.reply_text(f'{x}*{y} = {x * y}')
        logger.info("Пример пользователя %s: %s * %s = %s ", user.first_name, x, y, x*y)
        return COMPLOPERCHOICE # меню выбора оператора
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return COMPLMULT


def div_compl(update, _): # деление компл.
    user = update.message.from_user
    msg = update.message.text
    items = msg.split()  
    try:
        x = complex(float(items[0]), float(items[1]))
        y = complex(float(items[2]), float(items[3]))
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return COMPLDIV
    try:    
        update.message.reply_text(f'{x}/{y} = {x / y}')
        logger.info("Пример пользователя %s: %s / %s = %s ", user.first_name, x, y, x/y)
        return COMPLOPERCHOICE # меню выбора оператора
    except:
        update.message.reply_text('На ноль делить нельзя. Попробуйте что-нибудь еще')
        logger.error("Попытка деления на ноль", exc_info = True)
        return COMPLDIV


def pow_compl(update, _): # степень компл
    user = update.message.from_user
    msg = update.message.text
    print(msg)
    items = msg.split() 
    try:
        x = complex(float(items[0]), float(items[1]))
        y = complex(float(items[2]), float(items[3]))
        update.message.reply_text(f'{x}**{y} = {x ** y}')
        logger.info("Пример пользователя %s: %s ** %s = %s ", user.first_name, x, y, x**y)
        return COMPLOPERCHOICE # меню выбора оператора
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return COMPLPOW
    

def sqrt_compl(update, _): # корень компл.
    user = update.message.from_user
    msg = update.message.text
    items = msg.split()
    try:
        x = complex(float(items[0]), float(items[1]))
        update.message.reply_text(f'√{x}= {sc(x)}')
        logger.info("Пример пользователя %s: √ %s = %s ", user.first_name, x, sc(x))
        return COMPLOPERCHOICE # меню выбора оператора
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return COMPLSQRT    
         
    

def cancel(update, _): # выход из разговора
    user = update.message.from_user
    logger.info("User %s finished work with calculator.", user.first_name)
    update.message.reply_text('Спасибо, что посетили нас', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


if __name__ == '__main__':
    # Создаем Updater и передаем ему токен вашего бота.
    updater = Updater("TOKEN")
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
            OPERCHOICE: [MessageHandler(Filters.regex(f'^{operation_keybord_main}$'), oper_choice)],
            COMPLOPERCHOICE: [MessageHandler(Filters.regex(f'^{operation_keybord_main}$'), oper_choice_compl)],
            SUM: [MessageHandler(Filters.text & ~Filters.command, sum_oper)],
            SUB: [MessageHandler(Filters.text & ~Filters.command, subtraction_oper)],
            POWER: [MessageHandler(Filters.text & ~Filters.command, power_oper)],
            SQRT: [MessageHandler(Filters.text & ~Filters.command, sqrt_oper)],
            DIVISION: [MessageHandler(Filters.regex('^(Остаток|Целочисленное|Обычное|Главное меню)$'), division_ch)],
            DIVREM: [MessageHandler(Filters.text & ~Filters.command, div_rem)],
            DIVINT: [MessageHandler(Filters.text & ~Filters.command, division_int)],
            DIV: [MessageHandler(Filters.text & ~Filters.command, division)],
            MULTIPLY: [MessageHandler(Filters.text & ~Filters.command, multiply)],
            COMPLSUM: [MessageHandler(Filters.text & ~Filters.command, sum_compl)],
            COMPLSUB: [MessageHandler(Filters.text & ~Filters.command, sub_compl)],
            COMPLMULT: [MessageHandler(Filters.text & ~Filters.command, mult_compl)],
            COMPLDIV: [MessageHandler(Filters.text & ~Filters.command, div_compl)],
            COMPLSQRT: [MessageHandler(Filters.text & ~Filters.command, sqrt_compl)],
            COMPLPOW: [MessageHandler(Filters.text & ~Filters.command, pow_compl)],
            
        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Добавляем обработчик разговоров `conv_handler`
    dispatcher.add_handler(conv_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()
