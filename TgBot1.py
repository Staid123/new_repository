from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Text, Command
from random import randint

API_TOKEN = '6206897348:AAENqclh-o1SObNCLJV69uJCTL5VUVOgjUc'

bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

user: dict = {}
ATTEMPTS: int = 7


def get_random_number() -> int:
    return randint(1, 100)

def new_user(message: Message):
    if message.from_user.id not in user:
        user[message.from_user.id] = {'in_game': False, 'secret_number': None, 'attempts': 0, 'total_games': 0, 'wins': 0}
    return True


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(f'Правила игры:'
                         f'Я загадываю число от 1 до 100.У вас будет {ATTEMPTS} попыток отгадать число, иначе вы проиграете\n'
                         'Если вы написали число меньше загаданого - то я напишу вам, что нужно число больше\n'
                         'Если вы написали число больше загаданого - то я напишу вам, что нужно число меньше\n'
                         'Во время игры я не понимаю ничего, кроме цифр от 1 до 100\n'
                         '/cancel - закончить игру\n'
                         '/stat - посмотреть свою статистику\n'
                         'Начнем играть?(Да/Нет)')


@dp.message(Command(commands=['start']))
async def process_start_game(message: Message):
    user_name = message.chat.first_name
    await message.answer(f'Привет {user_name}.Введите /help, чтобы узнать правила игры.')
    new_user(message)


@dp.message(Command(commands=['stat']))
async def proccess_stat_command(message: Message):
    if new_user(message):
        await message.answer('Ваша статистика:\n'
                            f"Сыграно игр: {user[message.from_user.id]['total_games']}, "
                            f"побед: {user[message.from_user.id]['wins']} раз(а)")


@dp.message(Command(commands=['cancel']))
async def cancel_command(message: Message):
    if new_user(message) and user[message.from_user.id]['in_game']:
        await message.answer('Вы вышли из игры. Если захотите сыграть '
                             'снова - напишите об этом')
    else:
        await message.answer('А мы итак с вами не играем. '
                             'Может, сыграем разок?')


@dp.message(Text(text=['Да', 'Давай', 'Сыграем', 'Игра',
                       'Играть', 'Хочу играть'], ignore_case=True))
async def game_started(message: Message):
    if new_user(message) and not user[message.from_user.id]['in_game']:
        user[message.from_user.id]['in_game'] = True
        user[message.from_user.id]['total_games'] += 1
        user[message.from_user.id]['secret_number'] = get_random_number()
        await message.answer('Число загадано!Попытайтесь его отгадать!')
    else:
        await message.answer('Пока мы играем в игру я могу '
                             'реагировать только на числа от 1 до 100 '
                             'и команды /cancel и /stat')


@dp.message(Text(text=['Нет', 'Не надо', 'Не хочу', 'Не буду']))
async def process_negative_answer(message: Message):
    if new_user(message) and not user[message.from_user.id]['in_game']:
        await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто '
                             'напишите об этом')
    else:
        await message.answer('Мы же сейчас с вами играем. Присылайте, '
                             'пожалуйста, числа от 1 до 100')


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_number_answer(message: Message):
    if not user[message.from_user.id]['in_game']:
        await message.answer('Мы еще не играем. Хотите сыграть?')
    else:
        user[message.from_user.id]['attempts'] += 1
        if int(message.text) == user[message.from_user.id]['secret_number']:
            user[message.from_user.id]['in_game'] = False
            user[message.from_user.id]['wins'] += 1
            user[message.from_user.id]['attempts'] = 0
            await message.answer('Ура!!! Вы угадали число!\n\n'
                                 'Может, сыграем еще?')
        elif user[message.from_user.id]['attempts'] == ATTEMPTS:
            user[message.from_user.id]['in_game'] = False
            user[message.from_user.id]['attempts'] = 0
            await message.answer('К сожалению вы проиграли :('
                                 f'Загаданое число было {user[message.from_user.id]["secret_number"]} '
                                 'Если хотите сыграть еще - введите /start, если нет - /cancel')
        elif int(message.text) > user[message.from_user.id]['secret_number']:
            await message.answer('Ваше ввёденное число больше загаданого\n'
                                 'Попробуйте еще раз!')
        elif int(message.text) < user[message.from_user.id]['secret_number']:
            await message.answer('Ваше ввёденное число меньше загаданого\n'
                                 'Попробуйте еще раз!')


@dp.message()
async def other_text_answers(message: Message):
    if new_user(message) and user[message.from_user.id]['in_game']:
        await message.answer('Мы же сейчас с вами играем. '
                             'Присылайте, пожалуйста, числа от 1 до 100')
    else:
        await message.answer('Я довольно ограниченный бот, давайте '
                             'просто сыграем в игру?')


if __name__ == '__main__':
    dp.run_polling(bot)
