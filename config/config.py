import os
import json

#此文件用于修改和读取config.json文件，其中可用api为：
#load_config() return 1: success  0: fail             加载设置
#get_config(key) return int or str or None            获取某项设置，key为要获取的值名称
#set_config(key, value) return 1: success  0: fail    设置某个参数的值为value
#也可以直接到config.json中手动修改相关值，修改后调用load_config()即可重新读取（重启或你自己想办法都可以）


config = {
    "default": { #默认参数 无需修改
        "num": 2,  #当前几张up卡
        "name1": "【厳しくチェックしてくださいね！】优木雪菜",  #卡片名称
        "name2": "【おかしいな、違うのかな……】近江彼方",  #卡片名称
        "up1": 3307081,  #卡片cid
        "up2": 3306081,  #卡片cid
        "cost": 50,  #单次抽卡耗费
    }
}

keyword_list = [                 #避免错误设置
    "num",
    "name1",
    "name2",
    "up1",
    "up2",
    "cost"
]

group_config = {}

def load_config():
    global group_config
    try:
        path = os.path.join(os.path.dirname(__file__), 'config.json')
        if not os.path.exists(path):
            return 0
        with open(path, encoding='utf8') as f:
            d = json.load(f)
            for k,v in d.items():
                group_config[k] = v
            return 1
    except:
        return 0
load_config()

def get_config(key):
    try:
        if key not in keyword_list:
            return None        
        default = "default"
        if default not in group_config:
            group_config[default] = {}
            for k, v in config['default'].items():
                group_config[default][k] = v
        if key in group_config[default]:
            return group_config[default][key]
        else:
            return None
    except:
        return None

def set_config(key, value):
    try:
        if key not in keyword_list:
            return 0
        default = "default"
        if default not in group_config:
            group_config[default] = {}
            for k, v in config['default'].items():
                group_config[default][k] = v
        group_config[default][key] = value
        path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(path, 'w', encoding='utf8') as f:
            json.dump(group_config, f, ensure_ascii=False, indent=2)
        return 1
    except:
        return 0