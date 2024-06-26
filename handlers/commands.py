from aiogram import Router, F
from aiogram.filters import Command, CommandStart 
from aiogram.types import (
    Message, ReplyKeyboardMarkup, KeyboardButton, 
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, FSInputFile
)

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    description = (
        "👩‍💻Здравствуйте!!! Мы кадровое агентство ПроКонсалт, помогаем в поиске работы!!! \n"
    )
    kb = [
        [KeyboardButton(text="/start")], 
        [KeyboardButton(text="/OF_US")],
        [KeyboardButton(text="/Headhunter")], 
        [KeyboardButton(text="/Facebook")],
        [KeyboardButton(text="/бизнес_клуб_Атланты")],  
        [KeyboardButton(text="/Ostavit_zayavku")],
        # [KeyboardButton(text="/add_client1")],
        [KeyboardButton(text="/end")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(description, reply_markup=keyboard)



@router.message(Command(commands=['OF_US']))
async def OF_US(message:Message):
    CONTACTS = (
        "Мы - ПроКонсалт \n"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="OF_US", callback_data="1")],
        ])

    await message.answer(CONTACTS,reply_markup=keyboard)



@router.callback_query(F.data=="1")
async def send_1_picture(callback:CallbackQuery):
    await callback.message.answer_photo(
        photo=FSInputFile("1.jpg"),
        caption = ( # Описание к фото
            "Телеграм: https://t.me/ \n"
            "Инстаграм: https://www.instagram.com/proconsultkg/ \n"
            "Тел: +996997777733 \n"
            "График работы: Пн-Пт 08:30–17:30,Обед 12:30–13:30, Выходной Субб-Вс \n"
            "Адрес: Токтогула, 147, 2 этаж, 40/1 офис, Первомайский район, Бишкек, 720001 \n"
            "Ссылка на сайт: https://finjust.kg/ru/ \n"
        )
    )

@router.message(Command(commands=['Headhunter']))
async def Headhunter(message:Message):
    await message.answer(
        "Ссылка, на сайт - https://bishkek.headhunter.kg/ \n",
    )


@router.message(Command(commands=['Facebook']))
async def Facebook(message:Message):
    await message.answer(
        "Ссылка, на сайт - https://www.facebook.com/ \n",
    )


@router.message(Command(commands=['бизнес_клуб_Атланты']))
async def бизнес_клуб_Атланты(message:Message):
    await message.answer(
        "Ссылка, на сайт - https://atlanty.ru/ \n",
    )




# Обработчик для команды /end
@router.message(Command(commands=['end']))
async def end(message: Message):
    await message.answer("Спасибо, что воспользовались helpfindwork_bot! До новых встреч!", 
                        show_alert=True)










from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from main import *


ADMIN_CHAT_ID = ("6673864170")  # вставляете свой chat id
bot_instance: Bot = None  # Глобальная переменная для хранения экземпляра бота


class Form(StatesGroup):
    name = State()  # Состояние для ФИО
    age = State()
    phone_number = State()  # Состояние для номера телефона
    chat_id = State()
    experience = State()

def setup_routers(dispatcher: Dispatcher, bot: Bot):
    global bot_instance
    bot_instance = bot  # Сохраняем экземпляр бота для использования в хэндлерах
    dispatcher.include_router(router)


@router.message(Command("Ostavit_zayavku"))
async def cmd_ostavit_zayavku(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, введите ваше ФИО:")
    await state.set_state(Form.name)


@router.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Теперь введите ваш возраст:")
    await state.set_state(Form.age)



@router.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Теперь введите ваш номер телефона:")
    await state.set_state(Form.phone_number)


@router.message(Form.phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer("Теперь введите ваш chat_id:")
    await state.set_state(Form.chat_id)


@router.message(Form.chat_id)
async def process_chat_id(message: Message, state: FSMContext):
    await state.update_data(chat_id=message.text)
    await message.answer("Опыт работы:")
    await state.set_state(Form.experience)

@router.message(Form.experience)
async def process_experience(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    data = await state.get_data()

    # Формируем сообщение о принятой заявке
    response_message = (
        f"Заявка принята!\n"
        f"ФИО: {data['name']}\n"
        f"Номер телефона: {data['phone_number']}\n"
        f"Chat_id: {data['chat_id']}\n"
        f"Опыт работы: {data['experience']}\n"
        f"Новый клиент! Позвоните для подтверждения заявки на номер +996997777733!"
    )



    # Отправляем сообщение администратору
    user = message.from_user
    admin_message = (
        f"Новый клиент! Позвоните, для потверждения заявки, на номер +996997777733! \n"
    )
    # await message.answer(ADMIN_CHAT_ID, admin_message)
    await bot_instance.send_message(ADMIN_CHAT_ID, admin_message)

    await state.clear()

    # Отправляем сообщение пользователю
    await message.answer(response_message)

    # Сбрасываем состояние FSM (если нужно начать новую заявку сразу)
    await state.finish()











