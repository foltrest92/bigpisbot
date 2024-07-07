import logging
from aiogram import F, Bot, Router, types
from aiogram.filters import Command
from app.config import settings
from uuid import uuid4

from app.dao.buy import BuyDAO, PaymentsDAO


router = Router()

@router.message(Command('buy'))
async def buy(message: types.Message):
    logging.debug('msg from '+str(message.from_user.id)+' in '+str(message.chat.id)+':'+message.text)
    if message.chat.id < 0:
        await message.answer('Команда работает только в лс')
        return
    kb = [
        [types.InlineKeyboardButton(text='10 попыток (100 рублей)', callback_data='buy_10')]
    ]
    # await message.answer(f"В настоящий момент недоступно\n\nОферта: {settings.OFERTA_URL}")
    await message.answer("Выбери вариант:", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb))

@router.callback_query(F.data == 'buy_10')   
async def sub_bay(callback: types.CallbackQuery):
    logging.debug('start buing from '+str(callback.from_user.id))
    payment = {
        'user_id': callback.from_user.id,
        'payload': str(uuid4()),
        'price': 10000,
        'product': 10
    }
    await PaymentsDAO.add(user_id=payment['user_id'], payload=payment['payload'], price=payment['price'], product=payment['product'])
    logging.info('Payment: '+str(payment))
    await callback.bot.send_invoice(chat_id=callback.from_user.id,
                           title="Дополнительные попытки",
                           description="10 дополнительных попыток",
                           provider_token=settings.PAYMENT_TOKEN,
                           currency="rub",
                           photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[types.LabeledPrice(label="10 попыток", amount=payment['price'])],
                           start_parameter="ten_att",
                           payload=payment['payload'])

@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    print(pre_checkout_query.invoice_payload)
    logging.debug(f"CHECKOUT: {pre_checkout_query}")

@router.message(F.successful_payment)
async def successful_payment(message: types.Message):
    payment = await PaymentsDAO.update(message.successful_payment.invoice_payload, status=2)
    old_payment = await BuyDAO.find_one_or_none(user_id=payment.user_id)
    if old_payment:
        await BuyDAO.update(payment.user_id, using_remain=old_payment.using_remain+payment.product)
    else:
        await BuyDAO.add(
            user_id = payment.user_id,
            using_remain = payment.product
        )
    await message.answer('Оплата прошла успешно! Введите /dick в беседе')
    pay_info = ''
    for j,k in message.successful_payment:
        pay_info += f"{j} = {k}, "
    logging.info(pay_info)