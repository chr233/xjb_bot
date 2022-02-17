'''
# @Author       : Chr_
# @Date         : 2022-02-17 09:57:22
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-17 09:57:23
# @Description  : 自定义拒稿原因
'''

from aiogram.dispatcher.filters.state import State, StatesGroup


class RejectForm(StatesGroup):
    reason = State()
