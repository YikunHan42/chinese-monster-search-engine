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

# query.summary()

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

# for d in da:
#     print(d.image.embedding)
#     print(type(d.image.embedding))

# embed text data in query and dataset

model = SentenceModel("shibing624/text2vec-base-chinese", encoder_type=EncoderType.FIRST_LAST_AVG, device='cpu')
feature_vec = model.encode

query.main_text.embedding = feature_vec(query.main_text.text)
query.description.embedding = feature_vec(query.description.text)

for d in tqdm(da):
    # print(d.main_text)
    # print(type(d.main_text))
    # d.main_text.summary()
    # print(d.main_text.text)
    d.main_text.embedding = feature_vec(d.main_text.text)
    d.description.embedding = feature_vec(d.description.text)
    # print(d.main_text.embedding)
    # print(d.description.embedding)
    # print(type(d.description.embedding))
    # print(d.embedding.shape)
    # d.embedding = np.concatenate([feature_vec(d.main_text.text), feature_vec(d.description.text)])
    # print(d.embedding.shape)

    # d.main_text.embedding = feature_vec(d.main_text)
    # d.description.embedding = feature_vec(d.description)
    # d.embedding = np.concatenate([feature_vec(d.main_text), feature_vec(d.description)])

# for d in tqdm(da):
#     # d.summary()
#     print(d.embedding)

# query.main_text.embed_feature_hashing()
# query.description.embed_feature_hashing()改


# da['@.[description, main_text]'].apply(lambda d: feature_vec(d))


# print(query.main_text.embedding)
#
#
# combine embeddings to overall embedding
def combine_embeddings(d):
    # any (more sophisticated) function could go here
    d.embedding = np.concatenate(
        [d.image.embedding, d.main_text.embedding, d.description.embedding]
    )
    return d


query = combine_embeddings(query)  # combine embeddings for query
da.apply(combine_embeddings)  # combine embeddings in dataset

for d in da:
    print(d.embedding.shape)
    # print(d.embedding)

closest_match_page = da.find(query)[0][0]
print('OVERALL CLOSEST PAGE:')
closest_match_page.summary()

# da.push(name="devilanddemon")