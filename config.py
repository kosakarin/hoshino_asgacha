import os
import json


config = {
    "default": { #默认参数 无需修改
        "up_num": 2,
        "up_card1": "【気を抜くと眠っちゃいそう】朝香果林！",
        "up_card2": "【一緒に漫画タイムにしようよ～】高坂穗乃果！",
        "up1_team": 3,
        "up2_team": 1,
        "up1_mem": 4,
        "up2_mem": 1,
        "gacha_cost": 50,
    }
}

group_config = {}

def get_config(key, sub_key):
    if key in config and sub_key in config[key]:
        return config[key][sub_key]
    return None



def load_group_config():
    path = os.path.join(os.path.dirname(__file__), 'config.json')
    if not os.path.exists(path):
        return
    try:
        with open(path, encoding='utf8') as f:
            d = json.load(f)
            for k,v in d.items():
                group_config[k] = v
    except:
        print("error")
load_group_config()

def get_group_config(key):
    default = "default"
    if default not in group_config:
        group_config[default] = {}
        for k, v in config['default'].items():
            group_config[default][k] = v
    if key in group_config[default]:
        return group_config[default][key]
    else:
        return None

def set_group_config(key, value):
    default = "default"
    if default not in group_config:
        group_config[default] = {}
        for k, v in config['default'].items():
            group_config[default][k] = v
    group_config[default][key] = value
    path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(path, 'w', encoding='utf8') as f:
            json.dump(group_config, f, ensure_ascii=False, indent=2)
    except:
        print("error")