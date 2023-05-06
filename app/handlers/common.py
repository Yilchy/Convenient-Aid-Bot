from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from . import location_state


STARTING_MESSAGE = "You are using the bot which helps to find the most fitting points of providing humanitarian \
aid, type \"/update_personal\" to configure your personal data and to start to recieve messages of polling"


async def cmd_start(message: types.Message, state: FSMContext):
    if(await state.get_state() == await location_state.SendLocation.first()):
        await state.finish()
        await message.answer(STARTING_MESSAGE,
            reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        return


async def cmd_cancel(message: types.Message, state: FSMContext):
    if(await state.get_state() != location_state.StarterInitialize.waiting_for_starter_location):
        await state.set_state(await location_state.SendLocation.last())
    else:
        await state.finish()
    await message.answer("Actions stopped", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")