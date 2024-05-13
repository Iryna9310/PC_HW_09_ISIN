from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField

class Author(Document):
    fullname = StringField(required=True)
    born_date = DateTimeField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)