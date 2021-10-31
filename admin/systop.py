'''
# @Author       : Chr_
# @Date         : 2021-10-29 19:37:48
# @LastEditors  : Chr_
# @LastEditTime : 2021-10-31 15:42:24
# @Description  : 服务器监控
'''

from os import path
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from datetime import datetime
from platform import uname
from typing import Tuple
from aiogram.types.message import Message
from distro import linux_distribution
from psutil import boot_time, getloadavg, net_io_counters
from psutil import cpu_count, cpu_freq, cpu_percent
from psutil import virtual_memory, disk_usage, disk_partitions

FONT_PATH = path.join('res', 'sarasa-mono-sc-semibold.ttf')


async def cmd_systop(message: Message):
    f = draw_usage_data(get_system_data(), get_usage_data())

    await message.reply_photo(photo=f, caption='系统状态')


def size2str(size: int) -> str:
    '''
    将字节转换成合适的单位

    参数:
        字节数
    返回:
        形如 1.0KB 的格式
    '''
    def sos(integer: int, remainder: int, level: int) -> Tuple[int, int, int]:
        if integer >= 1024:
            remainder = integer % 1024
            integer //= 1024
            level += 1
            return sos(integer, remainder, level)
        else:
            return integer, remainder, level
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']
    integer, remainder, level = sos(size, 0, 0)
    if level+1 > len(units):
        level = -1
    return (f'{integer}.{str(remainder)[:2]}{units[level]}')


def get_system_data() -> list:
    '''
    获取系统数据

    返回:
        list: 报表数据, 每个元代表一行
    '''
    result = []

    u = uname()
    sys_type = u.system
    if sys_type == 'Linux':
        os_name, os_version, _ = linux_distribution(True)
        result.append(('操作系统', f'{os_name} {os_version}'))
    else:
        result.append(('操作系统', f'{u.system} {u.version}'))
    time_pass = datetime.now() - datetime.fromtimestamp(boot_time())
    result.append(
        ('运行时间', f'{time_pass.days} 天 '
         f'{int(time_pass.seconds/3600)} 时 {int(time_pass.seconds%3600/60)} 分'))
    m1, m5, m15 = getloadavg()
    c_count = cpu_count(logical=True)
    if c_count > 1:
        m1 = round(m1 / c_count, 2)
        m5 = round(m5 / c_count, 2)
        m15 = round(m15 / c_count, 2)
    s = f'{m1} / {m5} / {m15}'
    if (m1 > 1 or m5 > 1 or m15 > 1):
        s += ' [!]'
    result.append(('负载情况', s))
    n = net_io_counters()
    n_sent = size2str(n.bytes_sent)
    n_recv = size2str(n.bytes_recv)
    result.append(('网络流量', f'↑{n_sent} / ↓{n_recv}'))
    return result


def get_usage_data() -> list:
    '''
    获取系统数据

    返回:
        list: 报表数据, 每个元素 (标题左侧,标题右侧,百分比)
    '''
    result = []
    c_freq = round(cpu_freq().current / 1000, 2)
    c_percent = cpu_percent()
    c_core = cpu_count(logical=False)
    c_trade = cpu_count(logical=True)
    s_percent = str(c_percent).rjust(4)
    result.append(
        ('CPU用量', f'{c_freq}GHz / {c_core}C{c_trade}T [{s_percent}%]', c_percent))
    m = virtual_memory()
    m_percent = m.percent
    m_total = size2str(m.total)
    m_used = size2str(m.used)
    s_percent = str(m_percent).rjust(4)
    result.append(
        ('内存用量', f'{m_used} / {m_total} [{s_percent}%]', m_percent))
    for d in disk_partitions():
        d_mount = d.mountpoint
        if d.fstype:
            u = disk_usage(d_mount)
            d_percent = u.percent
            d_total = size2str(u.total)
            d_used = size2str(u.used)
        else:
            d_percent = 0.0
            d_total = '-'
            d_used = '-'
        s_percent = str(d_percent).rjust(4)
        result.append(
            (f'磁盘用量 {d_mount}', f'{d_used} / {d_total} [{s_percent}%]', d_percent))
    return result


def draw_usage_data(sysdata: list, usage: list) -> BytesIO:
    '''
    把系统数据绘成图片

    参数:
        data: get_dashboard_data的返回值
    返回:
        str: 图片路径
    '''
    # ================================
    BOARD = 5                    # 图片边框
    WIDTH = 280                  # 条目宽度
    ITEM_HEIGHT = 20             # 条目高度
    FONT_SIZE = 12               # 字体大小
    BG_COLOR = '#FFFFFF'         # 背景颜色
    BD_COLOR = '#EEEEEE'         # 边框颜色
    FT_COLOR = '#333333'         # 字体颜色
    BAR_LOW_COLOR = '#00a94e'    # 进度条颜色[0~50%]
    BAR_MID_COLOR = '#00a5ba'    # 进度条颜色[51~75%]
    BAR_HIGH_COLOR = '#ffbe00'   # 进度条颜色[76~90%]
    BAR_FULL_COLOR = '#f41b35'   # 进度条颜色[91~100%]
    # ===============================
    font = ImageFont.truetype(font=FONT_PATH, size=FONT_SIZE)
    width = WIDTH + 2*BOARD
    height = (len(sysdata)+len(usage)*2) * ITEM_HEIGHT + 2*BOARD
    img = Image.new('RGB', (width, height), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    # 外框
    draw.rectangle((BOARD, BOARD, width-BOARD, height-BOARD),
                   outline=BD_COLOR)
    flag = True
    current_y = BOARD
    for a, b in sysdata:
        x = BOARD
        y = current_y
        # 文字栏
        text_w, font_h = font.getsize(b)
        text_h = font_h+6
        if (flag):
            draw.rectangle((x, y, x+WIDTH-1,  y+text_h), fill=BD_COLOR)
        flag = not flag
        x += 5
        y += 3
        draw.text((x, y), a, fill=FT_COLOR, font=font)
        x = WIDTH - text_w - 5
        draw.text((x, y), b, fill=FT_COLOR, font=font)
        current_y += ITEM_HEIGHT

    for a, b, c in usage:
        x = BOARD
        y = current_y
        # 文字栏
        text_w, font_h = font.getsize(b)
        text_h = font_h+6
        draw.rectangle((x, y, x+WIDTH-1,  y+text_h), fill=BD_COLOR)
        x += 5
        y += 3
        draw.text((x, y), a, fill=FT_COLOR, font=font)
        x = WIDTH - text_w - 5
        draw.text((x, y), b, fill=FT_COLOR, font=font)
        # 进度条
        x = BOARD + 5
        y = current_y + text_h + 5
        bar_w = WIDTH - 10
        bar_h = ITEM_HEIGHT - 10
        draw.rectangle((x, y, x+bar_w-1,  y+bar_h), fill=FT_COLOR)
        draw.rectangle((x+1, y, x+bar_w-2,  y+bar_h-1), fill=BG_COLOR)
        if c < 50:
            color = BAR_LOW_COLOR
        elif c < 75:
            color = BAR_MID_COLOR
        elif c < 90:
            color = BAR_HIGH_COLOR
        else:
            color = BAR_FULL_COLOR
        bar_w = (bar_w-2) * c // 100
        bar_h -= 1
        if bar_w:
            draw.rectangle((x+1, y, x+bar_w,  y+bar_h), fill=color)
        current_y += ITEM_HEIGHT * 2

    f = BytesIO()
    img.save(f, 'PNG')
    f.seek(0)
    return f
