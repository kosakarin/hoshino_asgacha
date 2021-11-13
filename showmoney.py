import base64, os, random
from hoshino.image import *
from hoshino.money import *
import hoshino
from hoshino import Service
from hoshino.typing import CQEvent
from PIL import Image


sv = Service('查看财富', bundle='seemoney', help_='''使用如下命令进行查看：
我的钱包
'''.strip())


@sv.on_rex(('qianbao帮助'))
async def money_help(bot, ev):
    await bot.send(ev, f'[CQ:image,file=base64://{image_to_base64(text_to_image(sv.help.strip())).decode()}]')
    
@sv.on_fullmatch('我的钱包')
async def money_get(bot, ev):
    uid = ev['user_id']
    key_list = ["gold", "lovecastone", "starstone", "kirastone"]
    msg = ''
    for key in key_list:
        msg += f'\n{key} = {get_user_money(uid, key)}'

    await bot.send(ev, msg, at_sender = True)

