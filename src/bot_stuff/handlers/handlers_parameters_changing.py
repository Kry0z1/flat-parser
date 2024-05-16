from aiogram import F, types, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot_stuff.handlers import handlers_welcome
from src.bot_stuff.handlers.handlers_welcome import get_param_string_repr, print_params

router = Router()
params_dict = handlers_welcome.params_dict
adapter = handlers_welcome.adapter


@router.callback_query(F.data.startswith("ask-to-change-param-"))
async def callback_parameter_changing(callback: types.CallbackQuery):
    to_change = callback.data.split("-")[-2]
    user_id = callback.data.split("-")[-1]
    builder = InlineKeyboardBuilder()
    if to_change == "sort_type":
        builder.row(types.InlineKeyboardButton(
            text="Sort by price",
            callback_data=f"change-param-sort_type-price-{user_id}"
        ))
        builder.row(types.InlineKeyboardButton(
            text="Sort by date added",
            callback_data=f"change-param-sort_type-date-{user_id}"
        ))
    elif to_change == "rooms":
        for room in range(1, 5):
            builder.row(types.InlineKeyboardButton(
                text=f"Include(exclude) {room}",
                callback_data=f"change-param-rooms-{room}-{user_id}"
            ))
    elif to_change == "chosen":
        for site in adapter.names:
            builder.row(types.InlineKeyboardButton(
                text=f"Choose {site}",
                callback_data=f"change-param-chosen-{site}-{user_id}"
            ))
    await callback.message.answer(
        get_param_string_repr(to_change, params_dict[callback.from_user.id][to_change]),
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data.startswith("change-param"))
async def change_param(callback: types.CallbackQuery):
    to_change = callback.data.split("-")[2]
    change_value = callback.data.split("-")[3]
    user_id = int(callback.data.split("-")[-1])
    if to_change in "sort_type, chosen":
        params_dict[user_id][to_change] = change_value
    if to_change == "rooms":
        if int(change_value) in params_dict[user_id][to_change]:
            params_dict[user_id][to_change].remove(int(change_value))
        else:
            params_dict[user_id][to_change].append(int(change_value))
            params_dict[user_id][to_change].sort()
    await callback.answer("Changed successfully")
    await print_params(callback.message, user_id)
