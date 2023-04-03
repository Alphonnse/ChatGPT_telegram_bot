"""Import typing extentions"""
import os
from dotenv import load_dotenv
from aiogram import Router, types, F
from aiogram.types import Message
from aiogram import types
from aiogram.filters import Text
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import Bot
from request import Chat

load_dotenv()
router = Router()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

users = {}
request_count = {}  # For the support message
convs_count = {}  # convs iteration


"""keyboard"""

kb = [
        [
            types.KeyboardButton(text="Начать новый диалог"),
            types.KeyboardButton(text="Вернуться к старым диалогам"),
            # types.KeyboardButton(text="New conversation"),
            # types.KeyboardButton(text="Back to other conversations"),
        ],
    ]
keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
    input_field_placeholder="Select one"
    )


# @router.message(Text(text="New conversation"))
@router.message(Text(text="Начать новый диалог"))
async def start_conv(message: Message):
    """Handling the new conversation command"""
    user_id = message.from_user.id
    chat_id = message.chat.id

    if user_id not in convs_count:
        convs_count[user_id] = 0
    else:
        j = 0
        while users[user_id][chat_id][j][0] is not None:
            j += 1
        convs_count[user_id] = j
        if convs_count[user_id] == 4:
            convs_count[user_id] = 0

    if user_id not in users:
        chats = {}
        users[user_id] = chats
        if chat_id not in chats:
            conversations = [list((None, None)) for x in range(5)]
            chats[chat_id] = conversations

    users[user_id][chat_id][convs_count[user_id]][1] = Chat()
    users[user_id][chat_id][convs_count[user_id]][1].get_api()
    users[user_id][chat_id][convs_count[user_id]][1].add_system()

    await message.answer(
        # "You have started a new conversation without context.",
        "Вы начали новый диалог без контекста.",
        reply_markup=keyboard
    )

    if user_id not in request_count:
        request_count[user_id] = 1
    else:
        request_count[user_id] += 1
        if request_count[user_id] % 4 == 0:
            await message.answer(
                "По ссылке ниже можно поддержать разработчика. 👉👈\nhttps://www.tinkoff.ru/rm/dertsyan.narek1/3q6pb4506"
            )


# @router.message(Text(text="Back to other conversations"))
@router.message(Text(text="Вернуться к старым диалогам"))
async def all_conv(message: Message):
    """the coverstaion history"""
    user_id = message.from_user.id
    chat_id = message.chat.id
   
    builder = ReplyKeyboardBuilder()
    j = 0
    while users[user_id][chat_id][j][0] is not None:
        j += 1
    if j == 0:
        # await message.answer("There are no conversations yet")
        await message.answer("У вас пока нет диалогов")
    else:
        for i in range(j):
            builder.add(types.KeyboardButton(text=users[user_id][chat_id][i][0]))
        builder.adjust(2)

        await message.answer(
               # "Select the conversation you want to return to.",
               "Выберите диалог к которому вы хотите вернуться.",
                reply_markup=builder.as_markup(resize_keyboard=True)
                )


@router.message(F.text)
async def request(message: types.Message):
    """Handling the user messages"""

    changed = False
    user_id = message.from_user.id
    chat_id = message.chat.id

    if user_id not in users:
        await start_conv(message)
        user_id = message.from_user.id
        chat_id = message.chat.id

    for i in range(convs_count[user_id]+1):
        if message.text == users[user_id][chat_id][i][0]:
            convs_count[user_id] = i
            await message.answer(
                    # "Now, you have change the conversation context",
                    "Вы перешли к диалогу с другим контекстом",
                    reply_markup=keyboard
                    )
            changed = True

    if changed is False:
        await bot.send_chat_action(chat_id, "typing")
        response = users[user_id][chat_id][convs_count[user_id]][1].get_answer(message.text)
        users[user_id][chat_id][convs_count[user_id]][0] = users[user_id][chat_id][convs_count[user_id]][1].conversation_name(response)
        await message.answer(f"{response}")

