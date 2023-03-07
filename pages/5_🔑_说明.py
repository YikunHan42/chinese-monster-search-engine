import streamlit as st



st.title('说明 :key:')

st.markdown("中文语义匹配模型在[text2vec-base-chinese](https://huggingface.co/shibing624/text2vec-base-chinese)上进行了微调,\
            原模型在数据集上的性能如下:")

table = f"""
| Model Name                            | ATEC  | BQ    | LCQMC | PAWSX | STS-B | Avg   | QPS    |
|---------------------------------------|-------|-------|-------|-------|-------|-------|--------|
| w2v-light-tencent-chinese             | 20.00 | 31.49 | 59.46 | 2.57  | 55.78 | 33.86 | 10283  |
| paraphrase-multilingual-MiniLM-L12-v2 | 18.42 | 38.52 | 63.96 | 10.14 | 78.90 | 41.99 | 2371   |
| text2vec-base-chinese                 | 31.93 | 42.67 | 70.16 | 17.21 | 79.30 | 48.25 | 2572   |
"""
st.markdown(table)

st.markdown("")
st.write("""相似度计算公式如下:
$$
similarity(doc_1,doc_2)=cos(θ)=\\frac{doc_1doc_2}{|doc_1||doc_2|}
$$
""")

st.write("""
$$
distance(doc_1,doc_2)=1−similarity(doc_1,doc_2)
$$
""")

st.write("""视觉使用的网络架构如右图：
![resnet50](https://datagen.kinsta.cloud/app/uploads/2022/08/image1-1-414x1024.png)
""")

st.markdown("参数见下图:")

st.markdown("![resnet-50](https://datagen.kinsta.cloud/app/uploads/2022/08/image2-2-1024x446.png)")



