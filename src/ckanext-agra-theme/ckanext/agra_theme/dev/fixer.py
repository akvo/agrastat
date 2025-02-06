from ckan.model import Session, Tag, Vocabulary


def fixer():
    vocab = Vocabulary.by_name("value_chains")
    tag = Tag.by_name("Poutry", vocab=vocab)
    if tag:
        tag.name = "Poultry"
        Session.commit()
    else:
        print("Tag not found")
