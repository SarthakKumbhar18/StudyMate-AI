import chromadb
from django.conf import settings


client = chromadb.PersistentClient(
    path=str(settings.BASE_DIR / 'chroma_db')
)


collection = client.get_or_create_collection(
    name='study_materials'
)


def store_chunks(chunks, embeddings, study_id, student_id):

    if not chunks:
        return

    ids = []

    documents = []

    metadatas = []

    for index, chunk in enumerate(chunks):

        ids.append(
            f"study_{study_id}_chunk_{index}"
        )

        documents.append(chunk)

        metadatas.append({
            'study_id': str(study_id),
            'student_id': str(student_id),
            'chunk_index': index
        })

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )
    
    
    
def search_chunks(query_embedding, student_id, study_id=None):
    
    if study_id is not None:

        where = {
            '$and': [
                {
                    'student_id': str(student_id)
                },
                {
                    'study_id': str(study_id)
                }
            ]
        }

    else:

        where = {
            'student_id': str(student_id)
        }

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        where=where
    )

    return results['documents'][0]