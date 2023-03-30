from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def help_user(message: types.Message):
    msg = f"Bot Tomonidan foydalanuvchiga yordam ko'rsatish bo'limi\n" \
          f"Buyruqlar:\n/start — Botni ishga tushirish\n" \
          f"/help — Yordam Ko'rsatish va Bot ishlash tartibi\n\n" \
          f"<b>Botni ishlash tartibi</b>\n\n" \
          f"1.<a href='https://t.me/xaqulislom'>🫀Xaq Ul Islom🫀 Mع🙃</a> Telegram kanalining adminiga murojaat qilish uchun mo'ljallangan rasmiy bot."

    await message.reply(msg)

