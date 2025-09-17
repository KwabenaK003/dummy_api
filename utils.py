def replace_book_id(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc