import base64,os
from .asgacha import *
from hoshino import Service, R
from .countpoint import count_point
from hoshino.typing import CQEvent
from PIL import Image

from io import BytesIO


sv = Service('as抽卡', bundle='as', help_='''使用如下命令进行抽卡模拟：
[as][单抽|十连|一井][不加为普通卡池|角色名称|团队名称]
暂时支持的角色昵称如下：
[果][绘][鸟][海][凛][姬][希][花][妮]
[千][梨][南][黛][曜][善][丸][鞠][露]
[步梦][霞][雫][果林][爱][彼方][雪菜][艾玛][璃奈][栞][米娅][岚珠]
团体名称：[缪][水][虹]
暂不支持小队招募,以及米娅和岚珠的单人招募
使用如下命令进行控分计算：(模式：0或不提供:默认  1:仅S  2:无剧情关卡 3:无剧情关卡且仅S)
[as控分][分数1][分数2][模式] 
[as控分][分数][模式]
注：程序内部会自动取较大值为目标分数，
分数2请不要提供小于10的数，会被识别为模式参数
'''.strip())

up_num = 1 #当前卡池为单up还是双up
base_path = 'C:\/Users/Administrator/Desktop/XCW/res/img/image/frame.png'         #底图路径
icon_path = 'C:\/Users/Administrator/Desktop/XCW/res/img/'                        #icon路径
up_card1 = '【綺麗に色づいてるね】松浦果南！\n'
up_card2 = ''


def get_pic(pic_path:str, row:int):  #自动访问路径获取icon返回(返回的img像素为80*80)
    _path = icon_path + pic_path
    img = Image.open(_path)
    img = img.resize((row, row), Image.ANTIALIAS)
    return img

