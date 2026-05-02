import asyncio
import random
import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError, SessionPasswordNeededError

# --- КОНФИГУРАЦИЯ ---
BOT_TOKEN = 'ТВОЙ_ТОКЕН_ОТ_BOTFATHER'

# Список всех фраз (полный набор)
phrases = [
    "ты пидор ебаный нахуй", "я те мать еба шлн вахуй", "я отвожюб маоть пер нахуй",
    "ты пидро кебавнный нищий", "я тво.юмать ебалн ахуй", "ты гей ебанынй чмо нахзуй",
    "ты ебанынй нищий", "ты пидроь ебваанный уцптйон ахуй", "я твшолю мать пидоаврсли",
    "ты хузесос сранный", "чмошинк енахуй ебанынй изхчпкованный", "я втою мать пок олцькук нахуй трахал",
    "очко ебаннеле нахуй ты егй ебаный смлабячй", "ьты нищий пдиор я тувою мать изьебал",
    "тсарнынй егй нахукй закрйо ебало", "т ы нахуй пошел отсюда", "сперма моя нахуй оты ебеанная",
    "я товою матье балн ахуй", "ты придор ебанынй", "хуеосс сраныйн уптйон ахуй",
    "оты пидор ипачканнфый енбаный", "тупой нвахуй негр яблскдий черный", "твою. маитьт поебалн азхуй на найс",
    "ты пидор запомнеи я итеа мть ебал нахуй", "ты шлюахе бананя", "утенок енбанныйн нахуй я твою мать пиздил",
    "ща закрйол ебало нахуй свое", "ты прдиор ебаныянй чыерный", "тво юм ать ебалн ахуй",
    "ты е7й ебаныфй нищипй", "червяк сук анхзвауйц ебанный", "тупой ябслкдйи ишак",
    "ебанынй свельский пдиор", "акзвали ебало щас", "ты пидро ебло вальни нахуй",
    "ублюдолк ебанный", "пер те мать енхауй", "ты поянл меня нхауй ты ппес ебанный",
    "нищий бялдлский помойный нсхуй старнник", "ебало закрйо нвахъуй", "тыпидор ебаныйн очдичалый",
    "ебаныйн сранынй пидорас", "окей нахуй я те амтьб ебал нахуй", "тыв егй ебаныйн тупой",
    "голубой ухевосс нахуй", "песик ебснывнй ебало зщавали", "щенок бяслкдйи ебло вальни нхауй",
    "ты пдорр ебанынй измучаю етяб сука", "ты егйе бваныенй нахуй без пр4киоалов",
    "я твою мать ебаную нахзуй ебал", "ты сын бялди ебаныйн птйоон аху", "ты егй ебанный есранный",
    "ты нищйий харек блясдкеий", "помоыйн сын бялид", "сын шьбюзи зареванный",
    "изрезанный пидорас н ахуй", "истрезанная шавлаа нахуй", "те мать ебаолн ахуй",
    "ты дипор ебанынй уптой", "я твою мать ебалн ахуй", "ты егй ебанынй деревенский",
    "ебьаны6нйу прйон ахуй ог8ородник", "бяолскдий нахуй нищак", "беавнынй уптоурп йнхауй гей",
    "я тво ю апмть ебал нахуй забапвный уролд", "печашльн ый пдиор нпахзууй не з-лись",
    "я ет мать ебалн хуй парпуц раз", "ты егекй ебанный кптой нхауй", "избитый куоклд",
    "я твою маить уебал нахуй", "куоклд ебаыннй уптйо неахйу соси", "ты пдиор ебаын птуцопй нхауй т егей",
    "я оте амть ебал нgaхуй голубенкий фрик", "ты че навхуй черножопыйпидро", "ты егй небаныйн пробитый",
    "кукурузнник ебаныйн уптйо нахйу закрйо ебало", "я те мать ебал нахуй", "пидор", "ебал те мать",
    "сын шлюхи", "твою мать пиздил", "ты хуеосс нахуй", "твобю маоть ебал нахуй членом резиновым",
    "ты егй ебюаеныей упйо нахуй азкрйо еблак", "твоей матери на литцо насру", "зещеканц ебанынй уптуцой нхауй",
    "щенок а нгу втопи ебалот 0зас нахуй", "негр беанынй нрахуй", "ты ебало зававли щаас гей ебаныйну птйо",
    "ты мерзость ебананя", "терпли а нахуй ты", "твою матьб ебал красный пжитдро напхкйц",
    "не потей пдиора с я те все равнол матьб ебал", "ты напхуй джон ебапнынй упй", "гей нхауц йебанный",
    "Я ТЕ АМТЬЕ БАЛН АЗХЦУЙ ЫТ ПИДОР УТЕПОЙ", "ТЫ АМЕБКА ЕБАНАНЯ НХЪАЙУ ТЫ ЕТКЛА",
    "ТЫ ДАРШЕК НАЗУЙ ЕБАНЫНЙЦ УПТЦЙО", "я ета мтть ебалн ахы йцтцп пидро", "утпому пдтотру нахуй по ебалу дали",
    "ВАЯЛЕ АБАНЯН НАХУЙ РОТ ЗАКРЙО", "ты пидотр нбканынй я те мать поебалн авхуй", "я тя в жолп у пер нахуй",
    "тыв пидроь ебваыннй узкоглазхячый", "ты че н итут нахуй щекастый п идорн апзуй",
    "я те по обе щеки нхауй спермой залил", "ты мер4кая нахуй телка ебанная", "я твою мать ебал",
    "ты гей нахъуй ебаныйн уптйо", "твоя мать шлюха уттч елнвы сосет нахуй", "ты че утпйо бялсдкий помойный бомд",
    "бичукган ебанный уптйо природный", "ты геяка нхайу твоя мать сосала член", "ты пидрон ахуй ебаный у птйо измученый",
    "ты шалваьнахуй еьбананя тварь", "я твою мать ебалн ахйу", "завалавьи ебюанг6нлон еaхуй ты мкерзавец ебаны6нй",
    "тоупй нахуй не ной", "ты шлах ебананя цыганка", "я  твою матьебашил нахуй", "ты пмионля меня гнахйу тьы олеьн ебанынй",
    "ты утпрой гнилой нахуй хач", "ты епидргоас изьеабывйнн", "ты пдиор нхауй прирожденный",
    "енбали твою матль нахуй ты пидор", "закрой ебалот говноедн ахуй", "ты калловый сын шлюхзи нахуй а ну втапи ебало",
    "обама нгебюанынцй авзали ебалон казуй", "я тек ат ьтуту пмер сперма нахуй емоя", "ты сперма моя тупой ты дикарь",
    "твяома тть нахуй состе члены тут", "ты че защеканец ебснны упйон аухй", "ты избитый ппидорас",
    "изнасилованная нахуй шлюха чатн7ая", "я те мать убью назхуй ты егй ебанный", "ты укптоцй пидонрас спермцу жэуйб мою нахуй",
    "ты че гея ка ебанный проибтый", "я тво ю мать убью нахуй щас", "я тебе членом по лбу стуцчалн ахуй",
    "ты ебанный никто сука", "я те мать удтил нахуй тупой ты сукин сын", "ты трупная шлюжа ебанная",
    "я твоей матери череп лотмал нахуй ты утпой гей", "ебал те мать тупой сранный неджотайпер",
    "че ты оьбезяьан ебспнаня нахцуй", "ты че гроищшь нахуй сывнок шлюхи", "потлетарный пидорас я те мать убюь. юнахуй",
    "школьниек кебанныяй я твою мать тут потрахал", "ты не обизжайся нахуй гей ебанный", "я те мать убил сегодня",
    "тыч ен нваыхзкйу путана ебаннкая", "геяка сука засранная", "анука нхсвуй пдии отсюада",
    "я те мат ье ьбалн ахуй тут ты пидро", "повстане цбеанный нхауй ро такзрйо", "ты пидор ебанынй сранный",
    "ты че нахуй ппедик енбанный", "тупой навйхц ыт сраныйн говнбюк", "я твою маить пер назхйу тут",
    "ты сын шлюхи победимыф", "ты слабы нхауй ишук", "я тебя убь юнахуй", "тупой счынок шлюхи а ну ебало закрйор",
    "ты чето сыноко бляди ебанный", "ты утпой гей нахуй", "ты сранный нищак", "обнищалый придро пиздец",
    "я те мать ебалн ахуй", "ты тупой пдигор", "ебанный ты скот", "я те мать еблн хуй ты скотина",
    "ебаняч6нй уптой нахуй ты мерзавец", "я т вроюб мать дурун ахуй кнебал", "ты уцтпой пидор",
    "балбес бялсдкий", "ебанный уптойц нахуй ты пидор", "голопжэый пидор", "ты акзрйо ебалотнахуй",
    "втопи ебало свое", "ты пидор ебанынй безджзенный", "ты тупой пидорас а ну мочли нхавйу",
    "ты гей ебанынй уптйо нахйу", "я те мкаить перс нахпуй", "ты ктууопй ты гей ебаный", "ты слабак нахуй",
    "зхкрой ебашло лучше", "сыннок шлюхи истерзанный", "ты че такой утпой тот напхуй", "ть че сосеш нахуй ывсегда",
    "ты че тутноешь нахуй", "ты че слабая нахуй тут телка", "те че мебало сломатьн ахуй",
    "итсерзанный туопйц сынок бляди", "ебанный повстанец", "закрйо ебало нахуй", "тупрой ебанный евнух нахуй",
    "я те мать ебал ослеоб", "ебучий пастух", "ты нимткон ахуй", "еббанный цутпой пидро без фейма",
    "я те матье ебалн хуй", "ты скот бялскдий", "ебанный старый пидро", "я те мать убью нахуй",
    "дохлый ты пидор нахуй", "паолумертвый пидорас", "ты че нахуй ебанный трупной ты пидро",
    "я те мкать буьбюю напхуй", "ты тупой пидор", "ьвоя мать неахуй дуар ебананя", "я твою мать убью напхуй",
    "ты сукот еюанный sрианный", "ты че нахуй ноешь", "ты че такой гей ебанный", "ты че сранный пидор нахуй ебанныцй",
    "я непобедим", "тьы член сосшеь нахуй", "закрйо ебало щас свое", "ты слабый нахуй тупой ебанный ишак",
    "завиле белаон ахуй свое", " ятвою матьн ахуй просто на члене ебал", "твоя мать клитором языки все принимает и чолены",
    "твоя маитьн хуй скотина потраханная", "ты и изасиллованный ебанный петушок", "ты тутп нахуй ебалот втопи",
    "че умер нахуй)", "ты пидор ебанный утпцой)", "я те матб ебалдн ахуй уттр)", "ты пидор ебанныйф протраханный)",
    "ты че умер нахй ебанный идиот))", "сынок шллюхи ебанынй упй нахуй", "ты че тут  джохнгешщь ебанный стадник",
    "тебя убью нахуй", "ты пиджолр ебанын на рромансе", "я тебя зарежу нахуй тут", "я тебюя убьюн апхуй ты утпой ебанный",
    "тя ядоувитый сынок бюляди", "я тебе мат ьебалн ахуй слабак", "ебанынй уптйон ахъуй ты че попутал",
    "я те мать убюью нахуй ты слабы пидор", "сынок шлбжэихи ебанный", "пидор патифон ебангынйц уптйо нахуй",
    "я тек мать ебал сукин сын бялсдкий", "помойнывй ты пидор нахуй", "тьы ебавнная слдабачка", 
    "ты гондон ебанный прокаженный", "я те щас ебало нахуй разнесу", "ты пидор конченый безмозглый",
    "твою мать в рот ебал нахуй", "тв чк там сын хуйни", "твою мать потаскуху ебаь", "ты че жирныц сын хуйни соси мне там"
]

