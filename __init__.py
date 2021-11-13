import base64,os,math
import hoshino
from .asgacha import *
from .image import *
from .money import *
from .countpoint import count_point
from .config import get_config, get_group_config, set_group_config  
from .card_save import *
from hoshino import Service, R
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
[as仓库] 查看你的仓库
[as钱包] 查看你的钱包
[群排名] 看看你现在第几名
[as][u/s/r]查询[昵称] 查询当前bot内部有什么卡（这个地方代码不是很行，以前写的，建议删除（）
'''.strip())


base_path = 'C:\/Users/Administrator/Desktop/XCW/res/img/image/frame.png'         #底图路径
icon_path = 'C:\/Users/Administrator/Desktop/XCW/res/img/'                        #icon路径
COL_NUM = 8  #生成仓库图片时一行显示几张（我自己只试过8张，别的不清楚会不会错位啥的）
cid_list = {'1': [], '2': [], '3': []}  #将各个等级下的卡片id存进来
cids_list = [] #用来存当前所有的卡片id

def load_cards(): #预加载所有卡片资源
    global cids_list
    global cid_list
    for key in cid_list.keys():  #[稀有度]: 1 r; 2 sr; 3 ur;         #我自己根据[稀有度][团体编号][角色编号][卡片编号][觉醒标记]的规则
        for i in range(1,4):     #[团队编号]: 1 us; 2 aqours; 3 虹；  #生成了一个7位int型cid，可以调用asgacha.py下的get_cid([稀有度], 
            for ii in range(1,13):  #[角色编号]: 具体见help文本中的顺序 # [团体编号],[角色编号],[卡片编号])来获取一张未觉醒的卡片cid（因
                for iii in range(1,15): #[卡片编号]：随便编的          #为目前用不到觉醒卡片所以结尾默认写1了 
                    a = str(ii) if ii > 9 else str(f"0{ii}") #自动补0
                    b = str(iii) if  iii > 9 else str(f"0{iii}") #自动补0
                    rare = 'ur' if key == '3' else ('sr' if key == '2' else 'r') #转化稀有度为数字
                    _path = f"{icon_path}image/icon_{rare}/{i}/{ii}/{iii}.png"  #转化为对应路径
                    cid = int(f"{key}{i}{a}{b}1")  #转化为cid
                    try:
                        Image.open(_path)  #利用open来尝试是否存在此卡片
                        cid_list[key].append(cid) #存在则分别存入两个list
                        cids_list.append(cid)
                    except:
                        continue   #错误，则不存在，继续循环
load_cards() #载入时缓存所有cid

config_list = [         #用于检查设置时关键字是否正确
    "up_num",
    "up_card1",
    "up_card2",
    "up1_team",
    "up2_team",
    "up1_mem",
    "up2_mem",
    "gacha_cost"
]

def normalize_digit_format(n): #int转str自动补0
    return f'0{n}' if n < 10 else f'{n}'

def get_pic(pic_path:str, row:int):  #自动访问路径获取icon返回(row控制返回的图片大小)
    _path = icon_path + pic_path
    img = Image.open(_path)
    img = img.resize((row, row), Image.ANTIALIAS)
    return img

    
def get_pic_ex(pic_path:str, num, row:int):  #自动访问路径获取icon返回(根据卡片数量返回贴了破数贴图的图片)
    _path = icon_path + pic_path
    img = Image.open(_path)
    img = img.resize((row, row), Image.ANTIALIAS)
    star = get_pic("image/star.png", 16)
    star_disabled = get_pic("image/star_disabled.png", 16)
    num -= 1  #我定义num==2时是1破（1宝） ==3时2破 以此类推
    if num > 0: #如果num == 1 在上面-=1后就不会开始贴破数
        for i in range(0, 5):
            if i < num:
                img.paste(star, (i * 16, 60), star) #我自己内部写的是调用这个函数的row都是80像素 这里直接/5填了16，可以根据实际情况修改
            elif i >= num:
                img.paste(star_disabled, (i * 16, 60), star_disabled)
    return img

def get_grey_pic(pic_path, row): #返回一张黑白的图片（灰度图片）
    _path = icon_path + pic_path
    img = Image.open(_path)
    img = img.resize((row, row), Image.ANTIALIAS)
    img = img.convert('L')
    return img  
    
@sv.on_prefix('gacha')  
async def send_gacha(bot, ev): #用于不重启bot设置一些东西，应该可以完善一下，比如不要一条一条设置之类的，以后再改吧
    uid = ev['user_id']   #获取触发者的uid：int
    is_su = hoshino.priv.check_priv(ev, hoshino.priv.SUPERUSER) #判断权限是否足够
    args = ev.message.extract_plain_text().split()

    msg = ''
    if not is_su:  #权限不足直接退出
        await bot.send(ev, '需要超级用户权限')
        return
    elif len(args) == 0:
        await bot.send(ev, '输入错误')
        return
    elif args[0] == 'set' and len(args) >= 3: #识别到是set关键字，检测下一个关键字
        key = args[1]
        for i in config_list: #检查关键字合法性
            if key == i:
                break
        else:
            await bot.send(ev, '无此项参数')
            return
        string = args[2]
        temp = 0
        if args[2].isdigit():  #这里主要是为了将数字型的参数以int存进去，现在看看直接try except会好一些
            value = int(args[2])
            temp = 1
        else:
            temp = 2
        if temp == 1:
            try:
                set_group_config(key, value)
                msg = str(value)
            except:
                await bot.send(ev, '输入错误')
                return
        elif temp == 2:
            try:
                set_group_config(key, string)
                msg = str(string)
            except:
                await bot.send(ev, '输入错误')
                return
        await bot.send(ev, msg)
        return
    elif args[0] == 'get': #识别到关键字是get（asgacha get），返回当前参数列表
        msg += f'up_num : {get_group_config("up_num")}'
        msg += f'\nup_card1 : {get_group_config("up_card1")}'
        msg += f'\nup_card2 : {get_group_config("up_card2")}'
        msg += f'\nup1_team : {get_group_config("up1_team")}'
        msg += f'\nup2_team : {get_group_config("up2_team")}'
        msg += f'\nup1_mem : {get_group_config("up1_mem")}'
        msg += f'\nup2_mem : {get_group_config("up2_mem")}'
        msg += f'\ngacha_cost : {get_group_config("gacha_cost")}'
        await bot.send(ev, msg)
        return
    else:
        await bot.send(ev, '输入错误')
        return
    

@sv.on_rex((r'^(as|as )(.*)(一抽|单抽)(.*)'))                              #我讨厌正则表达式
async def gacha_one(bot, ev):  #单抽
    uid = ev['user_id']
    key = "starstone" #多少有点多此一举了
    now_starstone = get_user_money(uid, key)   #获得触发者当前有多少星石  在money.py下（凡是涉及到金钱操作的都在那里面
    kirastone_num = 0 #提前声明变量
    try:
        arg = str.strip(ev['match'].group(4))
        member, team = change_name(arg) #这个是asgacha.py内的一个名称转化函数，可以将识别到的关键字转成对应的团队编号和角色编号，栞的识别有点问题 需要注意
    except:
        member = 0
        team = 0
    if member == 11 or member == 12:
        await bot.finish(ev, '暂不支持米娅和钟岚珠的单人卡池模拟')  #这俩没ur 我就先写了这个 后续可以删除
        return
        
    #time_lmt.increase(uid)  #删漏了 我靠
    up_num = get_group_config("up_num")   #获取当前几张up卡
    gacha_cost = get_group_config("gacha_cost") #获取预设的单抽耗费 
        
    if str.strip(ev['match'].group(2)) == 'ur' or str.strip(ev['match'].group(2)) == 'UR': #匹配当前是ur必得模式还是普通模式
        ur_mode = 1
    else:
        ur_mode = 0
    
    cost = gacha_cost if ur_mode == 0 else (gacha_cost * 10) #暂定ur必得模式10倍消耗
    
    if ur_mode == 1: 
        if now_starstone < cost:  #判断你钱够不够  
            await bot.send(ev, f'当前剩余星星{now_starstone},不足{cost}星星！')
            return
        else:
            card_level = gacha_pup(up_num) #这个在asgacha.py中本来是计划用于判断抽出ur是否是upur的 突然想到可以直接拿来作为ur必得的随卡函数用
            reduce_user_money(uid, key, cost) #扣款 因为内部没写钱不够的校验 所有如果你需要调用请先进行校验再调用
    else:
        if now_starstone < cost:  #判断你钱够不够
            await bot.send(ev, f'当前剩余星星{now_starstone},不足{cost}星星！')
            return
        else:
            card_level = gacha_pt(up_num) #随机获取一个卡片稀有度 1：r  2：sr 3：ur 4：pickup_ur1 5：pickup_ur2 up_num控制会不会返回5
            reduce_user_money(uid, key, cost)

    _path, cid = random_give_card(card_level, member, team) #根据卡片稀有度 角色编号 团队编号直接给卡（顺序有点乱，主要是这个是第一版就写了的，那时候没想那么多
    card_temp = db.add_card(uid, cid)  #将cid和uid存入db中，返回这卡你有几张了 （添加前有6张会返回7，但是不会加入，db里面存的还是6）
    if card_temp > 6: #满突的话会添加失败，这里进行羽毛石获取的转换
        kirastone_num = 1 if card_level == 1 else (5 if card_level == 2 else 25) #根据稀有度给羽毛石
        increase_user_money(uid, "kirastone", kirastone_num) #增加货币量

    base = Image.open(base_path)  #加载底图
    f = get_pic(_path, 80)           #加载icon
    base.paste(f, (275,100), f)     #制图
    if card_temp == 1:   #根据突数贴一些特殊图标，根据图标名字应该能看出来各个图标的用途
        f2 = get_pic("image/new.png", 80)                
        base.paste(f2, (275,100), f2)
    elif card_temp > 6:
        f3 = get_pic("image/kirastone.png", 20)               
        base.paste(f3, (275,100), f3)
    else:
        f4 = get_pic(f"image/{card_temp - 1}.png", 80)               
        base.paste(f4, (275,117), f4)
    
    buf = BytesIO()
    base.save(buf, format='PNG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    msg = f'''[CQ:image,file={base64_str}]
