import jiagu

# 吻别是由张学友演唱的一首歌曲。
# 《盗墓笔记》是2014年欢瑞世纪影视传媒股份有限公司出品的一部网络季播剧，改编自南派三叔所著的同名小说，由郑保瑞和罗永昌联合导演，李易峰、杨洋、唐嫣、刘天佐、张智尧、魏巍等主演。

for n in range(5):
    print(n)

text = '清代时，某人养了一只八哥，教它说话，驯养得很灵巧。这人很喜欢这只八哥，连出门都和它形影不离，就这样过了好几年。'

print(text)

knowledge = jiagu.knowledge(text)
print(knowledge)

di = {'a':{'b':'c'}}

print(di)
print(type(di))

a = '0.1'
print(float(a))