

songs = [
    875,  #20LP S 
    860,  #20LP A
    640,  #16LP S
    620,  #16LP Aoi
    600,  #15LP S
    581,  #15LP A
    438,  #13LP S
    422,  #13LP A
    405,  #12LP S
    390,  #12LP A
    275,  #10LP S 
    262,  #10LP A 
    247,  #9LP S
    236   #9LP A
]


songs_list = [
    '上+ S',
    '上+ A',
    '16LP剧情关 S',
    '16LP剧情关 A',
    '上级 S',
    '上级 A',
    '13LP剧情关 S',
    '13LP剧情关 A',
    '中级 S',
    '中级 A',
    '初级 S',
    '初级 A',
    '9LP剧情关 S',
    '9LP剧情关 A'

]

def solve(songs,pt:int):
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
            if mp[j + i].get(i)==None:
                mp[j + i][i]=1
            else:
                mp[j + i][i]+=1
    return mp[pt]

def tran(i:int) -> str:
    temp = 0
    for song in songs:
        if i == song:
            return songs_list[temp]
        temp += 1

def count_point(target:int, x:int) -> str:
    target -= x
    p = target
    cnt = 0
    msg = ''
    if target >= 50000:
        cnt = (target - 49000)//875
        target -= cnt * 875
    res = solve(songs, target)
    msg += f'还需要获得{str(p)}pt,我们采用以下方案：\n注:以下结果为0%加成结果\n'
    if len(res) == 0:
        msg += '无解'
        return msg
    for i in res:
        if i == 875:
            res[i] += cnt
        msg += f'\n游玩{res[i]}次'
        msg += tran(i)
        msg += f'，每次获得{str(i)}pt，共获得{str(i*res[i])}pt'
        
    return msg
