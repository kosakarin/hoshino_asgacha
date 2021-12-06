import os 
from PIL import Image
#这个是自动整理脚本，将新卡从wiki上下载下来后放到'./image/b/'中后
#去掉最下面函数的注释字符后直接运行此文件就可以直接梳理好所有的卡片 大约需要一分钟左右的时间
card_lsit = sorted((fn for fn in os.listdir(os.path.join(os.path.dirname(__file__), 'image/b/')) if fn.endswith('.png')))
_path_1 = os.path.join(os.path.dirname(__file__), 'image/icon/')
_path_2 = os.path.join(os.path.dirname(__file__), 'image/b/')

cards = {} #计数用

def add_cards(cid): #计数
    if cid not in cards:
        cards[cid] = {}
        cards[cid] = 1
    else:
        cards[cid] += 1
    return cards[cid]

def id_to_cid(_id):  #将wiki的卡片id转成我想要的卡片id
    cid = ''
    cid += _id[5]
    cid += str(int(_id[2]) + 1)
    cid += _id[3]+_id[4]
    nums = add_cards(int(cid + _id[10]))
    cid += str(nums) if nums >= 10 else f'0{nums}'
    cid += _id[10]
    return int(cid)
        

def mo(_id):  #自动转存
    cid = id_to_cid(_id)
    save_path = f'{_path_1}{_id[10]}/{str(cid)}.png'
    icon = Image.open(f'{_path_2}{_id}')
    icon.save(save_path)


#for card in card_lsit:
#    _id = str(card)
#    mo(_id)
#print('success')


