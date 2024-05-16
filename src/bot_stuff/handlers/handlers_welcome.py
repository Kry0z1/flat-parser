from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot_stuff.adapter import Adapter

router = Router()
adapter = Adapter()
params_dict = dict()
loaded_data = dict()


def get_param_string_repr(param, param_value):
    if param == "sort_type":
        return f"Sort type: {'by price' if param_value == 'price' else 'by date added'}"
    if param == "rooms":
        return_value = f"Number of rooms allowed: {param_value[0]}"
        for room in param_value[1:]:
            return_value += f", {room}"
        return return_value
    if param == "chosen":
        return f"Website chosen: {param_value}"


@router.message
async def unknown_input(message: types.Message):
    await message.answer("Did not quite understood your command.")


@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(adapter.get_start_message())


@router.message(Command("params"))
async def print_params(message: types.Message, user_id=None):
    if user_id is None:
        user_id = message.from_user.id
    if user_id not in params_dict.keys():
        params_dict[user_id] = {"sort_type": "price", "rooms": [1, 2], "chosen": adapter.names[0]}
    answer, markup = get_params_changer(user_id)
    await message.answer(answer, reply_markup=markup)


def get_params_changer(id):
    params = params_dict[id]
    builder = InlineKeyboardBuilder()
    result_answer = ""
    for index, param in enumerate(params.keys()):
        result_answer += f"{index + 1}) {get_param_string_repr(param, params[param])}\n"
        builder.row(types.InlineKeyboardButton(
            text=f"Change parameter {index + 1}",
            callback_data=f"ask-to-change-param-{param}-{id}",
        ))
    builder.row(types.InlineKeyboardButton(
        text=f"Proceed",
        callback_data=f"log_websites-{id}",
    ))

    return result_answer, builder.as_markup()


@router.callback_query(F.data.startswith("show_website"))
async def show_website(callback: types.CallbackQuery, id=None):
    if id is None:
        id = int(callback.data.split("-")[2])
        page = int(callback.data.split("-")[1])
    else:
        page = 0
    if id not in loaded_data.keys():
        await callback.message.answer("Your data is not loaded. Type '/load'")
        return
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text=f"Show next",
        callback_data=f"show_website-{page+1}-{id}"
    ))

    data = loaded_data[id][page]
    await callback.message.answer(f"Link: {data.link}\n"
                                  f"Price: {data.price}\n"
                                  f"Price info: {data.price_info}\n"
                                  f"Nearest station: {data.metro}\n"
                                  f"Address: {data.street}\n"
                                  f"Description: {data.description}",
                                  reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("log_websites"))
@router.callback_query(Command("load"))
async def log_websites(callback: types.CallbackQuery):
    user_id = int(callback.data.split("-")[1])
    loaded_data[user_id] = adapter.load(params_dict[user_id])
    await show_website(callback, user_id)
