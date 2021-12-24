from aiogram import Bot, Dispatcher, executor, types
from keyboard import confirm_inline_keyboard
from config import token, moderators_chat_id, main_chat_id, group

bot = Bot(token=token)
dp = Dispatcher(bot)


# Message handler -----------------------------------------------------------------------------------------------------
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message_handler()
async def reply(message: types.Message):
    if message.chat.type not in group:
        try:
            await bot.send_message(moderators_chat_id,
                                   f"\n@{message.from_user.username} \n {message.text}",
                                   reply_markup=confirm_inline_keyboard)
        except:
            await bot.send_message(message.chat.id, "На данный момент превышен лимит одновременных сообщений "
                                                    "всех пользователей боту. Попробуйте снова через 1 минуту.")


# Callback handlers ----------------------------------------------------------------------------------------------------
@dp.callback_query_handler()
async def process_callback(call: types.CallbackQuery):
    if call.data == "accept_message":
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=call.message.text+f"\n[Accepted by @{call.from_user.username}]")
        message = call.message.text.split("\n", maxsplit=1)[1]
        await bot.send_message(main_chat_id, message)
    elif call.data == "decline_message":
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=call.message.text+f"\n[Declined by @{call.from_user.username}]")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
