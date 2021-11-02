'''
# @Author       : Chr_
# @Date         : 2021-11-02 12:07:14
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-02 13:23:16
# @Description  : 静态帮助文本
'''

from config import VERSION, BOT_NICK

__NORMAL = '\n\n'.join([
    '/start',
    '/help',
    '/myinfo'
])

__ADMIN = '\n\n'.join([
    '/top',
])

__SUPER = '\n\n'.join([
    '/reload',
])

CMD_HELP = {
    'NULL': '无可奉告',
    'NORMAL': __NORMAL,
    'ADMIN': f'{__NORMAL}\n\n{__ADMIN}',
    'SUPER': f'{__NORMAL}\n\n{__ADMIN}\n\n{__SUPER}',
}

BOT_MSG = f'''
{BOT_NICK} @{VERSION}
'''

VER_MSG = f'''
*{BOT_NICK}* Ver `{VERSION}` ©2021
'''.strip()
