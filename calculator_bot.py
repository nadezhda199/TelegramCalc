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

#from compl import sum_compl, sub_compl,mult_compl,div_compl,sqrt_compl,pow_compl,\
    #COMPLSUB,COMPLSUM,COMPLDIV,COMPLMULT,COMPLPOW,COMPLSQRT


MAINMENU, CHOOSING, OPERCHOICE,CATCHREPLY, CATCHREPLY2, CATCHREPLY3, CATCHREPLY4, DIVISION, CATCHREPLY5,\
CATCHREPLY6, CATCHREPLY7,MULTIPLY,OPERCHOICE2,COMPLSUB,COMPLSUM,COMPLDIV,COMPLMULT,COMPLPOW,COMPLSQRT = range(19)


def start(update, _):
    update.message.reply_text(
        'Здравствуйте, вас приветсвует телеграм-калькулятор. Для продолжения нажмите любую клавишу')

    return MAINMENU


def mainmenu(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s начал работу с калькулятором.", user.first_name)
    # Список кнопок для ответа
    reply_keyboard = [['Рациональные', 'Комплексные', 'Выход']]
    # Создаем простую клавиатуру для ответа
    markup_key = ReplyKeyboardMarkup(reply_keyboard, True)
    # Начинаем разговор с вопроса
    update.message.reply_text(
        'Выберите с какими числами вы хотите работать',
        reply_markup=markup_key, )

    return CHOOSING # выбор вида чисел


def choosing(update, _):
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
        return OPERCHOICE2 # меню выбора оператора
    elif num_choiсe == 'Выход':
        logger.info("Пользователь %s вышел", user.first_name)
        update.message.reply_text(
            'Спасибо, что посетили нас',
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    else:
        pass


def oper_choice(update, _):
    user = update.message.from_user
    oper = update.message.text
    logger.info("Пользователь %s выбрал %s.", user.first_name,oper)
    if oper == "Сложение":
        update.message.reply_text('Введите два числа через пробел')
        return CATCHREPLY # сложение рациональных чисел
    elif oper == "Вычитание":
        update.message.reply_text('Введите два числа через пробел')
        return CATCHREPLY2 # вычитание рациональных чисел
    elif oper == "Возведение в степень":
        update.message.reply_text('Введите два числа через пробел')
        return CATCHREPLY3 # возведение в степень рациональных чисел
    elif oper == "Деление":
        reply_keyboard = [['Остаток', 'Целочисленное', 'Обычное', 'Главное меню']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, True)
        update.message.reply_text('Выберите тип деления', reply_markup=markup_key)
        return DIVISION # выбор вида деления 
    elif oper == "Корень квадратный числа":
        update.message.reply_text('Введите число')
        return CATCHREPLY4 # вычисляет квадратный корень числа
    elif oper == "Умножение":
        update.message.reply_text('Введите два числа через пробел')
        return MULTIPLY # вычисляет квадратный корень числа
    elif oper == "Главное меню":
        update.message.reply_text(
            'возвращение в главное меню',
        )
        return MAINMENU
    else:
        pass
     
def oper_choice2(update, _):
    oper = update.message.text
    if oper == "Сложение":
        update.message.reply_text('Введите четыре числа через пробел')
        return COMPLSUM 
    elif oper == "Вычитание":
        update.message.reply_text('Введите четыре числа через пробел')
        return COMPLSUB 
    elif oper == "Возведение в степень":
        update.message.reply_text('Введите четыре числа через пробел')
        return COMPLPOW 
    elif oper == "Деление":
        update.message.reply_text('Введите четыре числа через пробел')
        return COMPLDIV 
    elif oper == "Корень квадратный числа":
        update.message.reply_text('Введите два числа через пробел')
        return COMPLSQRT 
    elif oper == "Умножение":
        update.message.reply_text('Введите четыре числа через пробел')
        return COMPLMULT 
    elif oper == "Главное меню":
        update.message.reply_text(
            'возвращение в главное меню',
        )
        return MAINMENU       

def sum_oper(update, _):
    user = update.message.from_user
    msg = update.message.text
    print(msg)
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
        return CATCHREPLY


def subtraction_oper(update, _):
    user = update.message.from_user
    msg = update.message.text
    print(msg)
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
        return CATCHREPLY2


def power_oper(update, _):
    user = update.message.from_user
    msg = update.message.text
    print(msg)
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
        logger.error("Ошибка ввода", exc_info = True)
        return DIVISION


def div_rem(update, _):
    user = update.message.from_user
    msg = update.message.text
    items = msg.split()
    try:
        x = float(items[0])
        y = float(items[1])
        if y != 0:
            update.message.reply_text(f'{x}%{y} = {x % y}')
            logger.info("Пример пользователя %s: %s '%' %s = %s ", user.first_name, x, y, x%y)
            return DIVISION
        else:
            update.message.reply_text('На ноль делить нельзя! Попробуйте еще раз')
            logger.info("Пользователь %s ввел ноль", user.first_name)
            return CATCHREPLY5
    except:
        update.message.reply_text('Ошибка ввода')
        logger.error("Ошибка ввода", exc_info = True) # вот тут я применил метод error модуля logging и здесь я остановился с включением логов
        return CATCHREPLY5


def division_int(update, _):
    user = update.message.from_user
    msg = update.message.text
    items = msg.split()
    try:
        x = float(items[0])
        y = float(items[1])
        if y != 0:
            update.message.reply_text(f'{x}//{y} = {x // y}')
            logger.info("Пример пользователя %s: %s // %s = %s ", user.first_name, x, y, x//y)
            return DIVISION
        else:
            update.message.reply_text('На ноль делить нельзя! Попробуйте еще раз')
            logger.info("Пользователь %s ввел ноль", user.first_name)
            return CATCHREPLY6
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return CATCHREPLY6


def division(update, _):
    user = update.message.from_user
    msg = update.message.text
    items = msg.split()
    try:
        x = float(items[0])
        y = float(items[1])
        if y != 0:
            update.message.reply_text(f'{x}/{y} = {round((x / y),2)}')
            logger.info("Пример пользователя %s: %s / %s = %s ", user.first_name, x, y, x/y)
            return DIVISION
        else:
            update.message.reply_text('На ноль делить нельзя! Попробуйте еще раз')
            logger.info("Пользователь %s ввел ноль", user.first_name)
            return CATCHREPLY7
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return CATCHREPLY7

def sqrt_oper(update, _):
    user = update.message.from_user
    msg = update.message.text
    print(msg)
    try:
        x = float(msg)
        update.message.reply_text(f'√{x}= {round(sqrt(x),2)}')
        logger.info("Пример пользователя %s: √%s = %s ", user.first_name, x, sqrt(x))
        return OPERCHOICE # меню выбора оператора 
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return CATCHREPLY4
    
def multiply(update, _):
    user = update.message.from_user
    msg = update.message.text
    print(msg)
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
    
    
def sum_compl(update, _):
    user = update.message.from_user
    msg = update.message.text
    print(msg)
    items = msg.split() 
    try:
        x = complex(float(items[0]), float(items[1]))
        y = complex(float(items[2]), float(items[3]))
        update.message.reply_text(f'{x}+{y} = {x + y}')
        logger.info("Пример пользователя %s: %s + %s = %s ", user.first_name, x, y, x+y)
        return OPERCHOICE2 # меню выбора оператора
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return COMPLSUM
    
def sub_compl(update, _):
    user = update.message.from_user
    msg = update.message.text
    print(msg)
    items = msg.split() 
    try:
        x = complex(float(items[0]), float(items[1]))
        y = complex(float(items[2]), float(items[3]))
        update.message.reply_text(f'{x}-{y} = {x - y}')
        logger.info("Пример пользователя %s: %s - %s = %s ", user.first_name, x, y, x-y)
        return OPERCHOICE2 # меню выбора оператора
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return COMPLSUB
    
def mult_compl(update, _):
    user = update.message.from_user
    msg = update.message.text
    print(msg)
    items = msg.split()  
    try:
        x = complex(float(items[0]), float(items[1]))
        y = complex(float(items[2]), float(items[3]))
        update.message.reply_text(f'{x}*{y} = {x * y}')
        logger.info("Пример пользователя %s: %s * %s = %s ", user.first_name, x, y, x*y)
        return OPERCHOICE2 # меню выбора оператора
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return COMPLMULT
    
def div_compl(update, _):
    user = update.message.from_user
    msg = update.message.text
    print(msg)
    items = msg.split()  
    try:
        x = complex(float(items[0]), float(items[1]))
        y = complex(float(items[2]), float(items[3]))
        update.message.reply_text(f'{x}/{y} = {x / y}')
        logger.info("Пример пользователя %s: %s / %s = %s ", user.first_name, x, y, x/y)
        return OPERCHOICE2 # меню выбора оператора
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return COMPLDIV
    
def pow_compl(update, _):
    user = update.message.from_user
    msg = update.message.text
    print(msg)
    items = msg.split() 
    try:
        x = complex(float(items[0]), float(items[1]))
        y = complex(float(items[2]), float(items[3]))
        update.message.reply_text(f'{x}**{y} = {x ** y}')
        logger.info("Пример пользователя %s: %s ** %s = %s ", user.first_name, x, y, x**y)
        return OPERCHOICE2 # меню выбора оператора
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return COMPLPOW
    
def sqrt_compl(update, _):
    user = update.message.from_user
    msg = update.message.text
    print(msg)
    items = msg.split()
    try:
        x = complex(float(items[0]), float(items[1]))
        update.message.reply_text(f'√{x}= {sc(x)}')
        logger.info("Пример пользователя %s: √ %s = %s ", user.first_name, x, sc(x))
        return OPERCHOICE2 # меню выбора оператора
    except:
        update.message.reply_text('Вы ввели неправильно, введите еще раз')
        logger.error("Ошибка ввода", exc_info = True)
        return COMPLSQRT    
         
    

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
    updater = Updater("Token")
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
            OPERCHOICE2: [MessageHandler(Filters.regex(f'^{operation_keybord_main}$'), oper_choice2)],
            CATCHREPLY: [MessageHandler(Filters.text & ~Filters.command, sum_oper)],
            CATCHREPLY2: [MessageHandler(Filters.text & ~Filters.command, subtraction_oper)],
            CATCHREPLY3: [MessageHandler(Filters.text & ~Filters.command, power_oper)],
            CATCHREPLY4: [MessageHandler(Filters.text & ~Filters.command, sqrt_oper)],
            DIVISION: [MessageHandler(Filters.regex('^(Остаток|Целочисленное|Обычное|Главное меню)$'), division_ch)],
            CATCHREPLY5: [MessageHandler(Filters.text & ~Filters.command, div_rem)],
            CATCHREPLY6: [MessageHandler(Filters.text & ~Filters.command, division_int)],
            CATCHREPLY7: [MessageHandler(Filters.text & ~Filters.command, division)],
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
