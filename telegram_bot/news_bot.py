import configparser
import json
import logging

import aiogram.utils.markdown as md
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

from telegram_bot.database import DBDriver
from telegram_bot.help_func_bot import show_list_keyword, verify_word
from telegram_bot.messages import MESSAGES, MessagesFunc

config = configparser.ConfigParser()
config.read("settings.ini")
bot = Bot(token=config["News_analyzer"]["token"])
storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)


class FormToAdd(StatesGroup):
    keyword = State()
    confirm_add = State()


class FormToRemove(StatesGroup):
    keyword = State()
    confirm_remove = State()


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    if DBDriver.is_new_user(user_id):
        user_dict = message.from_user.to_python()
        DBDriver.insert_user(user_dict)
        logging.info(f"Added new user:\n {json.dumps(user_dict, indent=4)}")
    else:
        await message.reply(MessagesFunc.prepare_welcome_msg(message.from_user.first_name))


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await bot.send_photo(message.from_user.id, 'https://ibb.co/m5ZB7Ph', MESSAGES['help'])


# todo: додати команду keyword_list для отримання списку ключових слів з додатковими атрибутами по рейтингу DONE
# todo: винести повідомлення, як константи в файл messages.py

@dp.message_handler(commands=['add_keyword'])
async def process_add_keyword_command(message: types.Message):
    await FormToAdd.keyword.set()
    await message.reply(MESSAGES['add_keyword'])


@dp.message_handler(state=FormToAdd.keyword)
async def process_add_keyword(message: types.Message, state: FSMContext):
    # todo: перевіряти на валідність ключові слова користувача DONE
    async with state.proxy() as data:
        data['keyword'] = message.text
        if verify_word(data['keyword']):
            await FormToAdd.next()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add("Так", "Ні")
            await message.reply(MESSAGES['confirm_remove_keyword'], reply_markup=markup)
        else:
            await message.reply(MESSAGES['wrong_word'])
            await state.finish()


@dp.message_handler(lambda message: message.text not in ["Так", "Ні"], state=FormToAdd.confirm_add)
async def process_add_confirm_invalid(message: types.Message):
    return await message.reply(MESSAGES['confirm_invalid'])


@dp.message_handler(state=FormToAdd.confirm_add)
async def process_confirm_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['confirm_add'] = message.text
        markup = types.ReplyKeyboardRemove()
        if data['confirm_add'] == "Так":
            data['user_id'] = message.from_user.id
            DBDriver.add_keyword(data)
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(MESSAGES['confirm_add_keyword'], '"', md.bold(data['keyword']), '"'),
                    sep='\n'
                ),
                reply_markup=markup,
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            await bot.send_message(message.chat.id, md.text(md.text(MESSAGES['add_no_change'])))
    await state.finish()


@dp.message_handler(commands=['remove_keyword'])
async def process_remove_keyword_command(message: types.Message):
    await FormToRemove.keyword.set()
    await message.reply(MESSAGES['remove_keyword'])


@dp.message_handler(state=FormToRemove.keyword)
async def process_remove_confirm_keyword(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['keyword'] = message.text
    await FormToRemove.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Так", "Ні")
    await message.reply(MESSAGES['confirm_remove_keyword'], reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["Так", "Ні"], state=FormToRemove.confirm_remove)
async def process_remove_invalid(message: types.Message):
    return await message.reply(MESSAGES['confirm_invalid'])


@dp.message_handler(state=FormToRemove.confirm_remove)
async def process_remove_keyword(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['confirm_remove'] = message.text
        markup = types.ReplyKeyboardRemove()
        if data['confirm_remove'] == 'Так':
            data['user_id'] = message.from_user.id
            DBDriver.remove_keyword(data)
            await bot.send_message(
                message.chat.id,
                md.text(
                    md.text(MessagesFunc.delete_keyword(md.bold(data['keyword']))),
                    sep='\n'
                ),
                reply_markup=markup,
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            await bot.send_message(message.chat.id, md.text(md.text(MESSAGES['remove_no_change'])))
    await state.finish()


@dp.message_handler(commands=['list_keyword'])
async def process_remove_keyword_command(message: types.Message):
    data = DBDriver.list_keyword(message.from_user.id)
    if not data:
        await bot.send_message(message.from_user.id, MESSAGES['empty_list_user'])
    else:
        await bot.send_message(message.from_user.id, MessagesFunc.show_keywords(show_list_keyword(data)))


if __name__ == '__main__':
    executor.start_polling(dp)
