import os, random
from .config import get_config, get_group_config


#图片保存位置 C:\/Users/Administrator/Desktop/XCW/res/img/image/icon_r 保留res/img/后面的即可(因为一开始是打算调用R.img来发图的，后来换了，就没动这里)
r_path = 'image/icon_r/'
r_path_2 = 'image/icon_r_2/'
sr_path = 'image/icon_sr/'
sr_path_2 = 'image/icon_sr_2/'
ur_path = 'image/icon_ur/'
ur_path_2 = 'image/icon_ur_2/'

base_path = 'C:\/Users/Administrator/Desktop/XCW/res/img/'


def con_num(path):
    count = 0
    for file in os.listdir(path): #file 表示的是文件名
            count = count+1
    return count
    


ur_prob = 0.05   #单次抽卡ur爆率为5%
sr_prob = 0.15   #单次抽卡sr爆率为15%
up_prob = 0.2    #当抽出ur时这张卡有10%概率为up卡     (单up时填双倍概率)
up_prob_ = 0.5   #当抽出up时这张卡有50%概率为pick_up1 (单up时填0.5)

def get_cid(card_level, team, member, temp): #CID合成 目前采用 [稀有度] 1 [团体号] 1 [角色编号] 2 [卡片编号] 2 [觉醒标记] 1 规则来合成7位cid
    card_level = card_level if card_level <= 3 else 3
    if member > 9 and temp > 9:
        cid = int(f'{card_level}{team}{member}{temp}1') 
    elif member > 9:
        cid = int(f'{card_level}{team}{member}0{temp}1')
    elif temp > 9:
        cid = int(f'{card_level}{team}0{member}{temp}1')
    else:
        cid = int(f'{card_level}{team}0{member}0{temp}1')
    return cid

def cid_to_path(cid): #3 2 01 01 1 #给定cid 返回对应的路径
    _path = ''
    cid_str = str(cid)
    card_level = int(cid_str[0])
    team = cid_str[1]
    member = cid_str[3] if cid_str[2] == '0' else (cid_str[2] + cid_str[3])
    temp = cid_str[5] if cid_str[4] == '0' else (cid_str[4] + cid_str[5])
    if card_level >= 3:
        _path += ur_path 
    elif card_level == 2:
        _path += sr_path
    else:
        _path += r_path
    _path += f'{team}/{member}/{temp}.png'
    return _path
    

 #用于v2.0的随机给卡函数 如果没有更好的就暂定用这个
def random_give_card(card_level:int, member:int, team:int):
    up1_team = get_group_config("up1_team")
    up1_mem = get_group_config("up1_mem")
    up2_team = get_group_config("up2_team")
    up2_mem = get_group_config("up2_mem")
    _path = ''
    mode_flag = 0
    if member == 0 and team == 0:
        mode_flag = 1
    
    if card_level >= 3:
        _path += ur_path 
    elif card_level == 2:
        _path += sr_path
    else:
        _path += r_path
        
    if card_level >= 4 and mode_flag == 1:
        if card_level == 4:
            _path += f'{up1_team}/{up1_mem}/'
            temp = con_num(base_path + _path)
            _path += f'{str(temp)}.png'
            cid = get_cid(3, up1_team, up1_mem, temp)
        elif up2_mem != 0 and up2_team != 0:
            _path += f'{up2_team}/{up2_mem}/'
            temp = con_num(base_path + _path)
            _path += f'{str(temp)}.png'
            cid = get_cid(3, up2_team, up2_mem, temp)
    else:
        if team == 0:
            team = random.randint(1, 3)
        if member == 0:
            if team == 3:
                member = random.randint(1, 10)
            else:
                member = random.randint(1, 9)
    
        _path += str(team) + '/' +  str(member) + '/'
        
        card_num = con_num(base_path + _path)
        if team == up1_team and member == up1_mem and mode_flag == 1:    
            temp = random.randint(1, card_num - 1)
            _path += str(temp) + '.png'
        elif team == up2_team and member == up2_mem and mode_flag == 1:  
            temp = random.randint(1, card_num - 1)        
            _path += str(temp) + '.png'
        elif card_num > 1:
            temp = random.randint(1, card_num)
            _path += str(temp) + '.png'
        elif card_num == 1:
            temp = 1
            _path += '1.png'
        cid = get_cid(card_level, team, member, temp)
    
    return _path, cid


def gacha_bd(up_num:int) -> int:  #十连保底 #十连时的第一抽 #返回卡片稀有度
    roll = random.random()
    if roll < ur_prob:
        card_level = gacha_pup(up_num)
    else:
        card_level = 2

    return card_level
    
def gacha_pt(up_num:int) -> int:  #普通抽卡 #返回卡片稀有度
    roll = random.random()
    if roll < ur_prob:
        card_level = gacha_pup(up_num)
    elif roll < sr_prob:
        card_level = 2
    else:
        card_level = 1
        
    return card_level

def gacha_pup(up_num:int) -> int:  #出3星时判断是否为up 是up则返回4 否则返回3（歪了）#返回卡片稀有度
    roll = random.random()
    if up_num == 2:
        if roll < up_prob * up_prob_:
            return 4
        elif roll < up_prob:
            return 5
        else:
            return 3
    elif up_num == 1:
        if roll < up_prob * up_prob_:
            return 4
        else:
            return 3
    elif up_num == 0:
        return 3
        
 #v2.0的名称转化函数
def change_name(name:str) -> int:
    member_name_list = ['果', '绘', '鸟', '海', '凛', '姬', '希', '花', '妮',
                              '千', '梨', '南', '黛', '曜', '善', '丸', '鞠', '露',
                              '步梦', '霞', '雫', '果林', '爱', '彼方', '雪菜', '艾玛', '璃奈', '刊', '米娅', '岚珠']
    team_name_list = ['缪', '水', '虹']
    
    flag = 1
    team_flag = 1
    member_re = 0
    team_re = 0
    for team_name in team_name_list:
        if name == team_name:
            team_re = flag
            break
        flag += 1
        
    if team_re == 0:
        flag = 1
        for member_name in member_name_list:
            if name == member_name:
                member_re = flag
                team_re = team_flag
                break
            flag += 1
            if flag > 9 and team_flag != 3:
                flag = 1
                team_flag += 1
    return member_re, team_re
 
            

def give_card(card_level:int, member:int, team:int) -> str:
    _path = ''
    _path_2 = ''
    
    if card_level >= 3:
        _path += ur_path 
        _path_2 += ur_path_2
    elif card_level == 2:
        _path += sr_path
        _path_2 += sr_path_2
    else:
        _path += r_path
        _path_2 += r_path_2
    _path += str(team) + '/' +  str(member) + '/'
    _path_2 += str(team) + '/' +  str(member) + '/'
    card_num = con_num(base_path + _path)
    return _path, _path_2, card_num
