import os
import json


config = {
    "default": {
        "gold" : 0,
        "lovecastone": 0,
        "starstone": 12500,
        "kirastone": 0,
        "last_login": 0,
    }
}

keyword_list = [
    "gold",
    "lovecastone",
    "starstone",
    "kirastone",
    "last_login"
]


user_money = {}

def get_config(key, sub_key):
    if key in config and sub_key in config[key]:
        return config[key][sub_key]
    return None


def load_user_money():
    path = os.path.join(os.path.dirname(__file__), 'user_money.json')
    if not os.path.exists(path):
        return
    try:
        with open(path, encoding='utf8') as f:
            d = json.load(f)
            for k,v in d.items():
                user_money[k] = v
    except:
        print("error")
load_user_money()

def get_user_money(user_id, key):
    user_id = str(user_id)
    if user_id not in user_money:
        user_money[user_id] = {}
        for k, v in config['default'].items():
            user_money[user_id][k] = v
    if key in user_money[user_id]:
        return user_money[user_id][key]
    else:
        return None

def set_user_money(user_id, key, value):
    user_id = str(user_id)
    if user_id not in user_money:
        user_money[user_id] = {}
        for k, v in config['default'].items():
            user_money[user_id][k] = v
    user_money[user_id][key] = value
    path = os.path.join(os.path.dirname(__file__), 'user_money.json')
    try:
        with open(path, 'w', encoding='utf8') as f:
            json.dump(user_money, f, ensure_ascii=False, indent=2)
    except:
        print("error")
        
        
        
def increase_user_money(user_id, key, value):
    user_id = str(user_id)
    if user_id not in user_money:
        user_money[user_id] = {}
        for k, v in config['default'].items():
            user_money[user_id][k] = v
    now_money = int(get_user_money(user_id, key)) + value
    
    user_money[user_id][key] = now_money 
    path = os.path.join(os.path.dirname(__file__), 'user_money.json')
    try:
        with open(path, 'w', encoding='utf8') as f:
            json.dump(user_money, f, ensure_ascii=False, indent=2)
    except:
        print("error")
        
        
def reduce_user_money(user_id, key, value):
    user_id = str(user_id)
    if user_id not in user_money:
        user_money[user_id] = {}
        for k, v in config['default'].items():
            user_money[user_id][k] = v
    now_money = int(get_user_money(user_id, key)) - value
    
    user_money[user_id][key] = now_money 
    path = os.path.join(os.path.dirname(__file__), 'user_money.json')
    try:
        with open(path, 'w', encoding='utf8') as f:
            json.dump(user_money, f, ensure_ascii=False, indent=2)
    except:
        print("error")