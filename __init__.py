import hoshino, asyncio
from hoshino import Service
from hoshino.typing import CQEvent
from .config import money
from .asgacha import as_gacha
from .aslogin import as_login
from .res import pcalculator, image
from . import randomtkk

COL_NUM = 18 #仓库查看时每行多少个

#本文件仅作为触发器使用，所有抽卡计算全部交由asgacha.py处理，其他对应功能交给对应文件处理
#各模块会将处理好的msg返回到本文件中对应的触发器中，然后由本文件负责让bot输出对应结果
sv = Service('as抽卡', bundle='as', help_='''使用如下命令进行抽卡模拟：
[as][单抽|十连|一井][不加为普通卡池|角色名称|团队名称]
暂时支持的角色昵称如下：
[果][绘][鸟][海][凛][姬][希][花][妮]
[千][梨][南][黛][曜][善][丸][鞠][露]
[步梦][霞][雫][果林][爱][彼方][雪菜][艾玛][璃奈][栞][米娅][岚珠]
团体名称：[缪][水][虹]
暂不支持小队招募,以及钟岚珠的单人招募
使用如下命令进行控分计算：(模式：0或不提供:默认  1:仅S  2:无剧情关卡 3:无剧情关卡且仅S)
[as控分][分数1][分数2][模式] 
[as控分][分数][模式]
[as加成控分][加成][分数1][分数2][模式](同无加成控分，但是加成必须写在第一位，你有18%加成就说18)
※暂时请不要使用加成控分，暂未理清活动pt的取整规则，加成计算存在取整误差
注：程序内部会自动取较大值为目标分数，
分数2请不要提供小于10的数，会被识别为模式参数
[as仓库] 查看你的仓库
[as钱包] 查看你的钱包
[群排名] 看看你现在第几名
'''.strip())

key_list = ["gold", "lovecastone", "starstone", "kirastone"]

#单抽
@sv.on_rex((r'^(as|as )(.*)(一抽|单抽)(.*)'))                              #我讨厌正则表达式
async def gacha_one(bot, ev):  #单抽
    uid = ev['user_id']
    try:
        name = str.strip(ev['match'].group(4))
    except:
        name = ''
    ur_mode = 1 if str.strip(ev['match'].group(2)) == 'ur' or str.strip(ev['match'].group(2)) == 'UR' else 0
    msg = as_gacha(name, uid, 1, ur_mode)
    await bot.send(ev, msg, at_sender=True)
    
#十连
@sv.on_rex((r'^(as|as )(.*)(十|10)(发|抽|连|连抽)(.*)'))                  #我讨厌正则表达式
async def gacha_ten(bot, ev):  #十连
    uid = ev['user_id']
    try:
        name = str.strip(ev['match'].group(5))
    except:
        name = ''
    ur_mode = 1 if str.strip(ev['match'].group(2)) == 'ur' or str.strip(ev['match'].group(2)) == 'UR' else 0
    msg = as_gacha(name, uid, 10, ur_mode)
    await bot.send(ev, msg, at_sender=True)
    
#一井
@sv.on_rex((r'^(as|as )(下|一|抽一)井(.*)'))                          #我讨厌正则表达式
async def gacha_jing(bot, ev):  #嫌慢？直接整一井！
    uid = ev['user_id']
    try:
        name = str.strip(ev['match'].group(3))
    except:
        name = ''
    msg = as_gacha(name, uid, 250, 0)
    await bot.send(ev, msg, at_sender=True)

#签到
@sv.on_rex(r'^(as|as |AS|AS )签到')
async def as_login_bonus(bot, ev):
    uid = uid = ev['user_id']
    vip = hoshino.priv.check_vip(uid)
    
    msg, add_vip_flag = as_login(uid, vip)
    if add_vip_flag:
        hoshino.priv.add_vip(uid)
    await bot.send(ev, f'[CQ:image,file=base64://{image.image_to_base64(image.text_to_image(msg.strip())).decode()}]')

#计算器
@sv.on_prefix(('as控分'))
async def up_ca(bot, ev):
    args = ev.message.extract_plain_text().strip().split()
    msg = pcalculator.get_msg(args)
    if len(msg) > 30:
        await bot.send(ev, f'[CQ:image,file=base64://{image.image_to_base64(image.text_to_image(msg.strip())).decode()}]')
    else:
        await bot.send(ev, msg)
    
