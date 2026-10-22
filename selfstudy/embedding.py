

model = None


def get_model():

    from sentence_transformers import SentenceTransformer

    global model
 
    if model is None:

        

        model = SentenceTransformer(
            "sentence-transformers/all-mpnet-base-v2"
        )

    return model


def create_embeddings(chunks):

    if not chunks:
        return []

    model = get_model()

    embeddings = model.encode(chunks)

    return embeddings.tolist()


def create_query_embedding(query):

    if not query:
        return None

    model = get_model()

    embedding = model.encode(query)

    return embedding.tolist()