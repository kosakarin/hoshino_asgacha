import os, random




#图片保存位置
r_path = 'image/icon_r/'
sr_path = 'image/icon_sr/'
ur_path = 'image/icon_ur/'



def random_give_card(card_level):  #根据卡牌稀有度随机抽取一张卡的icon，返回icon的路径
    flag = 1
     
    img_id = ''
    if card_level == 4:
        img_id = 'pick_up1.png'
        _path = ur_path 
    elif card_level == 5:
        img_id = 'pick_up2.png'
        _path = ur_path 
    elif card_level == 3:
        img_id = str(random.randint(1,233)) + '.png'
        _path = ur_path
    elif card_level == 2:
        img_id = str(random.randint(1,243)) + '.png'
        _path = sr_path
    else:
        img_id = str(random.randint(1,69)) + '.png'
        _path = r_path
        
        
    _path += img_id
    return _path
        
        
    

def gacha_bd():  #十连保底 #十连时的第一抽 #返回卡片稀有度
    roll = random.random()
    if roll < 0.05:
        card_level = gacha_pup()
    else:
        card_level = 2

    return card_level
    
def gacha_pt():  #普通抽卡 #返回卡片稀有度
    roll = random.random()
    if roll < 0.05:
        card_level = gacha_pup()
    elif roll < 0.2:
        card_level = 2
    else:
        card_level = 1
        
    return card_level

def gacha_pup():  #出3星时判断是否为up 是up则返回4 否则返回3（歪了）#返回卡片稀有度
    roll = random.random()
    if roll < 0.1:
        return 4
    elif roll < 0.2:
        return 5
    else:
        return 3
        

