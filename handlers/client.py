from aiogram import types,Dispatcher
#from aiogram.dispatcher import FSMContext
#from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from keyboards import kb_client
#from aiogram.types import  ReplyKeyboardRemove
from keys_token import tokens
from data_base import sql_db
import json

class forpayments():
    order_list = ''



#@dp.message_handler(commands=['start','help'])
async def command_start(message:types.Message):
    await bot.send_message(message.from_user.id, 'Нажміть на кнопку "Menu", щоб здійснити покупки',reply_markup=kb_client)


def datatake(data):
    items = json.loads(data)
    del items[0]
    order = ''
    price_list = list()
    for item in items:
        s1 = item["name"]+" - "+str(item["quantity"])
        order += s1 +'; '
        price_list.append(types.LabeledPrice(label=s1,amount = int(item["price"]*100) * item["quantity"]))
    return [order,price_list]

async def data_from_app(message : types.Message):
    prices = datatake(message.web_app_data.data)
    forpayments.order_list = prices[0]
    await bot.send_message(message.chat.id,
                           "Гарний вибір, залишилось за нього тільки заплатити. Використайте цей номер картки для оплати: `4242 4242 4242 4242`"
                           "\n\nThis is your demo invoice:", parse_mode='Markdown')
    await bot.send_invoice(message.chat.id, title='Order of MacDonald',
                           description='Ням-ням',
                           provider_token=tokens.paytoken(),
                           currency='usd',
                           photo_url='https://www.cornerhouserestaurants.co.uk/templates/yootheme/cache/homepage-07-b0e63288.jpeg',
                           photo_height=512,  # !=0/None or picture won't be shown
                           photo_width=512,
                           #photo_size=512,
                           is_flexible=True,  # True If you need to set up Shipping Fee
                           #prices={types.LabeledPrice(label="Make an order",amount = prices)},
                           prices=prices[1],
                           start_parameter='McDonalds-menu',
                           payload='Custom-payload')


async def shipping(shipping_query: types.ShippingQuery):
    shipping_options = [
    types.ShippingOption(id='instant', title='Delivery').add(types.LabeledPrice('Delivery', 300)),
    types.ShippingOption(id='pickup', title='Local pickup').add(types.LabeledPrice('Pickup', 0)),]
    await bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                                    error_message='Oh, seems like our Dog couriers are having a lunch right now.'
                                                  ' Try again later!')


async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    ready = True
    if pre_checkout_query.invoice_payload != 'Custom-payload':
        ready = False
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=ready,
                                        error_message="Aliens tried to steal your card's CVV,"
                                                      " but we successfully protected your credentials,"
                                                      " try to pay again in a few minutes, we need a small rest.")


async def got_payment(message: types.Message):
    await bot.send_message(message.chat.id,
                           'Hoooooray! Thanks for payment! We will proceed your order for `{} {}`'
                           ' as fast as possible! Stay in touch.'.format(
                               message.successful_payment.total_amount / 100, message.successful_payment.currency),
                           parse_mode='Markdown')
    obj = [forpayments.order_list,message.successful_payment.order_info.shipping_address.city, message.successful_payment.total_amount/100]
    await sql_db.sql_add_command(obj)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start','help'])
    #dp.register_message_handler(pizza_open_comand,commands=['Time_work'])
    #dp.register_message_handler(pizza_place_comand,commands=['Location'])
    #dp.register_message_handler(pizza_menu_command, commands=['Menu'])
    dp.register_message_handler(data_from_app, content_types=['web_app_data'])
    dp.register_shipping_query_handler(shipping, lambda query: True)
    dp.register_pre_checkout_query_handler(checkout, lambda query: True)
    dp.register_message_handler(got_payment, content_types=types.message.ContentTypes.SUCCESSFUL_PAYMENT)