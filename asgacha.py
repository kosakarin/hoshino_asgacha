import os, random



#图片保存位置
r_path = 'image/icon_r/'
sr_path = 'image/icon_sr/'
ur_path = 'image/icon_ur/'




def con_num(path):
    count = 0
    for file in os.listdir(path): #file 表示的是文件名
            count = count+1
    return count
    
#为了便于后续修改
r_num = con_num('C:\/Users/Administrator/Desktop/XCW/res/img/image/icon_r')     #69      #库存R卡数量
sr_num = con_num('C:\/Users/Administrator/Desktop/XCW/res/img/image/icon_sr')   #245     #库存sr卡数量
ur_num = con_num('C:\/Users/Administrator/Desktop/XCW/res/img/image/icon_ur')   #236+1   #库存UR数量(单up模式保留pick_up2.png)

ur_prob = 0.05   #单次抽卡ur爆率为5%
sr_prob = 0.15   #单次抽卡sr爆率为15%
up_prob = 0.2    #当抽出ur时这张卡有10%概率为up卡     (单up时填双倍概率)
up_prob_ = 0.5   #当抽出up时这张卡有50%概率为pick_up1 (单up时填0.5)




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
        img_id = str(random.randint(1, ur_num - 2)) + '.png'
        _path = ur_path
    elif card_level == 2:
        img_id = str(random.randint(1, sr_num)) + '.png'
        _path = sr_path
    else:
        img_id = str(random.randint(1, r_num)) + '.png'
        _path = r_path
        
        
    _path += img_id
    return _path
        

    

def gacha_bd(up_num):  #十连保底 #十连时的第一抽 #返回卡片稀有度
    roll = random.random()
    if roll < ur_prob:
        card_level = gacha_pup(up_num)
    else:
        card_level = 2

    return card_level
    
def gacha_pt(up_num):  #普通抽卡 #返回卡片稀有度
    roll = random.random()
    if roll < ur_prob:
        card_level = gacha_pup(up_num)
    elif roll < sr_prob:
        card_level = 2
    else:
        card_level = 1
        
    return card_level

def gacha_pup(up_num):  #出3星时判断是否为up 是up则返回4 否则返回3（歪了）#返回卡片稀有度
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
        

