import telebot
from telebot import types

token = "5068905941:AAEEFSp2gdzp6fwZunn93LwvDdb_tYeYjsc"

moderators_chat_id = "-1001672829183"
main_chat_id = "-1001512533450"


bot = telebot.TeleBot(token)

confirm_inline_keyboard = types.InlineKeyboardMarkup()
accept_button = types.InlineKeyboardButton('Accept', callback_data='accept_message')
decline_button = types.InlineKeyboardButton('Decline', callback_data='decline_message')
confirm_inline_keyboard.add(accept_button, decline_button)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.chat.type != "supergroup":
        bot.send_message(moderators_chat_id,
                         f"\n@{message.from_user.username} \n {message.text}",
                         reply_markup=confirm_inline_keyboard)
    else:
        pass


@bot.callback_query_handler(lambda call: True)
def handle(call):
    print(call)
    if call.data == "accept_message":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=call.message.text+f"\n[Accepted by @{call.from_user.username}]")
        message = call.message.text.split("\n", maxsplit=1)[1]
        bot.send_message(main_chat_id, message)

    elif call.data == "decline_message":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=call.message.text+f"\n[Declined by @{call.from_user.username}]")


bot.polling(none_stop=True, interval=0)
