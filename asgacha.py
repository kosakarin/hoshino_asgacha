import os, random, base64
from .config import config, money
from .res import gacha, card_save
from PIL import Image
from io import BytesIO

#抽卡模拟器

image_path = os.path.join(os.path.dirname(__file__), 'image/')      #'./iamge/'
card_path = os.path.join(os.path.dirname(__file__), 'image/icon/1/')  #./iamge/icon/1/'
up1 = config.get_config("up1")
up2 = config.get_config("up2")
up_num = config.get_config("num")
cost = config.get_config("cost")


cid_list = {'1': [], '2': [], '3': []} 
cids_list = []
ur_prob = 0.05   #单次抽卡ur爆率为5%
sr_prob = 0.15   #单次抽卡sr爆率为15%
up_prob = 0.2    #当抽出ur时这张卡有10%概率为up卡     (单up时填双倍概率)
up_prob_ = 0.5   #当抽出up时这张卡有50%概率为pick_up1 (单up时填0.5)

probal_list = [ur_prob, sr_prob, up_prob, up_prob_]



def load_cards(): #预加载所有卡片资源
    global cids_list
    global cid_list
    try:
        cid_list = {'1': [], '2': [], '3': []}
        cids_list = []
        card_list = sorted((fn for fn in os.listdir(card_path) if fn.endswith('.png')))
        for card in card_list:
            cid = int(f'{card[0]}{card[1]}{card[2]}{card[3]}{card[4]}{card[5]}{card[6]}')
            cids_list.append(cid)
            cid_list[card[0]].append(cid)
        return 1
    except:
        return 0

load_cards()

def reload_config():
    global up1
    global up2
    global up_num
    global cost
    up1 = config.get_config("up1")
    up2 = config.get_config("up2")
    up_num = config.get_config("num")
    cost = config.get_config("cost")
    if load_cards():
        return 1
    else:
        return 0

def get_pic_ex(pic_path, num, row):  #自动访问路径获取icon返回(同时返回卡片破数贴图)
    _path = pic_path
    img = Image.open(_path)
    img = img.resize((row, row), Image.ANTIALIAS)
    star = get_pic(f"{image_path}star.png", 16)
    star_disabled = get_pic(f"{image_path}star_disabled.png", 16)
    num -= 1
    if num > 0:
        for i in range(0, 5):
            if i < num:
                img.paste(star, (i * 16, 60), star)
            elif i >= num:
                img.paste(star_disabled, (i * 16, 60), star_disabled)
    return img

def get_grey_pic(pic_path, row):
    _path = pic_path
    img = Image.open(_path)
    img = img.resize((row, row), Image.ANTIALIAS)
    img = img.convert('L')
    return img

