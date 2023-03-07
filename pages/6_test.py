from docarray import dataclass, Document, DocumentArray
from docarray.typing import Image, Text


@dataclass
class Page:
    main_text: Text
    image: Image
    description: Text


query_page = Page(
    main_text='Hello world',
    image='八哥.jpg',
    description='This is the image of an apple',
)

query = Document(query_page)  # our query Document

da = DocumentArray(
    [
        Document(
            Page(
                main_text='First page',
                image='八哥.jpg',
                description='This is the image of an apple',
            )
        ),
        Document(
            Page(
                main_text='Second page',
                image='八哥.jpg',
                description='This is an image of a pear',
            )
        ),
    ],
    subindex_configs={'@.[image]': None},
)  # our dataset of pages

r = da.find({'main_text': {'$eq': 'Second Page'}})

print(r)  # just for pretty print