from .asgacha import *
from hoshino import Service, R
from hoshino.typing import CQEvent
from PIL import Image
import base64
from io import BytesIO
import os


sv = Service('as抽卡', bundle='as', help_='''

'''.strip())

up_num = 1 #当前卡池为单up还是双up


def get_pic(pic_path):
    _path = 'C:\/Users/Administrator/Desktop/XCW/res/img/' + pic_path
    img = Image.open(_path)
    img = img.resize((80, 80), Image.ANTIALIAS)
    return img

@sv.on_rex((r'^as( )?(ur|UR|)( )?(一|1|单)(发|抽)'),only_to_me = True)
async def gacha_one(bot, ev):  #单抽
    match = ev['match']
    msg = ''
    if match.group(2) == '':   
        card_level = gacha_pt(up_num)
    else:
        card_level = gacha_pup(up_num)   #UR
    _path = random_give_card(card_level)
    base = Image.open('C:\/Users/Administrator/Desktop/XCW/res/img/image/frame.png')  #加载底图
    f = get_pic(_path)           #加载icon
    base.paste(f, (275,100))     #制图
    
    buf = BytesIO()
    base.save(buf, format='PNG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    await bot.send(ev, f'[CQ:image,file={base64_str}]')



@sv.on_rex((r'^(as)( )?(ur|UR|)( )?(十|10)(发|抽|连|连抽)'), only_to_me = True) 
async def gacha_ten(bot, ev):  #十连
    match = ev['match']
    msg = '十连结果为：'
    card_level = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if match.group(2) == '':
        for i in range(1,10):
            card_level[i] = gacha_pt(up_num)
        card_level[0] = gacha_bd(up_num)
    else:    #ur
        for i in range(0,10):
            card_level[i] = gacha_pup(up_num)
    
    base = Image.open('C:\/Users/Administrator/Desktop/XCW/res/img/image/frame.png')  #加载底图
    row_offset = 35    #制图参数
    index = 0          #制图参数

        
    for level in card_level:  #依次读取卡片稀有度
        _path = random_give_card(level)  #获取icon path
        row_index = index // 5           #制图参数
        col_index = index % 5            #制图参数
        f = get_pic(_path)               #加载icon
        base.paste(f, (95 + col_index * 80 + (col_index - 1) * 30,
                     row_offset + 40 + row_index * 80 + (row_index - 1) * 20))  #制图
        index += 1
        #msg += R.img(_path).cqcode  ####
    buf = BytesIO()
    base.save(buf, format='PNG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    await bot.send(ev, f'[CQ:image,file={base64_str}]')

@sv.on_rex((r'^as( )?(下|一|抽一)井'), only_to_me = True)     
async def gacha_jing(bot, ev):  #嫌慢？直接整一井！
    up = 0
    ur = 0
    sr = 0
    r = 0  #统计用

    temp = 0
    temp1 = 0
    temp2 = 0 #记录是否出up
    gacha_times = 0 #记录出up时抽了多少发十连
    msgg = ''
    
    base = Image.open('C:\/Users/Administrator/Desktop/XCW/res/img/image/frame.png')  #加载底图
    row_offset = 5   #制图参数
    index = 0        #制图参数
    
    
    for i in range(1,26):   #25发10连
        gacha_times += 1
        card_level = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for ii in range(1,10):   #单次十连计算
            card_level[ii] = gacha_pt(up_num)
        card_level[0] = gacha_bd(up_num)
        
        for level in card_level:  #获得对应卡牌
            _path = ''
            if level == 4:
                temp1 = 1
                up += 1
                ur += 1
            elif level == 5:
                temp2 = 1
                up += 1
                ur += 1
            elif level == 3:
                ur += 1
            elif level == 2:  #数量过多不显示具体sr
                sr += 1
            else:  #数量过多不显示具体r
                r += 1
                
            if level >= 3:
                _path = random_give_card(level)   #获取icon path
                row_index = index // 7            #制图参数
                col_index = index % 7             #制图参数
                f = get_pic(_path)                #加载icon
                base.paste(f, (35 + col_index * 80 + (col_index - 1) * 5,
                          row_offset + 40 + row_index * 80 + (row_index - 1) * 5))  #制图
                index += 1
                
        temp = temp1 + temp2
        if temp == up_num:  #出up抽齐自动结束本次抽卡
            msgg += f'up抽齐啦!已自动结束下井\n当前up卡为【綺麗に色づいてるね】松浦果南！\n共抽取{gacha_times}发十连，共计抽出{ur}张ur，{sr}张sr'
            break
    if up_num == 2:        
        if temp == 1: #单up的提示
            msgg += f'出up啦！共抽取{gacha_times}发十连，共计抽出{ur}张ur，{sr}张sr'
        elif temp == 0:   #井了的提示
            msgg += f'井啦！共抽取{gacha_times}发十连，共计抽出{ur}张ur，{sr}张sr'
    elif up_num == 1:
        if temp == 0:
            msgg += f'井啦！共抽取{gacha_times}发十连，共计抽出{ur}张ur，{sr}张sr'

    buf = BytesIO()
    base.save(buf, format='PNG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    msg = f'''{msgg}
[CQ:image,file={base64_str}]'''
    await bot.send(ev, msg)
        


