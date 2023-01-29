import os
import logging
import glob

from aiogram import Bot
from aiogram import types
from aiogram import executor
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.types.message import ContentType
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup

from nst import load_net
from nst import make_nst
from nst import load_images
from config import TOKEN_API
from messages import MESSAGES


class BotStates(StatesGroup):
    LOAD_CONTENT_STATE = State()
    LOAD_STYLE_STATE = State()
    MAKE_NST_STATE = State()


bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(level=logging.INFO)

help_button = KeyboardButton(text='/help')
style_button = KeyboardButton(text='/style')
example_button = KeyboardButton(text='/example')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(help_button)
keyboard.add(style_button)
keyboard.add(example_button)


async def delete_photos(user_id):
    removing_files = glob.glob(f'bot_photo/{user_id}*.jpg')
    for i in removing_files:
        os.remove(i)


async def do_nst(content_path,
                 style_path,
                 output_path):
    content_image, style_image = load_images(content_image_path=content_path,
                                             style_image_path=style_path)
    net = load_net()
    make_nst(net, content_image, style_image, output_path=output_path)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply(text=MESSAGES['start'], reply=False, reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=MESSAGES['help'], reply=False, reply_markup=keyboard)


@dp.message_handler(commands=['example'], state='*')
async def send_examples(message: types.Message):
    media = types.MediaGroup()
    media.attach_photo(types.InputFile(
        'example/me_for_exp.jpg'), 'Content image')
    media.attach_photo(types.InputFile(
        'example/style_3.jpg'), 'Style image')
    media.attach_photo(types.InputFile('example/example.jpg'), 'Output image')
    await message.reply_media_group(media, reply=False)


@dp.message_handler(state='*', commands=['style'])
async def nst_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)

    await BotStates().LOAD_CONTENT_STATE.set()
    await message.reply(text='Загрузи картинку с контентом\n')


@dp.message_handler(state=BotStates.LOAD_CONTENT_STATE, content_types=types.ContentType.PHOTO)
async def load_content(message: types.Message):
    state = dp.current_state(user=message.from_user.id)

    await message.photo[-1].download(destination='bot_photo/{}_content.jpg'.format(message.from_user.id))
    await BotStates().LOAD_STYLE_STATE.set()
    await message.reply(text='Теперь загрузи картинку, стиль которой будем переносить!',
                        reply=False)


@dp.message_handler(state=BotStates.LOAD_STYLE_STATE, content_types=types.ContentType.ANY)
async def load_style(message: types.Message):
    state = dp.current_state(user=message.from_user.id)

    await message.photo[-1].download(destination='bot_photo/{}_style.jpg'.format(message.from_user.id))
    await BotStates().MAKE_NST_STATE.set()
    await make_style(message)


@dp.message_handler(state=BotStates.MAKE_NST_STATE, content_types=types.ContentType.PHOTO)
async def make_style(message: types.Message):
    state = dp.current_state(user=message.from_user.id)

    await message.answer(text='Обработка займет меньше минуты!')

    content_path = 'bot_photo/{}_content.jpg'.format(message.from_user.id)
    style_path = 'bot_photo/{}_style.jpg'.format(message.from_user.id)
    output_path = 'bot_photo/{}_output.jpg'.format(message.from_user.id)

    await do_nst(content_path, style_path, output_path)

    media = types.MediaGroup()
    media.attach_photo(types.InputFile(content_path), 'Content image')
    media.attach_photo(types.InputFile(style_path), 'Style image')
    media.attach_photo(types.InputFile(output_path), 'Output image')

    await message.reply_media_group(media, reply=False)
    await message.answer(text=MESSAGES['end'])
    await state.reset_state()
    await delete_photos(message.from_user.id)


@dp.message_handler(state='*')
async def echo(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=MESSAGES['echo'])


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)
