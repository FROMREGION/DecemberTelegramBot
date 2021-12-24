from aiogram import types

confirm_inline_keyboard = types.InlineKeyboardMarkup()
accept_button = types.InlineKeyboardButton('Accept ✅', callback_data='accept_message')
decline_button = types.InlineKeyboardButton('Decline ❌', callback_data='decline_message')
confirm_inline_keyboard.add(accept_button, decline_button)