消耗{cost}星星，剩余{get_user_money(uid, key)}星星
获得了{kirastone_num}羽毛石'''
    await bot.send(ev, msg, at_sender=True)

@sv.on_rex((r'^(as|as )(.*)(十|10)(发|抽|连|连抽)(.*)'))                  #我讨厌正则表达式  #后面的注释下次再补充
async def gacha_ten(bot, ev):  #十连
    uid = ev['user_id']
    up_num = get_group_config("up_num") 
    key = "starstone"
    now_starstone = get_user_money(uid, key)
    kirastone_num = 0
    kirastone_num_temp = 0
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
    gacha_cost = get_group_config("gacha_cost")
    cost = gacha_cost * 10 if ur_mode == 0 else (gacha_cost * 100)
    msg = '十连结果为：'
    card_level = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    if ur_mode == 1:
        if now_starstone < cost:
            await bot.send(ev, f'当前剩余星星{now_starstone},不足{cost}星星！')
            return
        else:
            reduce_user_money(uid, key, cost)
            for i in range(0,10):
                card_level[i] = gacha_pup(up_num)   
    else:
        if now_starstone < cost:
            await bot.send(ev, f'当前剩余星星{now_starstone},不足{cost}星星！')
            return
        else:
            reduce_user_money(uid, key, cost)
            for i in range(1,10):
                card_level[i] = gacha_pt(up_num)
            card_level[0] = gacha_bd(up_num)
    
    base = Image.open(base_path)  #加载底图
    row_offset = 35    #制图参数
    index = 0          #制图参数

    for level in card_level:  #依次读取卡片稀有度
        _path, cid = random_give_card(level, member, team)
        card_temp = db.add_card(uid, cid)
        if card_temp > 6:
            kirastone_num_temp = 1 if level == 1 else (5 if level == 2 else 25)
            kirastone_num += kirastone_num_temp   
        row_index = index // 5           #制图参数
        col_index = index % 5            #制图参数
        f = get_pic(_path, 80)               #加载icon
        base.paste(f, (95 + col_index * 80 + (col_index - 1) * 30,
                     row_offset + 40 + row_index * 80 + (row_index - 1) * 20), f)  #制图          

        if card_temp == 1:
            f2 = get_pic("image/new.png", 80)                
            base.paste(f2, (95 + col_index * 80 + (col_index - 1) * 30,
                          row_offset + 40 + row_index * 80 + (row_index - 1) * 20), f2)  #制图
        elif card_temp > 6:
            f3 = get_pic("image/kirastone.png", 20)               
            base.paste(f3, (95 + col_index * 80 + (col_index - 1) * 30,
                          row_offset + 40 + row_index * 80 + (row_index - 1) * 20), f3)  #制图
        else:
            f4 = get_pic(f"image/{card_temp - 1}.png", 80)               
            base.paste(f4, (95 + col_index * 80 + (col_index - 1) * 30,
                          row_offset + 57 + row_index * 80 + (row_index - 1) * 20), f4)  #制图
                
        index += 1
    increase_user_money(uid, "kirastone", kirastone_num)
    buf = BytesIO()
    base.save(buf, format='PNG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    msg = f'''[CQ:image,file={base64_str}]
