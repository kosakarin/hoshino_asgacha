import base64, os, random, time
import hoshino
from hoshino.util import DailyNumberLimiter
from hoshino import Service, R
from hoshino.typing import CQEvent
from PIL import Image

#可能有少量bug 主要原因是上传的这个是个阉割版，少了一些东西，上传前可能没删干净那些变量
aslmt = DailyNumberLimiter(1)

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
    "1216"

    
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
    "近江彼方"
    
    
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
    days = int(time.strftime("%d", time.localtime(time.time()))) + 31 * int(
        time.strftime("%m", time.localtime(time.time()))) + 77 +  int(
        time.strftime("%y", time.localtime(time.time()))) + 2000
    return (days * qq) >> 8


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

    
@sv.on_fullmatch('as签到')
async def as_login_bonus(bot, ev):
    uid = ev['user_id']
    
    list_len = len(login_list_3)
    days = int(time.strftime("%d", time.localtime(time.time())))
    months = int(time.strftime("%m", time.localtime(time.time())))
    week = int(time.strftime("%w", time.localtime(time.time())))
    birth_flag, member_birth = get_day(days, months)
    h = hash(uid)
    if not aslmt.check(uid):
        await bot.send(ev, '你今天已经签到过啦~~', at_sender=True)
        return
    else:
        aslmt.increase(uid)
        rp = h % 100
        rp_value = []
        for i in range(list_len):
            rp_value.append(h & 3)
            h >>= 2
        msg = f'今天是{months}月{days}日 星期{week_list[week]}\n'

            
        msg += f'今日人品值：{rp}\n'
        msg += '\n今日运势:\n'
        for i in range(list_len):
            if rp_value[i] == 3:
                msg += f'{login_list_3[i]}\n'
            elif rp_value[i] == 0:
                msg += f'{login_list_0[i]}\n'
                
        if birth_flag == 1:
            msg += f'今天是{member_birth}，让我们祝{member_birth}生日快乐！'
        await bot.send(ev, msg, at_sender = True)





