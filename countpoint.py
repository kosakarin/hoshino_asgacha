
#默认
songs = [
    875, 640, 600, 438, 405, 275,  247,  #S
    860, 620, 581, 422, 390, 262,  236   #A
]
songs_list = [
    '上+ S', '16LP剧情关 S', '上级 S', '13LP剧情关 S', '中级 S', '初级 S', '9LP剧情关 S',
    '上+ A', '16LP剧情关 A', '上级 A', '13LP剧情关 A', '中级 A', '初级 A', '9LP剧情关 A'
]
#无剧情关
songs_normal = [
    875, 600, 405, 275,  #S
    860, 581, 390, 262   #A
]
songs_list_normal = [
    '上+ S', '上级 S', '中级 S', '初级 S',
    '上+ A', '上级 A', '中级 A', '初级 A'
]
#无A
songs_S = [
    875, 640, 600, 438, 405, 275,  247  #S
]
songs_list_S = [
    '上+ S', '16LP剧情关 S', '上级 S', '13LP剧情关 S', '中级 S', '初级 S', '9LP剧情关 S'
]
#无剧情关且全S
songs_normal_S = [
    875, 600, 405, 275
]
songs_list_normal_S = [
    '上+ S', '上级 S', '中级 S', '初级 S'
]

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
    if mod == 1:
        return songs_S, songs_list_S, '当前为仅S模式'
    elif mod == 2:
        return songs_normal, songs_list_normal, '当前为无剧情关卡模式'
    elif mod == 3:
        return songs_normal_S, songs_list_normal_S, '当前为无剧情关卡仅S模式'
    else:
        return songs, songs_list, '未提供模式参数或模式参数识别失败，使用默认模式'

def tran(_songs, _songs_list, i:int) -> str:
    temp = 0
    for song in _songs:
        if i == song:
            return _songs_list[temp]
        temp += 1

def count_point(target:int, x:int, mod) -> str:
    target -= x
    p = target
    cnt = 0
    msg = ''
    _songs, _songs_list, mod_str = chose_list(mod)
    if target >= 50000:
        cnt = (target - 49000)//875
        target -= cnt * 875
    res = solve(_songs, target)
    msg += f'还需要获得{str(p)}pt,我们采用以下方案：\n注:以下结果为0%加成结果\n{mod_str}\n'
    if len(res) == 0:
        msg += '无解'
        return msg
    for i in res:
        if i == 875:
            res[i] += cnt
        msg += f'\n游玩{res[i]}次{tran(_songs, _songs_list, i)}，每次获得{str(i)}pt，共获得{str(i * res[i])}pt'
  
    return msg
