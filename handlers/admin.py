from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import bot,dp
from data_base import sql_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton


ID = None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()



#@dp.register_message_handler(commands=['moderator'], is_chat_admin = True)
async def make_changes_command(message: types.Message):
    global ID
    ID=message.from_user.id
    await bot.send_message(message.from_user.id, 'What do you need?',reply_markup=admin_kb.button_case_admin)
    await message.delete()

#@dp.message_handler(commands=['Download'], state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Download photo')


#@dp.message_handler(state="*", commands=['Cancel'])
#@dp.message_handler(Text(equals='Cancel',ignore_case=True),state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Ok')

#@dp.message_handler(content_types=['photo'],state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply('Type name of pizza')

#@dp.message_handler(state=FSMAdmin.name)
async def load_name(message:types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply('Type comment')


#@dp.message_handler(state = FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.reply('Put a price')


#@dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)
    await sql_db.sql_add_command(state)
    await state.finish()



#@dp.callback_query_handler(lambda x: x.data and x.data.startwith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sql_db.sql_delete_command(callback_query.data.replace('del ',''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ","")} deleted', show_alert=True)


#@dp.message_handler(commands=['Delete'])
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sql_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret["img"],f'{ret["name"]}\nDescription: {ret["description"]}\nPrice: {ret["price"]}')
            await bot.send_message(message.from_user.id, text='^^^',reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f'Delete{ret["name"]}',callback_data=f'del {ret["name"]}')))



def register_handlers_admin(dp:Dispatcher):
    dp.register_message_handler(cm_start,commands=['Download'],state=None)
    dp.register_message_handler(cancel_handler, Text(equals='Cancel',ignore_case=True), state="*")
    dp.register_message_handler(load_photo,content_types=['photo'],state=FSMAdmin.photo)
    dp.register_message_handler(load_name,state=FSMAdmin.name)
    dp.register_message_handler(load_description,state=FSMAdmin.description)
    dp.register_message_handler(load_price,state=FSMAdmin.price)
    dp.register_message_handler(cancel_handler,state="*",commands=['Cancel'])
    dp.register_message_handler(make_changes_command,commands=['moderator'], is_chat_admin = True)
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(delete_item, commands=['Delete'])