消耗{cost}星星，剩余{get_user_money(uid, key)}星星
获得了{kirastone_num}羽毛石'''
    await bot.send(ev, msg, at_sender=True)
 
@sv.on_rex((r'^(as|as )(下|一|抽一)井(.*)'))                          #我讨厌正则表达式
async def gacha_jing(bot, ev):  #嫌慢？直接整一井！
    uid = ev['user_id']
    up_card1 = get_group_config("up_card1") + "\n" 
    up_card2 = get_group_config("up_card2") + "\n" 
    up_num = get_group_config("up_num") 
    gacha_cost = get_group_config("gacha_cost")
    key = "starstone"
    now_starstone = get_user_money(uid, key)
    cost = gacha_cost * 250
    try:
        arg = str.strip(ev['match'].group(3)) 
        member, team = change_name(arg)
    except:
        member = 0
        team = 0
    if member == 11 or member == 12:
        await bot.finish(ev, '暂不支持米娅和钟岚珠的单人卡池模拟')
        return
    if now_starstone < cost:
        await bot.finish(ev, f'当前剩余星星{now_starstone},不足{cost}星星！')
        return
    kirastone_num = 0
    kirastone_num_temp = 0
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
                ur += 1
            elif level == 5:
                temp2 = 1
                ur += 1
            elif level == 3:
                ur += 1
            elif level == 2:  #数量过多不显示具体sr
                sr += 1
            else:  #数量过多不显示具体r
                r += 1
   
            _path, cid = random_give_card(level, member, team)
            card_temp = db.add_card(uid, cid)
            if card_temp > 6:
                kirastone_num_temp = 1 if level == 1 else (5 if level == 2 else 25)
                kirastone_num += kirastone_num_temp   
            if level >= 3:

                row_index = index // 8            #制图参数
                col_index = index % 8             #制图参数

                f = get_pic(_path, 70)                #加载icon
                base.paste(f, (35 + col_index * 70 + (col_index - 1) * 5,
                          row_offset + 25 + row_index * 70 + (row_index - 1) * 12), f)  #制图
                if card_temp == 1:
                    f2 = get_pic("image/new.png", 70)                #up卡加载边框
                    base.paste(f2, (35 + col_index * 70 + (col_index - 1) * 5,
                          row_offset + 25 + row_index * 70 + (row_index - 1) * 12), f2)  #制图
                elif card_temp > 6:
                    f3 = get_pic("image/kirastone.png", 18)                #up卡加载边框
                    base.paste(f3, (35 + col_index * 70 + (col_index - 1) * 5,
                          row_offset + 25 + row_index * 70 + (row_index - 1) * 12), f3)  #制图
                else:
                    f4 = get_pic(f"image/{card_temp - 1}.png", 70)                #up卡加载边框
                    base.paste(f4, (35 + col_index * 70 + (col_index - 1) * 5,
                          row_offset + 38 + row_index * 70 + (row_index - 1) * 12), f4)  #制图
                index += 1
                
        temp = temp1 + temp2
        if temp == up_num_flag and up_num_flag == 1:  #出up抽齐自动结束本次抽卡
            msgg += f'up抽齐啦!已自动结束下井\n当前up卡为{up_card1}\n'
            break
        elif temp == up_num_flag and up_num_flag == 2:  #出up抽齐自动结束本次抽卡
            msgg += f'up抽齐啦!已自动结束下井\n当前up卡为{up_card1}{up_card2}\n'
            break
    if up_num_flag == 2:        
        if temp == 1: #出单up的提示
            msgg += f'出up啦！\n当前up卡为\n{up_card1}{up_card2}\n'
        elif temp == 0:   #井了的提示
            msgg += f'井啦！\n当前up卡为\n{up_card1}{up_card2}\n'
    elif up_num_flag == 1:
        if temp == 0:
            msgg += f'井啦！\n当前up卡为\n{up_card1}\n'
    
    cost = gacha_times * gacha_cost * 10
    reduce_user_money(uid, key, cost)
    increase_user_money(uid, "kirastone", kirastone_num)
    msgg += f'共抽取{gacha_times}发十连，共计抽出{ur}张ur，{sr}张sr'
    buf = BytesIO()
    base.save(buf, format='PNG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    msg = f'''{msgg}
