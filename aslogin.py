import random, time
from .config import money


login_list_3 = [ '宜 抽卡', '宜 干饭', '宜 摸鱼', '宜 刷饰品', 
                 '宜 刷合宿', '宜 凹分榜', '宜 逛b站', '宜 逛漫展',
                 '宜 出门逛街', '宜 好好学习'
]

login_list_0 = ['忌 抽卡', '忌 干饭', '忌 摸鱼', '忌 刷饰品', 
                '忌 刷合宿', '忌 凹分榜', '忌 逛b站', '忌 逛漫展', 
                '忌 出门逛街', '忌 好好学习'
]

birth_list = ["0117", "0315", "0419", "0609", "0722", "0803", "0912", "1021", "1101",  
              "0101", "0210", "0304", "0417", "0613", "0713", "0801", "0919", "0921", 
              "0123", "0205", "0215", "0301", "0403", "0530", "0629", "0808", "1005", "1113", "1206", "1216",
              "0203"  
]

member_list = ["小泉花阳", "园田海未", "西木野真姬", "东条希", "矢泽妮可", "高坂穗乃果", "南小鸟", "绚濑绘里", "星空凛",
               "黑泽黛雅", "松浦果南", "国木田花丸", "渡边曜", "小原鞠莉", "津岛善子", "高海千歌", "樱内梨子", "黑泽露比",
               "中须霞", "艾玛·维尔德", "钟岚珠", "上原步梦", "樱坂雫", "宫下爱", "朝香果林", "优木雪菜", "三船栞子", "天王寺璃奈", "米娅·泰勒", "近江彼方",
               "小环奈"  
]

event_list = ['0101', '1225']

event_name_list = ['元旦节', '圣诞节']

week_list = [ "日", "一", "二", "三", "四", "五", "六"]

def hash():
    days = random.randint(10000000, 99999999)
    return days >> 8

def conti_login(days, months, last_login):
    try:
        _last_login = str(last_login)
        _len = len(_last_login)
        _m = ''
        _d = ''
        temp = 0
        for i in range(_len):
            if _last_login[_len - i -1] == '0' and i != 0 and not temp:
                temp = 1
                continue
            if temp:
                _m += _last_login[_len - i -1]
            else:
                _d +=_last_login[_len - i -1]
        _m += '0' if len(_m) == 2 else ''
        _d += '0' if len(_d) == 1 else ''
        _months = int(f'{_m[1]}{_m[0]}')
        _days = int(f'{_d[1]}{_d[0]}')
        if days - _days == 1 and _months == months:
            return 1
        elif days == 1 and months - _months == 1:
            if _days == 31 and _months in [1,3,5,7,8,10,12]:
                return 1
            elif _days == 30 and _months in [4,6,9,11]:
                return 1
            elif _days == 28 | 29 and _months == 2:
                return 1
            else:
                return 0
        elif days == 1 and months == 1:
            return 1 if _days == 31 and _months == 12 else 0
        else:
            return 0
    except:
        return 0
    

def get_day(days, months):
    flag_day = str(days) if days > 9 else f'0{str(days)}'
    flag_month = str(months) if months > 9 else f'0{str(months)}'
    flag = flag_month + flag_day
    i = 0
    msg = ''
    birth_flag = 0
    event_flag = 0
    for birth in birth_list:
        if flag == birth:
            birth_flag = 1
            msg += f'今天是{member_list[i]}的生日！让我们祝{member_list[i]}生日快乐！\n额外获得了500星星和200金币哦\n'
            break
        i += 1
    i = 0
    for event in event_list:
        if flag == event:
            event_flag == 1
            msg += f'今天是{event_name_list[i]}！\n额外获得了500星星和200金币哦\n'
            break
        i += 1

    return birth_flag, event_flag, msg

def as_login(uid, vip):
    list_len = len(login_list_3)
    days = int(time.strftime("%d", time.localtime(time.time())))
    months = int(time.strftime("%m", time.localtime(time.time())))
    week = int(time.strftime("%w", time.localtime(time.time())))
    birth_flag, event_flag, msgg = get_day(days, months)
    last_login = int(money.get_user_money(uid, "last_login"))
    gold = 400
    conti_flag = conti_login(days, months, last_login)
    
    login_flag = 1 if int(f'{months}0{days}') == last_login else 0
    h = int(money.get_user_money(uid, "rp")) if login_flag else hash()
    _h = h
    rp = _h % 101
    rp_value = []
    
    for i in range(list_len):
        rp_value.append(_h & 3)
        _h >>= 2
    msg = f'今天是{months}月{days}日 星期{week_list[week]}\n' 
    msg += '你今天已经签过到啦\n' if login_flag else ''
    if conti_flag and not login_flag:
        money.increase_user_money(uid, "logindays", 1)
    elif not login_flag:
        money.set_user_money(uid, "logindays", 1)
    
    msg += msgg        
    msg += f'今日人品值：{rp}\n'
    if rp >= 95 and not login_flag:
        loveca_num = max(1, min(3, rp - 95))
        msg += f'大幸运！获得了{loveca_num}枚lovecastone！\n'
        money.increase_user_money(uid, "lovecastone", loveca_num)
        
    msg += '\n今日运势:\n'
    for i in range(list_len):
        if rp_value[i] == 3:
            msg += f'{login_list_3[i]}\n'
            gold += 300 if i == 1 else 20
        elif rp_value[i] == 0:
            msg += f'{login_list_0[i]}\n'
            gold -= 200 if i == 1 else 10
    if not login_flag:
        logindays = money.get_user_money(uid, "logindays")
        num = rp * 5 + (1 + birth_flag + event_flag) * 500 + min(500, (logindays // 10) * 50)
        gold += (birth_flag + event_flag) * 200 + min(500, (logindays - 1) * 5)
        money.increase_user_money(uid, "starstone", num)
        money.increase_user_money(uid, 'gold', gold)
        money.set_user_money(uid, "last_login", int(f'{months}0{days}'))
        money.set_user_money(uid, "rp", h)
        msg += f'您已连续签到{logindays}天，额外获得{min(500, (logindays // 10) * 50)}星星\n'
        msg += f'总计获得了{num}星星！\n当前拥有{str(money.get_user_money(uid, "starstone"))}星星！！\n获得了{gold}金币！'
   

    return msg
       
