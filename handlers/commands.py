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
        [KeyboardButton(text="/add_client")],
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


ADMIN_CHAT_ID = ("5648090698")  # вставляете свой chat id
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
    await state.set_state(Form.experience)










    # Отправляем сообщение пользователю
    await message.answer(
        f"Заявка принята! \n"
        # f"ФИО: {data['name']}\n"
        # f"Номер телефона: {data['phone_number']}\n"
        # f"Chat_id: {data["chat_id"]}\n"
        # f"Опыт работы:{data["experience"]}"
    )



    # Отправляем сообщение администратору
    user = message.from_user
    admin_message = (
        f"Новый клиент! Позвоните, для потверждения заявки, на номер +996997777733! \n"
    )
    # await message.answer(ADMIN_CHAT_ID, admin_message)
    await bot_instance.send_message(ADMIN_CHAT_ID, admin_message)

    await state.clear()













from aiogram.types import Message,CallbackQuery,FSInputFile,ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class AddClientStates(StatesGroup):
    first_name = State()
    last_name = State()
    age = State()
    phone = State()
    chat_id = State()
    experience = State()



@router.message(Command("add_client"))
async def cmd_add_client(message:Message,state: FSMContext):
    await state.set_state(AddClientStates.first_name)
    await message.answer("Enter first_name:")
    

@router.message(AddClientStates.first_name)
async def process_first_name(message: Message, state: FSMContext) -> None:
    await state.update_data(first_name=message.text)
    await state.set_state(AddClientStates.last_name)
    await message.answer("Enter last_name:")


@router.message(AddClientStates.last_name)
async def process_last_name(message: Message, state: FSMContext) -> None:
    await state.update_data(last_name=message.text)
    await state.set_state(AddClientStates.age)
    await message.answer("Enter age:")


@router.message(AddClientStates.age)
async def process_age(message: Message, state: FSMContext) -> None:
    await state.update_data(age=message.text)
    await state.set_state(AddClientStates.phone)
    await message.answer("Enter phone:")

@router.message(AddClientStates.phone)
async def process_phone(message: Message, state: FSMContext) -> None:
    await state.update_data(phone=int(message.text))
    await state.set_state(AddClientStates.chat_id)
    await message.answer("Enter chat_id:")

@router.message(AddClientStates.chat_id)
async def process_chat_id(message: Message, state: FSMContext) -> None:
    await state.update_data(chat_id=message.text)
    await state.set_state(AddClientStates.experience)
    await message.answer("Enter experience:")

@router.message(AddClientStates.experience)
async def process_experience(message: Message, state: FSMContext) -> None:
    await state.update_data(experience=int(message.text))
    data = await state.get_data()
    await show_summary(message, data)
    await state.clear()

async def show_summary(message: Message, data: dict[str, any]):
    client = Client(first_name=data["first_name"],
            last_name=data["last_name"],
            age=data["age"],
            phone=data["phone"],
            chat_id=data["chat_id"], 
            experience=data["experience"])
    result = await create_client(client)
    await message.answer(text="Успешно добавили клиента!", reply_markup=ReplyKeyboardRemove())








from sqlalchemy import Integer,String,Text,DECIMAL,ForeignKey
from sqlalchemy.orm import (relationship,Mapped,mapped_column,
                            DeclarativeBase,Session)
from sqlalchemy.ext.asyncio import (create_async_engine,AsyncSession,
                                    async_sessionmaker,AsyncAttrs,
                                    AsyncEngine)

from config import MYSQL_URL

engine = create_async_engine(MYSQL_URL,echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase,AsyncAttrs):
    pass


class CLIENT(Base):
    __tablename__ = 'CLIENT'

    Id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    first_name:Mapped[str] = mapped_column(String(20))
    last_name:Mapped[str] = mapped_column(String(20))
    age:Mapped[int] = mapped_column(Integer)
    # phone:Mapped[int] = mapped_column(Integer(20))
    chat_id:Mapped[int] = mapped_column(Integer)
    experience:Mapped[int] = mapped_column(Integer)
    
    


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        
        async with async_session() as session:
            department = CLIENT(
                            Id = 1,
                            first_name = 'Ivan',
                            last_name = 'Ivamov',
                            age = 34,
                            phone = 1234567890,
                            chat_id = 5648090698,
                            experience = 6,
                            )
            session.add(department)
            await session.commit()



async def get_departments():
    async with async_session() as session:
        result = await session.scalars(select(CLIENT))
        return result


async def get_clients(department_id):
    async with async_session() as session:
        result = await session.scalars(select(CLIENT).where(
            CLIENT.department_id == department_id))
        return result


async def get_client(CLIENT_id):
    async with async_session() as session:
        result = await session.scalar(select(CLIENT).where(
            CLIENT.id == CLIENT_id))
        return result


async def get_client():
    async with async_session() as session:
        result = await session.scalars(select(CLIENT))
        return result
    

async def delete_client(rab_id):
    async with async_session() as session:
        await session.execute(delete(CLIENT).where(
            CLIENT.id == CLIENT_id))
        await session.commit()


async def create_CLIENT(rab):
    async with async_session() as session:
        
        session.add(rab)
        await session.commit()
        await session.refresh(rab)
        return rab
