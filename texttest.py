from docarray import Document, DocumentArray
from tqdm import tqdm
from text2vec import SentenceModel, EncoderType
import numpy as np
from pprint import pprint
#import os
#text2vec在调用模型时要访问huggingface.co，如网络质量不好会导致无法调用模型，此次请想办法科学上网
#os.environ["http_proxy"] = "http://ip:port"
#os.environ["https_proxy"] = "http://ip:port"

with open('./1.txt', encoding='utf-8') as f:
    txt = f.read()
d = Document(text=txt)
da = DocumentArray(Document(text=s.strip()) for s in d.text.split('\n') if s.strip())  # 按照换行进行分割字符串
print('文字准备好了')
model = SentenceModel("shibing624/text2vec-base-chinese", encoder_type=EncoderType.FIRST_LAST_AVG, device = 'cpu')
feature_vec = model.encode
print('模型准备好了')
for d in tqdm(da):
    d.embedding = feature_vec(d.text)
text = Document(text='警告地球人不要回答')  # 要匹配的文本
text.embedding = feature_vec(text.text)
q = text.match(da, limit=10, exclude_self=True, metric='cos', use_scipy=True)  # 找到与输入的文本最相似的句子
pprint(q.matches[:, ('text', 'scores__cos')]) # 输出对应的文本与 cos 相似性分数