[CQ:image,file={base64_str}]
消耗{cost}星星，剩余{get_user_money(uid, key)}星星
获得了{kirastone_num}羽毛石'''
    await bot.send(ev, msg, at_sender=True)
        
@sv.on_rex((r'^(as|as )(帮助|抽卡帮助|招募帮助|help)'))
async def as_help(bot, ev):
    await bot.send(ev, f'[CQ:image,file=base64://{image_to_base64(text_to_image(sv.help.strip())).decode()}]')

@sv.on_rex((r'^(as|as )([r|R|s|u|S|U])(查询)(.*)'))
async def card_li(bot, ev):
    match = ev['match']
    msg = ''
    i = 0
    level_labels = ['r', 's', 'u', 'R', 'S', 'U']
    
    arg_level = level_labels.index(match.group(2)) + 1
    if arg_level > 3:
        arg_level -= 3
    arg_name = str.strip(ev['match'].group(4)) 
    level = int(arg_level)
    member, team = change_name(arg_name)
    if member == 0:
        msg = '''请给出角色昵称
暂时支持的角色昵称如下：
[果][绘][鸟][海][凛][姬][希][花][妮]
[千][梨][南][黛][曜][善][丸][鞠][露]
[步梦][霞][雫][果林][爱][彼方][雪菜][艾玛][璃奈][栞][米娅][岚珠]'''
        await bot.finish(ev, f'[CQ:image,file=base64://{image_to_base64(text_to_image(msg.strip())).decode()}]', at_sender = True)
        
    base = Image.open(base_path)  #加载底图
    row_offset = 5   #制图参数
    index = 0        #制图参数

    _path, _path_2, card_num = give_card(level, member, team)
    card_n = int(card_num)
    while i < card_n:
        card_path = _path + f'{i + 1}.png'
        card_path_2 = _path_2 + f'{i + 1}.png'
        row_index = index // 8            #制图参数
        col_index = index % 8             #制图参数
        f = get_pic(card_path, 70)                #加载icon
        base.paste(f, (35 + col_index * 70 + (col_index - 1) * 5,
                          row_offset + 30 + row_index * 70 + (row_index - 1) * 5), f)  #制图
        index += 1
        row_index = index // 8            #制图参数
        col_index = index % 8             #制图参数
        f = get_pic(card_path_2, 70)                #加载icon
        base.paste(f, (35 + col_index * 70 + (col_index - 1) * 5,
                          row_offset + 30 + row_index * 70 + (row_index - 1) * 5), f)  #制图
        index += 1
        i += 1
        
    msg_level = ['R', 'SR', 'UR']    
    buf = BytesIO()
    base.save(buf, format='PNG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    msg = f'''当前bot内一共有{card_num}张{arg_name}{msg_level[level - 1]}[CQ:image,file={base64_str}]'''
    
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
    
    await bot.send(ev, f'[CQ:image,file=base64://{image_to_base64(text_to_image(msg)).decode()}]')
    
@sv.on_fullmatch(('as仓库'))
async def storage(bot, ev):
    uid = ev['user_id']
    row_nums = {}
    for star in cid_list.keys():
        row_nums[star] = math.ceil(len(cid_list[star]) / COL_NUM)
    row_num = sum(row_nums.values())
    base = Image.open('C:\/Users/Administrator/Desktop/XCW/res/img/image/frame_bg.png')
    base = base.resize((40+COL_NUM*80+(COL_NUM-1)*10, 120 +
                        row_num*80+(row_num-1)*10), Image.ANTIALIAS)
    cards_num = db.get_cards_num(uid)
    cards_num = {card_id: card_amount for card_id,
                 card_amount in cards_num.items() if card_id in cids_list}
    
    row_index_offset = 0
    row_offset = 0
    for star in cid_list.keys():
        cards_list = cid_list[star]
        for index, id in enumerate(cards_list):
            row_index = index // COL_NUM + row_index_offset
            col_index = index % COL_NUM
            card_id = cards_list[index]
            pic_path = cid_to_path(card_id)
            f = get_pic_ex(pic_path, cards_num[card_id], 80) if card_id in cards_num else get_grey_pic(
                pic_path, 80)
            
            base.paste(f, (30 + col_index * 80 + (col_index - 1) * 10,
                           row_offset + 40 + row_index * 80 + (row_index - 1) * 10))
        row_index_offset += row_nums[star]
        row_offset += 30
    ranking = db.get_ranking(uid)
    ranking_desc = f'第{ranking}位' if ranking != -1 else '未上榜'
    total_card_num = sum(cards_num.values())
    super_rare_card_num = len(
        [card_id for card_id in cards_num if card_id > 3000000])
    super_rare_card_total = len(cid_list['3'])
    rare_card_num = len(
        [card_id for card_id in cards_num if card_id > 2000000 and card_id < 3000000])
    rare_card_total = len(cid_list['2'])
    normal_card_num = len(cards_num) - super_rare_card_num - rare_card_num
    normal_card_total = len(cid_list['1'])
    buf = BytesIO()
    base = base.convert('RGB')
    base.save(buf, format='JPEG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    msg = f'''的仓库:[CQ:image,file={base64_str}]
持有卡片数: {total_card_num}
R卡收集: {normalize_digit_format(normal_card_num)}/{normalize_digit_format(normal_card_total)}
SR卡收集: {normalize_digit_format(rare_card_num)}/{normalize_digit_format(rare_card_total)}
UR卡收集: {normalize_digit_format(super_rare_card_num)}/{normalize_digit_format(super_rare_card_total)}
图鉴完成度: {normalize_digit_format(len(cards_num))}/{normalize_digit_format(len(cids_list))}
当前群排名: {ranking_desc}'''
    await bot.send(ev, msg, at_sender = True)
  
@sv.on_fullmatch(('群排名'))
async def my_rank(bot, ev):
    uid = ev['user_id']
    ranking = db.get_ranking(uid)
    ranking_desc = f'第{ranking}位' if ranking != -1 else '未上榜'
    await bot.send(ev, ranking_desc, at_sender = True)
  
