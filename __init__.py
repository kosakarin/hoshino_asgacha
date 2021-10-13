from .asgacha import *
from hoshino import Service, R
from hoshino.typing import CQEvent
from PIL import Image
import base64
from io import BytesIO
import os


sv = Service('as抽卡', bundle='as', help_='''

'''.strip())

def get_pic(pic_path):
    _path = 'C:\/Users/Administrator/Desktop/XCW/res/img/' + pic_path
    img = Image.open(_path)
    img = img.resize((80, 80), Image.ANTIALIAS)
    return img

@sv.on_rex((r'^as( )?(一|1|单)(发|抽)'),only_to_me = True)
async def gacha_one(bot, ev):  #单抽
    msg = ''
    card_level = gacha_pt()
    _path = random_give_card(card_level)
    base = Image.open('C:\/Users/Administrator/Desktop/XCW/res/img/image/frame.png')
    f = get_pic(_path)
    base.paste(f, (275,
                 100))
    
    buf = BytesIO()
    base.save(buf, format='PNG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    await bot.send(ev, f'[CQ:image,file={base64_str}]')



@sv.on_rex((r'^as( )?(十|10)(发|抽|连|连抽)'), only_to_me = True) 
async def gacha_ten(bot, ev):  #十连

    msg = '十连结果为：'
    card_level = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(1,10):
        card_level[i] = gacha_pt()
    card_level[0] = gacha_bd()
    
    base = Image.open('C:\/Users/Administrator/Desktop/XCW/res/img/image/frame.png')
    row_offset = 35
    index = 0
    
    for level in card_level:
        _path = random_give_card(level)
        row_index = index // 5
        col_index = index % 5
        f = get_pic(_path)
        base.paste(f, (95 + col_index * 80 + (col_index - 1) * 30,
                     row_offset + 40 + row_index * 80 + (row_index - 1) * 20))
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
    
    base = Image.open('C:\/Users/Administrator/Desktop/XCW/res/img/image/frame.png')
    row_offset = 5
    index = 0
    
    
    for i in range(1,26):   #25发10连
        gacha_times += 1
        card_level = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for ii in range(1,10):   #单次十连计算
            card_level[ii] = gacha_pt()
        card_level[0] = gacha_bd()
        
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
                _path = random_give_card(level)
                row_index = index // 7 
                col_index = index % 7
                f = get_pic(_path)
                base.paste(f, (35 + col_index * 80 + (col_index - 1) * 5,
                          row_offset + 40 + row_index * 80 + (row_index - 1) * 5))
                index += 1
                
        temp = temp1 + temp2
        if temp == 2:  #出双up结束本次抽卡
            msgg += f'出双up啦！共抽取{gacha_times}发十连，共计抽出{ur}张ur，{sr}张sr，{r}张r'
            break
            
    if temp == 1: #单up的提示
        msgg += f'出up啦！共抽取{gacha_times}发十连，共计抽出{ur}张ur，{sr}张sr，{r}张r'
    elif temp == 0:   #井了的提示
        msgg += f'井啦！共抽取{gacha_times}发十连，共计抽出{ur}张ur，{sr}张sr，{r}张r'


    buf = BytesIO()
    base.save(buf, format='PNG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    msg = f'''{msgg}
[CQ:image,file={base64_str}]'''
    await bot.send(ev, msg)
        


