import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from random import randint as RI


bot = telebot.TeleBot("5845643823:AAGgY8Qe0xuJKaSh0bFnteEKh0oGwvm7-_Y", parse_mode=None)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello buddy', reply_markup=set_menu_buttons())

def set_menu_buttons() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    calculate_btn = KeyboardButton('Calculate')
    quiz_btn = KeyboardButton('Guess the number')
    keyboard.add(calculate_btn, quiz_btn)
    return keyboard

def calculate(message):
    bot.send_message(message.from_user.id,'Result: ' + str(eval(message.text)))


def quiz(message, counts, right_number):
    if message.text.isdigit():
        if right_number == int(message.text):
            bot.send_message(message.from_user.id, f"That's right, you did it with {counts} attempts")
        else:
            if right_number < int(message.text):
                bot.send_message(message.from_user.id, f"Your answer is more then my number")
            else:
                bot.send_message(message.from_user.id, f"Your answer is less then my answer")
                bot.register_next_step_handler(message, quiz, counts + 1, right_number)
    else:
        bot.send_message(message.from_user.id, f"Enter number and try again")
        bot.register_next_step_handler(message, quiz, counts, right_number)

@bot.message_handler(content_types=['text'])
def start(message):
    if 'Calculate' in message.text:
        bot.reply_to(message, 'Enter expressions for calculation:')
        bot.register_next_step_handler(message, calculate)
    elif 'Guess the number' in message.text:
        rnumber = RI(1,1000)
        bot.reply_to(message, 'Try to guess a number from 1 to 1000')
        bot.register_next_step_handler(message, quiz, 1, rnumber)


bot.infinity_polling()