# Хранилище сессий и состояний
user_clients = {} # {user_id: client}
user_tasks = {}   # {user_id: task}
calendar_targets = {} # {user_id: target_id}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class AuthStates(StatesGroup):
    waiting_for_api_id = State()
    waiting_for_api_hash = State()
    waiting_for_phone = State()
    waiting_for_code = State()

# --- КЛАВИАТУРЫ ---
def get_main_kb():
    kb = [
        [types.KeyboardButton(text="🔐 Авторизация")],
        [types.KeyboardButton(text="🚀 Спам"), types.KeyboardButton(text="📅 Calendar")],
        [types.KeyboardButton(text="🛑 Остановить всё")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# --- ЛОГИКА АВТОРИЗАЦИИ ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Управление мульти-аккаунт спамером.\nНажми 'Авторизация'.", reply_markup=get_main_kb())

@dp.message(lambda m: m.text == "🔐 Авторизация")
async def auth_start(message: types.Message, state: FSMContext):
    await message.answer("Введите ваш API ID:")
    await state.set_state(AuthStates.waiting_for_api_id)

@dp.message(AuthStates.waiting_for_api_id)
async def process_api_id(message: types.Message, state: FSMContext):
    await state.update_data(api_id=message.text)
    await message.answer("Введите ваш API HASH:")
    await state.set_state(AuthStates.waiting_for_api_hash)

@dp.message(AuthStates.waiting_for_api_hash)
async def process_api_hash(message: types.Message, state: FSMContext):
    await state.update_data(api_hash=message.text)
    await message.answer("Введите ваш номер телефона (с +):")
    await state.set_state(AuthStates.waiting_for_phone)

@dp.message(AuthStates.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone = message.text
    session_path = f"sessions/user_{message.from_user.id}"
    
    client = TelegramClient(session_path, data['api_id'], data['api_hash'])
    await client.connect()
    
    try:
        sent_code = await client.send_code_request(phone)
        await state.update_data(client=client, phone=phone, hash=sent_code.phone_code_hash)
        await message.answer("Код отправлен! Введите его в чат:")
        await state.set_state(AuthStates.waiting_for_code)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")
        await state.clear()

@dp.message(AuthStates.waiting_for_code)
async def process_code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    client = data['client']
    try:
        await client.sign_in(data['phone'], message.text, phone_code_hash=data['hash'])
        user_clients[message.from_user.id] = client
        
        # Регистрация обработчика Calendar для этого клиента
        @client.on(events.NewMessage)
        async def calendar_handler(event):
            u_id = message.from_user.id
            if u_id in calendar_targets and event.sender_id == calendar_targets[u_id]:
                await event.reply(random.choice(phrases))
        
        await message.answer("✅ Успешно! Теперь выбери режим.")
        await state.clear()
    except Exception as e:
        await message.answer(f"Ошибка кода: {e}")

# --- УПРАВЛЕНИЕ ---
@dp.message(lambda m: m.text == "🚀 Спам")
async def spam_req(message: types.Message):
    if message.from_user.id not in user_clients:
        return await message.answer("Сначала авторизуйся!")
    await message.answer("Пришли @username или ID чата для спама:")

@dp.message(lambda m: m.text == "📅 Calendar")
async def cal_req(message: types.Message):
    if message.from_user.id not in user_clients:
        return await message.answer("Сначала авторизуйся!")
    await message.answer("Пришли ID жертвы для автоответа:")

async def spam_worker(user_id, target):
    client = user_clients[user_id]
    while True:
        try:
            await client.send_message(target, random.choice(phrases))
            await asyncio.sleep(0.7)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except Exception:
            break

@dp.message(lambda m: m.text == "🛑 Остановить всё")
async def stop_all(message: types.Message):
    u_id = message.from_user.id
    if u_id in user_tasks:
        user_tasks[u_id].cancel()
        del user_tasks[u_id]
    if u_id in calendar_targets:
        del calendar_targets[u_id]
    await message.answer("Все твои процессы остановлены.")

@dp.message()
async def global_handler(message: types.Message):
    u_id = message.from_user.id
    if u_id not in user_clients: return
    
    text = message.text
    if text.startswith('-100') or text.startswith('@') or text.isdigit():
        # Если была нажата кнопка Calendar
        if u_id not in user_tasks:
            try:
                target = int(text) if text.isdigit() else (await user_clients[u_id].get_entity(text)).id
                calendar_targets[u_id] = target
                await message.answer(f"✅ Режим Calendar включен на {target}")
            except:
                # Если не календарь, значит спам
                user_tasks[u_id] = asyncio.create_task(spam_worker(u_id, text))
                await message.answer(f"🚀 Спам запущен в {text}")

async def main():
    if not os.path.exists('sessions'): os.makedirs('sessions')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
