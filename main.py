# from docarray import dataclass
# from docarray.typing import Image, Text
#
#
# @dataclass
# class Page:
#     main_text: Text
#     image: Image
#     description: Text
#
# from docarray import Document
#
# page = Page(
#     main_text='八哥',
#     image='八哥.jpg',
#     description='清代时，某人养了一只八哥，教它说话，驯养得很灵巧。这人很喜欢这只\
# 八哥，连出门都和它形影不离，就这样过了好几年。\
# 一天，这人去绛州，离家很远，盘缠用光了，正在发愁，八哥说：“你为\
# 什么不把我给卖了呢？卖到王爷家里，肯定能有个好价钱，不愁回去没有路\
# 费。”这人说：“我怎么忍心呀！”八哥说：“没事，你拿到了钱，赶紧走，到城\
# 西二十里的那棵大树下等我。”这人就答应了。\
# 这人带着鸟进了城，八哥和他有问有答，引来很多人看热闹，王爷听说了，\
# 就把这人叫到了府里，问卖不卖。这人说：“小人我和这只鸟相依为命，不愿\
# 意卖。”王爷问鸟：“你愿意留下来吗？ ”八哥说：“我愿意！”王爷听了，很高\
# 兴。鸟说：“给十两银子，别多给。”\
# 王爷听了，更加高兴，让人拿来十两银子，交给了这人。这人故意做出后\
# 悔的样子，离开了。\
# 王爷买了鸟，和鸟说说笑笑，很高兴，还让人取来肉喂鸟。八哥吃完了，\
# 说：“我要洗澡！”王爷就让人用金盆盛水，开了笼子。鸟洗了澡，在屋檐外\
# 飞来飞去，与王爷说了一会儿话，大声道：“我走了哈！”言罢，展翅飞走。\
# 王爷和仆人们四处寻找，也没找到那只八哥。\
# 后来，有人在西安的集市上看到过那个人，还有那只八哥。',
# )
#
# doc = Document(page)
# doc.summary()
#
# from torchvision.models import resnet50
#
# img_model = resnet50(pretrained=True)
#
# # embed textual data
# doc.main_text.embed_feature_hashing()
# doc.description.embed_feature_hashing()
# # embed image data
# doc.image.set_image_tensor_shape(shape=(224, 224)).set_image_tensor_channel_axis(
#     original_channel_axis=-1, new_channel_axis=0
# ).set_image_tensor_normalization(channel_axis=0).embed(img_model)
#
# print(doc.main_text.embedding.shape)
# print(doc.description.embedding.shape)
# print(doc.image.embedding.shape)

from docarray import dataclass, Document, DocumentArray
from docarray.typing import Image, Text
from tqdm import tqdm
from text2vec import SentenceModel, EncoderType
import numpy as np


@dataclass
class Page:
    main_text: Text
    image: Image = None
    description: Text = None


query_page = Page(
    main_text='八子哥',
    image='八哥.jpg',
    description = '或许是八哥',
)

query = Document(query_page)  # our query Document

query.summary()

da = DocumentArray(
    [
        Document(
            Page(
                main_text='八哥',
                image='八哥.jpg',
                description='这是一只八哥',
            )
        ),
        Document(
            Page(
                main_text='貘',
                image='貘.jpg',
                description='这是一只貘',
            )
        ),
    ],
    subindex_configs={'@.[image]': None},
)  # our dataset of pages


from torchvision.models import resnet50
import numpy as np

img_model = resnet50(pretrained=True)

# embed query
query.image.set_image_tensor_shape(shape=(224, 224)).set_image_tensor_channel_axis(
    original_channel_axis=-1, new_channel_axis=0
).set_image_tensor_normalization(channel_axis=0).embed(img_model)

# embed dataset
da['@.[image]'].apply(
    lambda d: d.set_image_tensor_shape(shape=(224, 224))
    .set_image_tensor_channel_axis(original_channel_axis=-1, new_channel_axis=0)
    .set_image_tensor_normalization(channel_axis=0)
).embed(img_model)

# embed text data in query and dataset

model = SentenceModel("shibing624/text2vec-base-chinese", encoder_type = EncoderType.FIRST_LAST_AVG, device = 'cpu')
feature_vec = model.encode

# for d in tqdm(da):
#     d.embedding = feature_vec(d.main_text)
#     d.embedding = feature_vec(d.description)

# query.main_text.embed_feature_hashing()
# query.description.embed_feature_hashing()改



query.summary()

da['@.[description, main_text]'].apply(lambda d: d.embed_feature_hashing())


print(query.main_text.embedding)

# combine embeddings to overall embedding
def combine_embeddings(d):
    # any (more sophisticated) function could go here
    d.embedding = np.concatenate(
        [d.image.embedding, d.main_text.embedding, d.description.embedding]
    )
    return d


query = combine_embeddings(query)  # combine embeddings for query
da.apply(combine_embeddings)  # combine embeddings in dataset