@sv.on_rex((r'^(as|as )(.*)(一抽|单抽)(.*)'))                              #我讨厌正则表达式
async def gacha_one(bot, ev):  #单抽
    
    try:
        arg = str.strip(ev['match'].group(4))
        member, team = change_name(arg) 
    except:
        member = 0
        team = 0
    if member == 11 or member == 12:
        await bot.finish(ev, '暂不支持米娅和钟岚珠的单人卡池模拟')
        
    if str.strip(ev['match'].group(2)) == 'ur' or str.strip(ev['match'].group(2)) == 'UR':
        ur_mode = 1
    else:
        ur_mode = 0

    msg = ''
    if ur_mode == 1:
        card_level = gacha_pup(up_num)
    else:
        card_level = gacha_pt(up_num)
    #_path = random_give_card(card_level)
    _path = random_give_card(card_level, member, team)
    base = Image.open(base_path)  #加载底图
    f = get_pic(_path, 80)           #加载icon
    base.paste(f, (275,100))     #制图
    
    buf = BytesIO()
    base.save(buf, format='PNG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    await bot.send(ev, f'[CQ:image,file={base64_str}]', at_sender=True)



@sv.on_rex((r'^(as|as )(.*)(十|10)(发|抽|连|连抽)(.*)'))                  #我讨厌正则表达式
async def gacha_ten(bot, ev):  #十连
    try:
        arg = str.strip(ev['match'].group(5))
        member, team = change_name(arg)
    except:
        member = 0
        team = 0
    if member == 11 or member == 12:
        await bot.finish(ev, '暂不支持米娅和钟岚珠的单人卡池模拟')

    if str.strip(ev['match'].group(2)) == 'ur' or str.strip(ev['match'].group(2)) == 'UR':
        ur_mode = 1
    else:
        ur_mode = 0
    msg = '十连结果为：'
    card_level = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if ur_mode == 1:
        for i in range(0,10):
            card_level[i] = gacha_pup(up_num)
    else:
        for i in range(1,10):
            card_level[i] = gacha_pt(up_num)
        card_level[0] = gacha_bd(up_num)
    
    base = Image.open(base_path)  #加载底图
    row_offset = 35    #制图参数
    index = 0          #制图参数

        
    for level in card_level:  #依次读取卡片稀有度
        #_path = random_give_card(level)  #获取icon path
        _path = random_give_card(level, member, team)
        row_index = index // 5           #制图参数
        col_index = index % 5            #制图参数
        f = get_pic(_path, 80)               #加载icon
        base.paste(f, (95 + col_index * 80 + (col_index - 1) * 30,
                     row_offset + 40 + row_index * 80 + (row_index - 1) * 20))  #制图
        index += 1
        #msg += R.img(_path).cqcode  ####
    buf = BytesIO()
    base.save(buf, format='PNG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    await bot.send(ev, f'[CQ:image,file={base64_str}]', at_sender=True)

    
    
@sv.on_rex((r'^(as|as )(下|一|抽一)井(.*)'))                          #我讨厌正则表达式
async def gacha_jing(bot, ev):  #嫌慢？直接整一井！

    try:
        arg = str.strip(ev['match'].group(3)) 
        member, team = change_name(arg)
    except:
        member = 0
        team = 0
    if member == 11 or member == 12:
        await bot.finish(ev, '暂不支持米娅和钟岚珠的单人卡池模拟')

    up = 0
    ur = 0
    sr = 0
    r = 0  #统计用
    up_num_flag = up_num
    temp = 0
    temp1 = 0
    temp2 = 0 #记录是否出up
    gacha_times = 0 #记录出up时抽了多少发十连
    msgg = ''
    
    base = Image.open(base_path)  #加载底图
    row_offset = 5   #制图参数
    index = 0        #制图参数
    
    if member != 0:
        up_num_flag = 0
    elif team != 0:
        up_num_flag = 0  
        
    for i in range(1,26):   #25发10连
        gacha_times += 1
        card_level = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for ii in range(1,10):   #单次十连计算
            card_level[ii] = gacha_pt(up_num_flag)
        card_level[0] = gacha_bd(up_num_flag)
        
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
                #_path = random_give_card(level)   #获取icon path
                _path = random_give_card(level, member, team)
                row_index = index // 8            #制图参数
                col_index = index % 8             #制图参数
                f = get_pic(_path, 70)                #加载icon
                base.paste(f, (35 + col_index * 70 + (col_index - 1) * 5,
                          row_offset + 30 + row_index * 70 + (row_index - 1) * 5))  #制图
                index += 1
                
        temp = temp1 + temp2
        if temp == up_num_flag and up_num_flag != 0:  #出up抽齐自动结束本次抽卡
            msgg += f'up抽齐啦!已自动结束下井\n当前up卡为{up_card1}{up_card2}\n'
            break
    if up_num_flag == 2:        
        if temp == 1: #单up的提示
            msgg += f'出up啦！\n当前up卡为{up_card1}{up_card2}\n'
        elif temp == 0:   #井了的提示
            msgg += f'井啦！\n当前up卡为{up_card1}{up_card2}\n'
    elif up_num_flag == 1:
        if temp == 0:
            msgg += f'井啦！\n当前up卡为{up_card1}{up_card2}\n'
   
        
    msgg += f'共抽取{gacha_times}发十连，共计抽出{ur}张ur，{sr}张sr'
    buf = BytesIO()
    base.save(buf, format='PNG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    msg = f'''{msgg}
[CQ:image,file={base64_str}]'''
    await bot.send(ev, msg, at_sender=True)
        

@sv.on_rex((r'^(as|as )角色列表'))
async def cha_li(bot, ev):
    msg = '''暂时支持的角色昵称如下：
果 绘 鸟 海 凛 姬 希 花 妮
千 梨 南 黛 曜 善 丸 鞠 露
步梦 霞 雫 果林 爱 彼方 雪菜 艾玛 璃奈 栞 米娅 岚珠
团体名称：缪 水 虹
暂不支持小队招募'''
    await bot.send(ev, msg)


@sv.on_prefix(('as控分'))
async def up_ca(bot, ev):
    args = ev.message.extract_plain_text().strip().split()
    if len(args) <= 0 or len(args) > 3:
        await bot.send(ev, '输入错误，使用as帮助查看具体指令')
        return
    elif len(args) == 3:
        try:
            target = max(int(args[0]), int(args[1]))
            x = min(int(args[0]), int(args[1]))
            mod = int(args[2])
        except:
            await bot.send(ev, '输入类型错误')

        msg = count_point(target, x, mod)
    elif len(args) == 2:
        try:
            arg = int(args[1])
        except:
            await bot.send(ev, '输入类型错误')
            return
        if arg <= 10:
            try:
                target = int(args[0])
                msg = count_point(target, 0, arg)
            except:
                await bot.send(ev, '输入类型错误')
                return
        else: 
            try:
                target = max(int(args[0]), int(args[1]))
                x = min(int(args[0]), int(args[1]))
                msg = count_point(target, x, 0)
            except:
                await bot.send(ev, '输入类型错误')
                return
    else:
        try:
            msg = count_point(int(args[0]), 0, 0)
        except:
            await bot.send(ev, '输入类型错误')
            return

    await bot.send(ev, msg, at_sender=True)
