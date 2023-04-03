"""Import typing extentions"""
from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.filters import Text
from request import Chat
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import new_conv

router = Router()


@router.message(Text(text="Back to other conversations"))
async def all_conv(message: Message):
    """the coverstaion history"""
    user_id = message.from_user.id
    chat_id = message.chat.id

    builder = ReplyKeyboardBuilder()
    for i in range(new_conv.convs_count[user_id]+1):
        builder.add(types.KeyboardButton(text=new_conv.users[user_id][chat_id][i][0]))
    builder.adjust(2)

    await message.answer(
            "Select the conversation you want to return to.",
            reply_markup=builder.as_markup(resize_keyboard=True)
            )

