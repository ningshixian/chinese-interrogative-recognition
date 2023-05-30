
# import paddlehub as hub

# print("装载LAC模型...")
# lac = hub.Module(name="lac")

# inputs = (
#     {"text": ["苹果甜不甜？"]}
# )
# # IndexError: string index out of range 未解决
# results = lac.lexical_analysis(data=inputs)  # → {'word': [], 'tag': []}
# print(results)


import re

special_token = "到底、多会儿、多會兒、多久、多少、反倒、干吗、干嘛、干什么、幹嗎、幹嘛、幹什麼、何、何来、何时、何時、何为、何為、何用、何在、几时、幾時、究竞、可好、毛线、毛線、莫非、哪、哪儿、哪兒、哪个、哪個、哪会儿、哪會兒、哪里、哪裡、哪些、哪种、哪種、难道、难怪、難谊、難怪、岂、豈、州街、啥、哈 时候、啥時候、什么、什麼、神马、神馬、孰是孰非、谁、誰、为何、为毛、为啥、为什么、為何、為毛、為啥、為什麼、要不、有何、有木有、怎、怎的、怎地、怎会、怎會、怎么、怎么办、怎么回事、 怎么弄、怎么样、怎么着、怎么做、怎麼、怎麼辦、怎麼回事、怎麼弄、怎麼樣、怎麼著、怎麼做、怎样、怎樣、知否、肿么"
special_token = special_token.split("、")
special_token = "|".join(special_token)


def func(text, special_token):
    res = []
    
    # 正反问句 pos_and_neg√
    pn_pattern1 = re.compile(r".*(.{1})不(.{1}).*")
    pn_pattern2 = re.compile(r".*(.{2})不(.{2}).*")
    m1 = pn_pattern1.match(text)
    m2 = pn_pattern2.match(text)
    if (m1 and m1.group(1)==m1.group(2)) or (m2 and m2.group(1)==m2.group(2)):
        res.append("正反问句")

    # 选择问句 choice√
    c_pattern = re.compile(r".*是?.*还是.*")
    m = c_pattern.match(text)
    if m:
        res.append("选择问句")

    # 是非问句 whether×
    w_pattern1 = re.compile(r"(.*[吗么]$|.*[吗么][，。？]{1,3}$)")
    w_pattern2 = re.compile(r"(.*[啊吧]$|.*[啊吧][？]$)")
    m1 = w_pattern1.match(text)
    m2 = w_pattern2.match(text)
    if (m1) or (m2):
        res.append("是非问句")

    # 特指问句 special√
    s_pattern = re.compile(r".*" + "(" + special_token + ")" + r".*" + r"[啊吧呢么啦]?[？]?$")
    m = s_pattern.match(text)
    if m:
        res.append("特指问句")

    return res


if __name__ == "__main__":

    for text in [
        "不能直接退吗", 
        "显示报名成功就行了，对吧？", 
        "上面显示要给工作人员签到", 
        "500。  1000龙珠",
        "你这边后台把90天冷静期给我去掉，可以吗", 
        "内部员工，把90天冷静期给我取消就行", 
        "没有注销呀", 
        "不签到坐等发货就可以了吗？", 
        "15天之类发货", 
        "只要报名成功就可以了吗？需要签到吗？", 
        "哦哦，那好的，不需要签到吗", 
        "就是报名成功就可以吗", 
        "我应该是新用户", 
        "我每天签到，现在才又攒了七个", 
        "哦哦，那估计是账号没切换", 
        "这个是报名成功了就有是吧", 
        "话题赚龙珠获得的", 
        "报名成功，就等快递嘛？", 
        "报名成功  就可以了么", 
        "中石油", 
        "……是云闪付付的啊", 
        "什么是龙珠成长值", 
        "发什么快递呢", 
        "发什么快递呢？", 
    ]:
        print(func(text, special_token), text)


