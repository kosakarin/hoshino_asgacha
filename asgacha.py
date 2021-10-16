import os, random



#图片保存位置 C:\/Users/Administrator/Desktop/XCW/res/img/image/icon_r 保留res/img/后面的即可(因为一开始是打算调用R.img来发图的，后来换了，就没动这里)
r_path = 'image/icon_r/'
sr_path = 'image/icon_sr/'
ur_path = 'image/icon_ur/'

base_path = 'C:\/Users/Administrator/Desktop/XCW/res/img/'


def con_num(path):
    count = 0
    for file in os.listdir(path): #file 表示的是文件名
            count = count+1
    return count
    
#为了便于后续修改
r_num = con_num(base_path + r_path)     #69      #库存R卡数量
sr_num = con_num(base_path + sr_path)   #245     #库存sr卡数量
ur_num = con_num(base_path + ur_path)   #236+1   #库存UR数量(单up模式保留pick_up2.png)

ur_prob = 0.05   #单次抽卡ur爆率为5%
sr_prob = 0.15   #单次抽卡sr爆率为15%
up_prob = 0.2    #当抽出ur时这张卡有10%概率为up卡     (单up时填双倍概率)
up_prob_ = 0.5   #当抽出up时这张卡有50%概率为pick_up1 (单up时填0.5)




 #用于v2.0的随机给卡函数 如果没有更好的就暂定用这个
def random_give_card(card_level:int, member:int, team:int) -> str:
    _path = ''
    
    if card_level >= 3:
        _path += ur_path 
    elif card_level == 2:
        _path += sr_path
    else:
        _path += r_path
        
    if card_level >= 4 and member == 0 and team == 0:
        if card_level == 4:
            _path += 'pick_up1.png'
        else:
            _path += 'pick_up2.png'
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
        if card_num > 1:
            _path += str(random.randint(1, card_num)) + '.png'
        elif card_num == 1:
            _path += '1.png'
    
    return _path    

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
        flag += 1
        
    if team_re == 0:
        flag = 1
        for member_name in member_name_list:
            if name == member_name:
                member_re = flag
                team_re = team_flag
            flag += 1
            if flag > 9 and team_flag != 3:
                flag = 1
                team_flag += 1
    return member_re, team_re
 
            
    
