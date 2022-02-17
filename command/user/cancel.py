'''
# @Author       : Chr_
# @Date         : 2022-02-17 09:38:50
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-17 09:53:19
# @Description  : 
'''

from loguru import logger
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.storage import FSMContext


async def handle_cancel(message: Message, state: FSMContext):

    current_state = await state.get_state()
    if not current_state:
        await message.reply('操作已取消', reply_markup=ReplyKeyboardRemove())
        return

    logger.info(f'当前状态: {current_state}')
    
    await state.finish()

    await message.reply('操作已取消', reply_markup=ReplyKeyboardRemove())
