from . import asgacha
import math, base64, os
from io import BytesIO
from .res import card_save
from PIL import Image, ImageFont, ImageDraw

def normalize_digit_format(n):
    return f'0{n}' if n < 10 else f'{n}'

def cid_list_remaker(cids_list):  #将卡片按角色排序
    cid_list = {}
    for cid in cids_list:
        cid_str = str(cid)
        keywords = f'{cid_str[1]}{cid_str[2]}{cid_str[3]}'
        if keywords not in cid_list.keys():
            cid_list[keywords] = []
        cid_list[keywords].append(cid)

    return cid_list

def img_maker_star(cid_list, cids_list, cards_num, COL_NUM = 18):
    row_nums = {}
    for star in cid_list.keys():
        row_nums[star] = math.ceil(len(cid_list[star]) / COL_NUM)
    row_num = sum(row_nums.values())
    base = Image.new("RGB",(40  + COL_NUM * 80 + (COL_NUM - 1) * 10, 
                            120 + row_num * 80 + (row_num - 1) * 10), (255, 255, 255))
    #base = base.resize((40 + COL_NUM * 80+(COL_NUM - 1) * 10, 120 +
                        #row_num * 80+(row_num - 1) * 10), Image.ANTIALIAS)
    row_index_offset = 0
    row_offset = 0
    for star in ['3','2','1']:
        cards_list = cid_list[star]
        for index, id in enumerate(cards_list):
            row_index = index // COL_NUM + row_index_offset
            col_index = index % COL_NUM
            card_id = cards_list[index]
            pic_path = asgacha.cid_to_path(card_id)
            f = asgacha.get_pic_ex(pic_path, cards_num[card_id], 80) if card_id in cards_num else asgacha.get_grey_pic(
                pic_path, 80)
            base.paste(f, (30 + col_index * 80 + (col_index - 1) * 10,
                           row_offset + 40 + row_index * 80 + (row_index - 1) * 10))
        row_index_offset += row_nums[star]
        row_offset += 30
    buf = BytesIO()
    base = base.convert('RGB')
    base.save(buf, format='JPEG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    return base64_str

def img_maker_chara(cids_list, cards_num, COL_NUM = 14):
    cid_list = cid_list_remaker(cids_list)
    row_nums = {}
    for chara in cid_list.keys():
        row_nums[chara] = math.ceil(len(cid_list[chara]) / COL_NUM)
    row_num = sum(row_nums.values())
    base = Image.new("RGB",(40  + COL_NUM * 80 + (COL_NUM - 1) * 10, 
                            10 * 40 + row_num * 80 + (row_num - 1) * 10), (255, 255, 255))
    #base = base.resize((40 + COL_NUM * 80+(COL_NUM - 1) * 10, 120 +
                        #row_num * 80+(row_num - 1) * 10), Image.ANTIALIAS)
    row_index_offset = 0
    row_offset = 0
    for chara in cid_list.keys():
        cards_list = cid_list[chara]
        for index, id in enumerate(cards_list):
            row_index = index // COL_NUM + row_index_offset
            col_index = index % COL_NUM
            card_id = cards_list[len(cards_list) - index - 1]
            pic_path = asgacha.cid_to_path(card_id)
            f = asgacha.get_pic_ex(pic_path, cards_num[card_id], 80) if card_id in cards_num else asgacha.get_grey_pic(
                pic_path, 80)
            base.paste(f, (30 + col_index * 80 + (col_index - 1) * 10,
                           row_offset + 40 + row_index * 80 + (row_index - 1) * 10))
        row_index_offset += row_nums[chara]
        row_offset += 10
    buf = BytesIO()
    base = base.convert('RGB')
    base.save(buf, format='JPEG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    return base64_str



def card_storage(uid, COL_NUM = 18, img_mode = 0):
    cid_list = asgacha.cid_list
    cids_list = asgacha.cids_list
    cards_num = card_save.db.get_cards_num(uid)
    cards_num = {card_id: card_amount for card_id,
                 card_amount in cards_num.items() if card_id in cids_list}
                 
    if not img_mode:
        base64_str = img_maker_star(cid_list, cids_list, cards_num, COL_NUM)
    else:
        base64_str = img_maker_chara(cids_list, cards_num)
    ranking = card_save.db.get_ranking(uid)
    ranking_desc = f'第{ranking}位' if ranking != -1 else '未上榜'
    total_card_num = sum(cards_num.values())
    super_rare_card_num = len(
        [card_id for card_id in cards_num if card_id > 3000000])
    super_rare_card_total = len(cid_list['3'])
    rare_card_num = len(
        [card_id for card_id in cards_num if card_id > 2000000 and card_id < 3000000])
    rare_card_total = len(cid_list['2'])
    normal_card_num = len(cards_num) - super_rare_card_num - rare_card_num
    normal_card_total = len(cid_list['1'])

    
    msg = f'''的仓库:[CQ:image,file={base64_str}]
持有卡片数: {total_card_num}
R卡收集: {normalize_digit_format(normal_card_num)}/{normalize_digit_format(normal_card_total)}
SR卡收集: {normalize_digit_format(rare_card_num)}/{normalize_digit_format(rare_card_total)}
UR卡收集: {normalize_digit_format(super_rare_card_num)}/{normalize_digit_format(super_rare_card_total)}
图鉴完成度: {normalize_digit_format(len(cards_num))}/{normalize_digit_format(len(cids_list))}
当前群排名: {ranking_desc}'''
    return msg

def get_my_rank(uid):
    ranking = card_save.db.get_ranking(uid)
    ranking_desc = f'第{ranking}位' if ranking != -1 else '未上榜'
    return ranking_desc

def card_search(name):
    member, team = gacha.change_name(name)
    if member == 0:
        return '角色昵称识别失败'
    chara = f'{team}{normalize_digit_format(member)}'
    cid_list = cid_list_remaker(asgacha.cids_list)
    fontpath = os.path.join(os.path.dirname(__file__), 'res/msyh.ttc')
    font = ImageFont.truetype(fontpath, 40)
    row_num = len(cid_list[chara])
    base = Image.new("RGB",(300, 
                            20 + row_num * 80 + (row_num - 1) * 10), (255, 255, 255))
    index = 0
    for cid in cid_list[chara]:
        _path = asgacha.cid_to_path(cid)
        icon = Image.open(_path)
        icon = icon.resize((80,80), Image.ANTIALIAS)
        base.paste(icon,(10, 90 * index + 10), icon)
        draw = ImageDraw.Draw(base)
        draw.text((100, 90 * index + 25),str(cid),font=font,fill=(0, 0, 0, 0))
        index += 1
    buf = BytesIO()
    base = base.convert('RGB')
    base.save(buf, format='JPEG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    return f'[CQ:image,file={base64_str}]'
