import asyncio

import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.all_or_one import send_ans
from keyboards.inline.menu import menu,back
from data.config import ADMINS
from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from states.ads import One
from states.sendMessage import Message


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    # ADD USER IN DB
    try:
        await db.add_user(
            telegram_id=message.from_user.id,
            full_name=name,
            username=message.from_user.username
        )
        await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!\n<a href='https://t.me/xaqulislom'>🫀Xaq Ul Islom🫀 Mع🙃</a> Telegram kanalining adminiga murojaat qilish uchun mo'ljallangan rasmiy bot. \n\nXabaringizni yuboring: ",disable_web_page_preview=True)
        count = await db.select_all_user()
        msg = f"{message.from_user.full_name} bazaga qo'shildi.\nBazada {len(count)} ta foydalanuvchi bor."
        try:
            for user in ADMINS:
                await bot.send_message(user, msg)
        except:
            pass

    except asyncpg.exceptions.UniqueViolationError:
        await message.answer(f"Hurmatli Foydalanuvchi siz Bot ga a'zo bo'lgansiz bemalol foydalanishingiz mumkin.\n\nXabaringizni yuboring: ")

@dp.message_handler(content_types=["text","file","video","photo","audio","location"])
async def get_text(msg: types.Message, state:FSMContext):
    text_type = msg.content_type
    try:
        text_html = msg.html_text
        # rep_btn = msg.reply_markup
        text_caption = msg.caption
        rep_btn = await send_ans(msg.from_user.first_name)
        post = f"{text_html}\n\n"
        post += f"👆 Bu Xabar <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.full_name}</a> tomonidan yuborildi.\n" \
                f"ID – <code>{msg.from_user.id}</code>"
        post1 = f"{text_caption}\n\n"
        post1 += f"👆 Bu Xabar <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.full_name}</a> tomonidan yuborildi.\n" \
               f"ID – <code>{msg.from_user.id}</code>"
    except:
        await msg.answer("Faylining tagiga matn yozing")
    try:
        for user_id in ADMINS:
            if text_type == 'sticker':
                return
            elif text_type == 'text':
                await bot.send_message(chat_id=user_id, text=post, reply_markup=rep_btn)
                await asyncio.sleep(0.05)
            elif text_type == 'video':
                await bot.send_video(user_id, msg.video.file_id, caption=post1, reply_markup=rep_btn)
                await asyncio.sleep(0.05)
            elif text_type == 'photo':
                await bot.send_photo(user_id, msg.photo[-1].file_id, caption=post1, reply_markup=rep_btn)
                await asyncio.sleep(0.05)
            elif text_type == 'audio':
                await bot.send_audio(user_id, msg.audio, reply_markup=rep_btn)
                await asyncio.sleep(0.05)
            elif text_type == 'location':
                lat = msg.location['latitude']
                lon = msg.location['longitude']
                await bot.send_location(chat_id=user_id, latitude=lat, longitude=lon, reply_markup=rep_btn)
                await asyncio.sleep(0.05)
        await msg.answer(f"Sizning xabaringiz Adminga yuborildi.")
    except Exception:
        for i in ADMINS:
            await bot.send_message(chat_id=int(i), text="Xabar yuborilmadi")



@dp.callback_query_handler(text_contains="reklama:")
async def get_id(call: CallbackQuery, state:FSMContext):
    await call.answer()
    user_id = ""
    user_id1 = ""
    if call.message.caption:
        user_id1 = call.message.caption.split("ID – ")[1]
    elif call.message.text:
        user_id = call.message.text.split("ID – ")[1]
    if len(user_id)>0:
        name1 = await db.get_one_by_id(int(user_id))
        await call.message.answer(f"{name1[1]} ga xabaringizni yuboring: ")
    elif len(user_id1)>0:
        name2 = await db.get_one_by_id(int(user_id1))
        await call.message.answer(f"{name2[1]} ga xabaringizni yuboring: ")
    await call.message.delete()
    await state.update_data(
        {
            "user_id":user_id,
            "caption_id":user_id1
        }
    )
    await One.text.set()

@dp.message_handler(state=One.text, content_types=["text","video","photo","file","location","audio"])
async def send_message_to_user(msg: types.Message, state:FSMContext):
    text_caption = msg.caption
    text_type = msg.content_type
    data = await state.get_data()
    user_id = None
    caption_id = None
    if data["caption_id"]:
        caption_id = data["caption_id"]
    elif data["user_id"]:
        user_id = data["user_id"]
    text = msg.html_text
    rep_btn = msg.reply_markup
    try:
        if caption_id:
            if text_type == 'sticker':
                return
            elif text_type == 'text':
                await bot.send_message(chat_id=caption_id, text=text, reply_markup=rep_btn)
                await asyncio.sleep(0.05)
            elif text_type == 'video':
                await bot.send_video(caption_id, msg.video.file_id, caption=text_caption, reply_markup=rep_btn)
                await asyncio.sleep(0.05)
            elif text_type == 'photo':
                await bot.send_photo(caption_id, msg.photo[-1].file_id, caption=text_caption, reply_markup=rep_btn)
                await asyncio.sleep(0.05)
            elif text_type == 'audio':
                await bot.send_audio(caption_id, msg.audio, reply_markup=rep_btn)
                await asyncio.sleep(0.05)
            elif text_type == 'location':
                lat = msg.location['latitude']
                lon = msg.location['longitude']
                await bot.send_location(chat_id=caption_id, latitude=lat, longitude=lon, reply_markup=rep_btn)
                await asyncio.sleep(0.05)
        if user_id:
            if text_type == 'sticker':
                return
            elif text_type == 'text':
                await bot.send_message(chat_id=user_id, text=text, reply_markup=rep_btn)
                await asyncio.sleep(0.05)
            elif text_type == 'video':
                await bot.send_video(user_id, msg.video.file_id, caption=text_caption, reply_markup=rep_btn)
                await asyncio.sleep(0.05)
            elif text_type == 'photo':
                await bot.send_photo(user_id, msg.photo[-1].file_id, caption=text_caption, reply_markup=rep_btn)
                await asyncio.sleep(0.05)
            elif text_type == 'audio':
                await bot.send_audio(user_id, msg.audio, reply_markup=rep_btn)
                await asyncio.sleep(0.05)
            elif text_type == 'location':
                lat = msg.location['latitude']
                lon = msg.location['longitude']
                await bot.send_location(chat_id=user_id, latitude=lat, longitude=lon, reply_markup=rep_btn)
                await asyncio.sleep(0.05)
        await bot.send_message(chat_id=msg.from_user.id,text="Xabar yuborildi.")
    except Exception:
        await bot.send_message(chat_id=msg.from_user.id,text="Yuborilmadi.")
    await state.finish()
