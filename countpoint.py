import json,os

def solve(songs, pt:int):
    #print(pt)
    res = []
    visited = [False] * (pt + 10)
    mp = [{} for i in range(pt + 10)]
    visited[0] = True
    for i in songs:
        if i > pt:
            continue
        for j in range(pt - i + 1):
            if not visited[j]:
                continue
            if visited[j + i]:
                continue
            visited[j + i]=True
            for k in mp[j]:
                mp[j + i][k]=mp[j][k]
            if mp[j + i].get(i) == None:
                mp[j + i][i] = 1
            else:
                mp[j + i][i] += 1
    return mp[pt]

def chose_list(mod:int):
    with open(os.path.join(os.path.dirname(__file__), 'points.json'), "r", encoding='utf8') as f: 
        points = json.load(f)   
    _list = {"point":[],"name":[]}
    if mod == 1:
        for i in points:
            if i["rank"] == 'S':
                _list["point"].append(i["point"])
                _list["name"].append(i["name"] + i["rank"])
        string = '当前为仅S模式'
    elif mod == 2:
        for i in points:
            if i["lpcost"] in [10,12,15,20]:
                _list["point"].append(i["point"])
                _list["name"].append(i["name"] + i["rank"])
        string =  '当前为无剧情关卡模式'
    elif mod == 3:
        for i in points:
            if i["lpcost"] in [10,12,15,20] and i["rank"] == 'S':
                _list["point"].append(i["point"])
                _list["name"].append(i["name"] + i["rank"])
        string ='当前为无剧情关卡仅S模式'
    else:
        for i in points:
            _list["point"].append(i["point"])
            _list["name"].append(i["name"] + i["rank"])
        string ='未提供模式参数或模式参数识别失败，使用默认模式'

    return _list, string

def tran(__song, _list, i):
    temp = 0
    for a in __song:
        if a == i:
            return _list["name"][temp]
        temp += 1

def count_point(target:int, x:int, mod:int, _up:int) -> str:
    target -= x
    p = target
    cnt = 0
    msg = ''
    __song = []
    res_list = []
    _list, mod_str = chose_list(mod)
    for i in range(0, len(_list["point"])):
        __song.append(int(_list["point"][i] * (_up / 100 + 1)))
    if target >= 50000:
        cnt = (target - 49000)//__song[0]
        target -= cnt * __song[0]
    res = solve(__song, target)
    msg += f'还需要获得{str(p)}pt,我们采用以下方案：\n注:以下结果为{_up}%加成结果\n{mod_str}\n使用币值为：{__song}\n'
    if len(res) == 0:
        msg += '无解'
        return msg
    for i in res:
        if i == __song[0]:
            res[i] += cnt
        msg += f'\n游玩{res[i]}次{tran(__song, _list, i)}，每次获得{str(i)}pt，共获得{str(i * res[i])}pt'
        res_list.append(i * res[i])
    temp = 0
    for i in res_list:
        temp += i
    msg += f'\n反算获得pt为：{temp}'

    return msg
