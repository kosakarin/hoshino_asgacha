# hoshino_asgacha
hoshinobot的llas抽卡模拟器v4.0

# git这个网页管理真反人类 搞得我想删仓跑路了（

# 使用方法
 把image.zip解压后放到\image  下
 
 在__bot__.py内添加 'asgacha'
 
 现在路径应该都是绝对位置了，而且不需要修改啥了


# 更新记录

## 先重写了一点点代码 把重写的传上来了

大概重写了以下东西：

1.重新设计抽卡的相关算法；

2.内置随机唐可可

3.仓库查看支持两种查看模式

4.签到支持连续登录

5.新的资源请移步网盘下载https://pan.baidu.com/s/1enRtK-CKlQsqcTReCLwMLQ 提取码:23yr

## 计划重新设计重写抽卡模拟器部分代码 预计明年2月前重写完成（

## v3.1

重写了下加成计算器那块的东西，支持了下加成控分，不过具体数值还有待验证，建议先别用等下次storyevent我去验证一下顺便改改公式

## v3.0 

终于稍微弄懂数据库了；

1.新增仓库功能，现在将会使用一个数据库存储大家有什么卡了（参考了https://github.com/GWYOG/GWYOG-Hoshino-plugins#8-%E6%88%B3%E6%9C%BA%E5%99%A8%E4%BA%BA%E9%9B%86%E5%8D%A1%E5%B0%8F%E6%B8%B8%E6%88%8Fpokemanpcr  的相关代码）；

2.新增货币系统，利用一个json文件存储当前你的货币，目前定义了4种货币（实际只有一种货币有用其他都只是看着好看）；

3.新增现场设置功能，可以直接通过指令不重启bot设置卡池的一些参数了；

## v2.1.1 完善控分计算器计算算法

1.完善控分计算器计算算法，现在会优先选择S评价再选择A评价了；

2.控分计算器提供模式选择参数，在命令最后加入相关参数可以控制计算器使用哪些关卡，目前支持模式：0或不提供:默认  1:仅S  2:无剧情关卡 3:无剧情关卡且仅S

命令举例：as控分 114514 1919810 2

as控分 114514 1

as控分 114514 1919810

as控分 114514

## v2.1 更新as签到功能，as控分计算器功能！

感谢@比那名居的桃子 提供的控分算法

## v2.0 支持单人卡池抽取！
1.重做抽取函数，支持单人卡池；

2.完善了UR抽卡判断，UR抽卡和普通抽卡合并为同一个函数；

3.为了支持单人卡池抽取重新规划了icon存储路径；

4.单人卡池暂时支持的角色昵称如下：

果 绘 鸟 海 凛 姬 希 花 妮   千 梨 南 黛 曜 善 丸 鞠 露   步梦 霞 雫 果林 爱 彼方 雪菜 艾玛 璃奈 栞 米娅 岚珠

团体名称：缪 水 虹

暂不支持小队招募

## v1.1

1.将几个参数修改为变量，便于后续修改；

2.将随机发送图片的范围由手动填写改为自动扫描目录下文件数量；

3.新增up_num参数用于控制当前是双up模式还是单up模式；

4.更新了几张新卡的icon；

5.更新了ur单抽和ur十连命令，暂定可以出up；

## v1.0

asgacha初次上线
