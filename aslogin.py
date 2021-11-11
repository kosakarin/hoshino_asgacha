import base64, os, random, time
from .image import *
from .money import *
import hoshino
from hoshino import Service
from hoshino.typing import CQEvent
from PIL import Image


sv = Service('as签到', bundle='aslogin', help_='''使用如下命令进行签到：
as签到
'''.strip())



login_list_3 = [
    '宜 抽卡',
    '宜 干饭',
    '宜 摸鱼',
    '宜 刷饰品',
    '宜 刷合宿',
    '宜 凹分榜',
    '宜 逛b站',
    '宜 逛漫展',
    '宜 出门逛街',
    '宜 好好学习'

]

login_list_0 = [
    '忌 抽卡',
    '忌 干饭',
    '忌 摸鱼',
    '忌 刷饰品',
    '忌 刷合宿',
    '忌 凹分榜',
    '忌 逛b站',
    '忌 逛漫展',
    '忌 出门逛街',
    '忌 好好学习'

]

birth_list = [
    "0117",
    "0315",
    "0419",
    "0609",
    "0722",
    "0803",
    "0912",
    "1021", 
    "1101",
    
    "0101",
    "0210",
    "0304",
    "0417",
    "0613",
    "0713",
    "0801",
    "0919",
    "0921",
    
    "0123",
    "0205",
    "0215",
    "0301",
    "0403",
    "0530",
    "0629",
    "0808",
    "1005",
    "1113",
    "1206",
    "1216",
    
    
    "0203"
    
]

member_list = [
    "小泉花阳",
    "园田海未",
    "西木野真姬",
    "东条希",
    "矢泽妮可",
    "高坂穗乃果",
    "南小鸟",
    "绚濑绘里",
    "星空凛",
    
    "黑泽黛雅",
    "松浦果南",
    "国木田花丸",
    "渡边曜",
    "小原鞠莉",
    "津岛善子",
    "高海千歌",
    "樱内梨子",
    "黑泽露比",
    
    "中须霞",
    "艾玛·维尔德",
    "钟岚珠",
    "上原步梦",
    "樱坂雫",
    "宫下爱",
    "朝香果林",
    "优木雪菜",
    "三船栞子",
    "天王寺璃奈",
    "米娅·泰勒",
    "近江彼方",
    
    
    "小环奈"
    
]

week_list = [
    "日",
    "一",
    "二",
    "三",
    "四",
    "五",
    "六"
]

def hash(qq: int):
    days = int(time.strftime("%d", time.localtime(time.time()))) + random.randint(0, 31) * int(
        time.strftime("%m", time.localtime(time.time()))) + random.randint(0, 77) +  int(
        time.strftime("%y", time.localtime(time.time()))) + random.randint(0, 114)
    return (days * qq - random.randint(0, 514)) >> 8


def get_day(days, months):
    flag_day = str(days) if days > 9 else f'0{str(days)}'
    flag_month = str(months) if months > 9 else f'0{str(months)}'
    flag = flag_month + flag_day
    i = 0
    for birth in birth_list:
        if flag == birth:
            return 1, member_list[i]
        i += 1

    return 0, ''


@sv.on_rex(('as签到帮助'))
async def aslogin_help(bot, ev):
    await bot.send(ev, f'[CQ:image,file=base64://{image_to_base64(text_to_image(sv.help.strip())).decode()}]')
    
@sv.on_rex(r'^(as|as |AS|AS )签到')
async def as_login_bonus(bot, ev):
    uid = ev['user_id']
    key = "starstone"
    list_len = len(login_list_3)
    days = int(time.strftime("%d", time.localtime(time.time())))
    months = int(time.strftime("%m", time.localtime(time.time())))
    week = int(time.strftime("%w", time.localtime(time.time())))
    birth_flag, member_birth = get_day(days, months)
    last_login = int(get_user_money(uid, "last_login"))
    h = hash(int(uid))
    if days == last_login:
        await bot.send(ev, '你今天已经签到过啦~~', at_sender=True)
        return
    else:
        set_user_money(uid, "last_login", days)
        rp = h % 101
        rp_value = []
        for i in range(list_len):
            rp_value.append(h & 3)
            h >>= 2
        msg = f'今天是{months}月{days}日 星期{week_list[week]}\n'
        if birth_flag == 1:
            msg += f'今天是{member_birth}的生日！让我们祝{member_birth}生日快乐！\n'
            
        msg += f'今日人品值：{rp}\n'
        if rp >= 95:
            loveca_num = max(1, min(3, rp - 95))
            msg += f'大幸运！获得了{loveca_num}枚lovecastone！\n'
            increase_user_money(uid, "lovecastone", loveca_num)
        msg += '\n今日运势:\n'
        for i in range(list_len):
            if rp_value[i] == 3:
                msg += f'{login_list_3[i]}\n'
            elif rp_value[i] == 0:
                msg += f'{login_list_0[i]}\n'
        num = rp * 5 + (1 + birth_flag) * 500
        increase_user_money(uid, key, num)
        
        msg += f'获得了{num}星星！\n当前拥有{str(get_user_money(uid, key))}星星！！'

        await bot.send(ev, f'[CQ:image,file=base64://{image_to_base64(text_to_image(msg)).decode()}]', at_sender = True)