def get_pic(_path, row = 80, num = 0):  #自动访问路径获取icon返回
    if num:
        img = Image.new("RGB",(row, int(row * 1.2)), (255, 255, 255))
        f = Image.open(_path)
        f = f.resize((row, row), Image.ANTIALIAS)
        img.paste(f, (0, 0), f)
        if num == 1:
            t = Image.open(f'{image_path}{num}.png')
            t = t.resize((row, row), Image.ANTIALIAS)
            img.paste(t, (0, 0), t)
        elif num <= 6:
            t = Image.open(f'{image_path}{num}.png')
            t = t.resize((row - 2, row - 2), Image.ANTIALIAS)
            img.paste(t, (1, int(row * 0.21)), t)
        elif num == 7:
            t = Image.open(f'{image_path}kirastone.png')
            t = t.resize((row // 5, row // 5), Image.ANTIALIAS)
            img.paste(t, (0, 0), t)
    else:
        img = Image.open(_path)
        img = img.resize((row, row), Image.ANTIALIAS)
        
    return img

def cid_to_path(card_list, times = 0):  #给定cid 返回对应的路径 3308051
    if times:
        result_list = []
        for i in card_list:
            if times <= 10:
                cid_str = str(i['cid'])
                result_list.append({'num':i['num'], 'path':f'{card_path}{cid_str}.png'})
            elif i['cid'] >= 3000000:
                cid_str = str(i['cid'])
                result_list.append({'num':i['num'], 'path':f'{card_path}{cid_str}.png'})
    else:
        result_list = f'{card_path}{card_list}.png'
    return result_list

def get_gacha_list(member, team):
    gacha_list = {'1': [], '2': [], '3': []}
    if member:
        _range = {'1': ((team * 100000) + (member * 1000) + 1000000), 
                  '2': ((team * 100000) + (member * 1000) + 2000000),
                  '3': ((team * 100000) + (member * 1000) + 3000000)}
        for i in ['1', '2', '3']:
            for cid in cid_list[i]:
                if cid in range(_range[i], _range[i] + 999):
                    gacha_list[i].append(cid)
    elif team:
        _range = {'1': ((team * 100000) + 1000000), 
                  '2': ((team * 100000) + 2000000),
                  '3': ((team * 100000) + 3000000)}
        for i in ['1', '2', '3']:
            for cid in cid_list[i]:
                if cid in range(_range[i], _range[i] + 99999):
                    gacha_list[i].append(cid)
    else:
        for i in ['1', '2', '3']:
            for cid in cid_list[i]:
                if cid == up1 or cid == up2:
                    continue
                gacha_list[i].append(cid)
    
    return gacha_list

def remake_level_list(level_list, gacha_mode):
    if not gacha_mode:
        for i in level_list:
            for ii in range(len(i)):
                if i[ii] > 3:
                    i[ii] = 3
    elif up_num == 1:
        for i in level_list:
            for ii in range(len(i)):
                if i[ii] == 5:
                    i[ii] = 3
    return level_list

def save_card(card_list, uid):
    result_list = []
    for cid in card_list:
        _num = card_save.db.add_card(uid, cid)
        result_list.append({'cid':cid, 'num':_num})
    return result_list

def get_msg(card_num):
    ur_num = card_num['3'] + card_num['4'] + card_num['5'] 
    sr_num = card_num['2'] 
    msg = f'共抽到{ur_num}张UR,{sr_num}张SR\n'
    if card_num['4']:
        msg += '抽到' + config.get_config('name1') + '啦！\n'
    if card_num['5']:
        msg += '抽到' + config.get_config('name2') + '啦！\n' 
    return msg

def make_img(path_list, times):
    _len = len(path_list)
    base = Image.open(f'{image_path}frame.png')  #加载底图
    base = base.resize((650,310), Image.ANTIALIAS)
    index = 0
    if times == 250:
        for i in path_list:
            _path = i['path']
            row_index = index // 8            #制图参数
            col_index = index % 8             #制图参数
            f = get_pic(_path, 70, i['num'])                #加载icon
            base.paste(f, (35 + col_index * 70 + (col_index - 1) * 5,
                           30 + row_index * 70 + (row_index - 1) * 12))  #制图
            index += 1
    elif times == 10:
        for i in path_list:
            _path = i['path']
            row_index = index // 5           #制图参数
            col_index = index % 5            #制图参数
            f = get_pic(_path, 80, i['num'])               #加载icon
            base.paste(f, (95 + col_index * 80 + (col_index - 1) * 30,
                           75 + row_index * 80 + (row_index - 1) * 20))  #制图 
            index += 1
    else:
        for i in path_list:
            _path = i['path']
            f = get_pic(_path, 80, i['num'])           #加载icon
            base.paste(f, (275,100))     #制图
            
            
    buf = BytesIO()
    base.save(buf, format='PNG')
    
    base.save('./test.png')  #测试用语句
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    return base64_str


def as_gacha(name, uid, times, ur_mode):
    if ur_mode and times == 250:
        return '不支持UR下井'
    #金钱判断
    need = times * cost * (10 ** ur_mode)
    have = money.get_user_money(uid, 'starstone')
    if have < need:
        return f'金钱不足，需要{need}星星，拥有{have}星星'
    member, team = gacha.change_name(name)
    if member == 12:
        return '暂不支持钟岚珠'
    
    gacha_mode = 1 if member == 0 and team == 0 else 0
    gacha_list = cid_list if gacha_mode else get_gacha_list(member, team)
    level_list = remake_level_list(gacha.random_give_level(times, ur_mode, probal_list), gacha_mode)
    card_list = []
    card_num = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0} #计数定义在这里是为了gacha_mode == 1时井出货停止
    for i in level_list:
        for level in i:
            card_num[str(level)] += 1
            if level <= 3:
                card_list.append(random.choice(gacha_list[str(level)]))
            elif level == 4:
                card_list.append(up1)
            elif level == 5:
                card_list.append(up2)
        if card_num['4'] and card_num['5']:  #不用考虑10连和单抽
            break
        elif card_num['4'] and up_num == 1:
            break
    #卡片存入
    _card_list = save_card(card_list, uid)
    result_list = cid_to_path(_card_list, times)
    #金钱计算
    kirastone_num = 0
    for i in _card_list:
        if i['num'] == 7:
            kirastone_num += 25 if i['cid'] > 3000000 else (5 if i['cid'] > 2000000 else 1)
    reduce_money = len(card_list) * cost * (10 ** ur_mode)
    #金钱改变
    money.increase_user_money(uid, 'kirastone', kirastone_num)
    money.reduce_user_money(uid, 'starstone', reduce_money)
    
    msg = f'''{get_msg(card_num)}[CQ:image,file={make_img(result_list, times)}]
共抽卡{len(card_list)}次，花费{reduce_money}星星，获得{kirastone_num}羽毛石！
'''
    
    return msg
