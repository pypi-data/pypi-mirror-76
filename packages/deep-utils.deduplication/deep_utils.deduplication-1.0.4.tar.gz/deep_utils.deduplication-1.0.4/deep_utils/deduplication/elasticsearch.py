import json
from typing import List, Dict, Tuple, NewType
from functools import reduce

from elasticsearch import Elasticsearch as Es

from .utils import es_wrapper

VectorDict = NewType('VectorDict', Dict[str, List[float]])

# Filter response data attributes
FILTER_PATH = ['hits.hits._score', 'hits.hits._id', 'hits.hits._source', 'hits.total', 'hits.max_score']


def create_data(doc_id: int, vectors: Dict[str, List[float]], index_name: str):
    data: List[Dict] = []
    data.append(dict(index=dict(_index=index_name, _id=doc_id)))
    data.append({vector_name: vector for vector_name, vector in vectors.items()})
    return data


def es_bulk(index_name: str, data: List[Dict]) -> Tuple[bool, str]:
    response = es.bulk(index=index_name, body=data)
    if response['errors']:
        return False, response['items'] and response['items'][0]['index']['error']['caused_by']['reason']
    return True, 'Success'


def add_to_index(doc_id: int, vectors: VectorDict, index_name: str, es: Es):
    data = create_data(doc_id, vectors, index_name)
    print(json.dumps(data, indent=4))
    return es_bulk(index_name, data)


def add_to_index_bulk(doc_ids: List[int], vectors: List[VectorDict], index_name: str, es: Es) -> Tuple[bool, str]:
    # Check if lengths match
    if len(doc_ids) != len(vectors):
        return False, "Mismatching number of doc_ids and vectors"
    data: List[Dict] = reduce(
        lambda acc, id_vector: [*acc, *create_data(id_vector[0], id_vector[1], index_name)],
        zip(doc_ids, vectors),
        []
    )
    return es_bulk(index_name, data)


def search_similar(similar_count: int, vector: Tuple[str, List[float]], index_name: str, es: Es):
    query = {
        "size": similar_count,
        "query": {
            "knn": {
                vector[0]: {
                    "vector": vector[1],
                    "k": similar_count
                }
            }
        }
    } if vector else None
    return es.search(body=query, index=index_name, filter_path=FILTER_PATH)


if __name__ == '__main__':
    import random
    index_name = "en-test-index"
    es = es_wrapper(
        endpoint='https://search-deep-dev-7yt6m5ulk7irae7vgbgu3ueafe.us-east-1.es.amazonaws.com',
        region='us-east-1',
        profile_name='dfs-es'
    )
    bulk_size = 50
    rangedata = range(bulk_size)
    vecs = [{'vector1': [random.randrange(50) for _ in range(5)]} for _ in rangedata]
    # resp = add_to_index_bulk([x + 1. for x in rangedata], vecs, index_name, es)
    search_param = ('vector1', [10, 22, 47, 46, 47])
    # search_param = None
    resp = search_similar(5, search_param, index_name, es)
    print(resp)
