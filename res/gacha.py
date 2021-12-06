import os, random


_probal_list = []

def change_name(name):
    member_name_list = ['果', '绘', '鸟', '海', '凛', '姬', '希', '花', '妮',
                              '千', '梨', '南', '黛', '曜', '善', '丸', '鞠', '露',
                              '步梦', '霞', '雫', '果林', '爱', '彼方', '雪菜', '艾玛', '璃奈', '刊', '米娅', '岚珠']
    team_name_list = ['缪', '水', '虹']
    
    flag = {"flag":1, "team_temp":1, "member":0, "team":0}
    for team_name in team_name_list:
        if name == team_name:
            flag["team"] = flag["flag"]
            break
        flag["flag"] += 1
        
    if flag["team"] == 0:
        flag["flag"] = 1
        for member_name in member_name_list:
            if name == member_name:
                flag["member"] = flag["flag"]
                flag["team"] = flag["team_temp"]
                break
            flag["flag"] += 1
            if flag["flag"] > 9 and flag["team_temp"] != 3:
                flag["flag"] = 1
                flag["team_temp"] += 1
    return flag["member"], flag["team"]

def gacha_bd():  #十连保底 #十连时的第一抽 #返回卡片稀有度
    roll = random.random()
    if roll < _probal_list[0]:
        card_level = gacha_pup()
    else:
        card_level = 2

    return card_level
    
def gacha_pt():  #普通抽卡 #返回卡片稀有度
    roll = random.random()
    if roll < _probal_list[0]:
        card_level = gacha_pup()
    elif roll < _probal_list[1]:
        card_level = 2
    else:
        card_level = 1
        
    return card_level

def gacha_pup():  #出3星时判断是否为up 是up则返回4 否则返回3（歪了）#返回卡片稀有度
    roll = random.random()
    if roll < _probal_list[2] * _probal_list[3]:
        return 4
    elif roll < _probal_list[2]:
        return 5    #根据up数判断，如果双up，5就是up2，单up，5就视作3
    else:
        return 3
        
def random_give_level(times, ur_mode, probal_list):
    global _probal_list
    _probal_list = probal_list
    level_list = []
    if ur_mode:
        if times == 1:
            level_list.append([gacha_pup()])
        else:
            for i in range(times // 10):
                _level = []
                for ii in range(10):
                    _level.append(gacha_pup())
                level_list.append(_level)
    else:
        if times == 1:
            level_list.append([gacha_pt()])
        else:
            for i in range(times // 10):
                _level = []
                _level.append(gacha_bd())
                for ii in range(9):
                    _level.append(gacha_pt())
                level_list.append(_level)
    return level_list