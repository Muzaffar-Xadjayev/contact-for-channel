from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

cancel = InlineKeyboardMarkup(row_width=1)
btn = InlineKeyboardButton(text="🔙 Bekor qilish",callback_data="bekor_qilish")
cancel.add(btn)