#唐可可
@sv.on_prefix(('随机唐可可'))                              
async def random_tkk(bot, ev):  
    gid = ev["group_id"]
    args = ev.message.extract_plain_text().strip().split()
    msg1, _waittime, msg3 = randomtkk.randomtkk(gid, args)
    if msg1 == '':
        return
    await bot.send(ev, msg1)
    msg2 = f'将在{_waittime}s后公布答案'
    await bot.send(ev, msg2)
    await asyncio.sleep(_waittime)
    if randomtkk.cheak_guess_flag(gid):
        return    
    randomtkk.close_game(gid)
    await bot.send(ev, msg3)

@sv.on_prefix(('答案是'))
async def huida(bot, ev):
    gid = ev["group_id"]
    args = ev.message.extract_plain_text().strip().split()
    
    if randomtkk.cheak_game(gid, args):
        await bot.send(ev, "好厉害!", at_sender = True)
    else:
        return

#仓库查看
@sv.on_fullmatch(('as仓库'))
async def storage(bot, ev):
    uid = ev['user_id']
    msg = card.card_storage(uid, COL_NUM, 0)
    await bot.send(ev, msg, at_sender = True)

@sv.on_fullmatch(('as角色仓库'))
async def charastorage(bot, ev):
    uid = ev['user_id']
    msg = card.card_storage(uid, COL_NUM, 1)
    await bot.send(ev, msg, at_sender = True)
   
@sv.on_fullmatch(('群排名'))
async def my_rank(bot, ev):
    uid = ev['user_id']
    msg = card.get_my_rank(uid)
    await bot.send(ev, msg, at_sender = True)

#财富管理    这地方不想再单开一个文件了（
@sv.on_fullmatch('我的钱包')
async def money_get(bot, ev):
    uid = ev['user_id'] 
    msg = ''
    for key in key_list:
        msg += f'\n{key} = {money.get_user_money(uid, key)}'
    msg += '\n收集100枚lovecastone后有神秘奖励哦！'
    await bot.send(ev, msg, at_sender = True)


@sv.on_fullmatch('whosyourdaddy')
async def money_test(bot, ev):
    uid = ev['user_id']
    if uid == your_uid: #修改为你的qq号  
        for key in key_list:
            money.increase_user_money(uid, key, 12500)
        msg = '测试用物资已下发'
        await bot.send(ev, msg, at_sender = True)
    else:
        return
        
@sv.on_prefix('as兑换')
async def chongqian(bot, ev):
    uid = ev['user_id']
    string = ev.message.extract_plain_text().strip()
    arrs = string.split('/')
    if len(arrs) == 0:
        await bot.send(ev, '请使用 [as兑换][币种名称]/[数字]来消耗羽毛石转化为其他币种,不提供数量将默认全部消耗')
        return
    elif len(arrs) == 1:
        key = money.translatename(arrs[0])
        if key == '':
            await bot.send(ev, '货币名称识别失败')
            return
        num = money.get_user_money(uid, 'kirastone')
        if num <= 0:
            await bot.send(ev, '羽毛石数量不足')
            return 
        nums, value = money.tran_kira(uid, key, num)
        await bot.send(ev, f'消耗{nums}羽毛石兑换{value}{key}成功')
        return
    elif len(arrs) == 2:
        key = money.translatename(arrs[0])
        if key == '':
            await bot.send(ev, '货币名称识别失败')
            return
        try:
            num = int(arrs[1])
            if num > money.get_user_money(uid, 'kirastone') or num <= 0:
                await bot.send(ev, '羽毛石数量不足')
                return
            nums, value = money.tran_kira(uid, key, num)
            await bot.send(ev, f'消耗{nums}羽毛石兑换{value}{key}成功')
            return
        except:
            await bot.send(ev, '货币数量识别失败')
            return
    else:
         return

@sv.on_prefix('维护补偿')
async def sys_compensate(bot, ev):
    uid = ev['user_id']
    string = ev.message.extract_plain_text().strip()
    arrs = string.split('/')
    if uid == your_uid: #修改为你的qq号  
        name = arrs[0]
        value = int(arrs[1])
        key = money.translatename(name)
        if money.increase_all_user_money(key, value):
            await bot.send(ev, '补偿下发成功', at_sender = True)
        else: 
            await bot.send(ev, '补偿下发失败', at_sender = True)
    else:
        return
        
@sv.on_fullmatch('asreload')
async def reload_card_(bot, ev):
    uid = ev['user_id'] 
    if uid == your_uid: #修改为你的qq号  
        if asgacha.reload_config():
            await bot.send(ev, 'reload success', at_sender = True)