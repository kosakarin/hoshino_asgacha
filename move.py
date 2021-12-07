'''
import os, json
from PIL import Image
#这个是自动整理脚本，将新卡从wiki上下载下来后放到'./image/b/'中后
#去掉最上面的注释字符后直接运行此文件就可以直接梳理好所有的卡片 大约需要一分钟左右的时间
#梳理完成后的操作正在改善，目前需要你手动打开'card.text'文件去将里面的cid写入config.json里，正在思考算法使其更完善（主要是怎么自动获得当前up卡）
json_list_path = os.path.join(os.path.dirname(__file__), 'image/icon_list.json')
config_path = os.path.join(os.path.dirname(__file__), 'config/config.json')
card_lsit = sorted((fn for fn in os.listdir(os.path.join(os.path.dirname(__file__), 'image/b/')) if fn.endswith('.png')))
cid_list = sorted((fn for fn in os.listdir(os.path.join(os.path.dirname(__file__), 'image/icon/1/')) if fn.endswith('.png')))
cid_list_2 = sorted((fn for fn in os.listdir(os.path.join(os.path.dirname(__file__), 'image/icon/2/')) if fn.endswith('.png')))
_path_1 = os.path.join(os.path.dirname(__file__), 'image/icon/')
_path_2 = os.path.join(os.path.dirname(__file__), 'image/b/')

_cid = []
cards = {} #计数用

for i in cid_list_2:
    cid_list.append(i)

def get_new_card_id():
    new_card_list = []
    with open(json_list_path, encoding='utf8') as f:
        _card_list = json.load(f)
    for card in card_lsit:
        if card not in _card_list:
            new_card_list.append(card)
    return new_card_list

def save_new_card():
    with open(json_list_path, 'w', encoding='utf8') as f:
        json.dump(card_lsit, f, ensure_ascii=False, indent=2)


def get_new_cid():
    new_cid_list = []
    for cid in _cid:
        if f'{cid}.png' not in cid_list:
            new_cid_list.append(cid)

    return new_cid_list


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
    int_cid = int(cid)
    _cid.append(int_cid)
    
        

def mo(_id, cid):  #自动转存
    str_cid = str(cid)
    if f'{_id[5]}{int(_id[2])+1}{_id[3]}{_id[4]}' == f'{str_cid[0]}{str_cid[1]}{str_cid[2]}{str_cid[3]}': #防止弄错
        save_path = f'{_path_1}{_id[10]}/{str(cid)}.png'
        icon = Image.open(f'{_path_2}{_id}')
        icon.save(save_path)
        return 1
    else:
        return 0


for card in card_lsit:
    _id = str(card)
    id_to_cid(_id)

new_card_list = get_new_card_id()
new_cid_list = get_new_cid()
print(f'{new_card_list}\n{new_cid_list}')
index = 0
for card in new_card_list:
    if mo(card, new_cid_list[index]):
        index += 1
    else:
        break
else:
    with open('./card.txt', mode='w') as f:
        f.write(str(new_card_list))
        f.write(str(new_cid_list))
    save_new_card()
    print('success')

'''
