from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = InlineKeyboardMarkup(row_width=2)
btn3 = InlineKeyboardButton(text="☎️ Xabar Yuborish", callback_data="personal_link")
menu.add(btn3)

back = InlineKeyboardMarkup(row_width=1)
cancel = InlineKeyboardButton(text='🔙 Bekor qilish',callback_data="cancel")
back.add(cancel)

