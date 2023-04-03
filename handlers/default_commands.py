from aiogram import Router, types
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=['start']))
async def send_start(message: Message):
    """The start command handler"""
    kb = [
            [
                # types.KeyboardButton(text="New conversation"),
                types.KeyboardButton(text="Начать новый диалог"),
                ],
            ]
    keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder="Select one"
            )

    await message.answer_photo(
        'https://telegra.ph/file/f5455a3fb9b56804db143.jpg')
    await message.answer("Привет! \nЯ - это искусственный интеллект которым вы можете пользоваться через бота, разработанного гением на фотографии выше, для общения с людьми. Я могу ответить на ваши вопросы, помочь с поиском информации в Интернете, предоставить советы и рекомендации, а также выполнить некоторые задачи, связанные с обработкой языка. Я могу общаться на нескольких языках, включая английский, испанский, французский, немецкий, итальянский, португальский, голландский, русский и многие другие. \nНе забвайте, что я могу отвечать на ваши вопросы основываясь на информации доступной в интернете до 2021 года.\nТак же я использую движок 'gpt-3.5-turbo', который использует официальный сайт в том числе.\nВыберите что-нибудь на клавиатуре ниже", reply_markup=keyboard)
    # await message.answer("Hi! I am a chatGPT bot designed by a genius who is above.\n Do not forget that my answers will be based on information published before 2021.\nI am on engine named 'gpt-3.5-turbo'.\nSelect something on keyboard", reply_markup=keyboard)
