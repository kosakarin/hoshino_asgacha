#import base64, os, random ##不是 我当初写这里的时候怎么会import这些东西 没必要啊
#from .image import *    #不是 我当初写这里的时候怎么会import这东西 没必要啊
from .money import *
import hoshino
from hoshino import Service
from hoshino.typing import CQEvent
#from PIL import Image    #不是 我当初写这里的时候怎么会import这东西 没必要啊

#其实我感觉这个可以直接合到别的文件里面（超小声） 属于是写的时候脑抽了
sv = Service('查看财富', bundle='seemoney', help_='''

'''.strip())


    
@sv.on_fullmatch('我的钱包')
async def money_get(bot, ev):
    uid = ev['user_id']
    key_list = ["gold", "lovecastone", "starstone", "kirastone"]
    msg = ''
    for key in key_list:
        msg += f'\n{key} = {get_user_money(uid, key)}'

    await bot.send(ev, msg, at_sender = True)

