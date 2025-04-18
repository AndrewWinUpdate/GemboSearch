import pysrt
from elasticsearch import Elasticsearch

ELASTIC_USER = "elastic" 
ELASTIC_PASSWORD = "L2RDCKVFJr350ldjWiw5"  
ELASTIC_HOST = "https://host.docker.internal:9200" 

es = Elasticsearch(
    [ELASTIC_HOST],
    basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
    verify_certs=False
)

def parse_srt(file_path, rus_path, eng_path):
    subs = pysrt.open(file_path)
    parsed_subtitles = []

    for sub in subs:
        parsed_subtitles.append({
            "start_time": str(sub.start),
            "end_time": str(sub.end),
            "text": sub.text.replace("\n", " "),
            "path_to_rus_sub": rus_path,
            "path_to_eng_sub": eng_path
        })

    return parsed_subtitles

def index_clip(movie_id, clip_id, srt_path, path_to_rus_sub, path_to_eng_sub):
    subtitles = parse_srt(srt_path, path_to_rus_sub, path_to_eng_sub)

    doc = {
        "movie_id": movie_id,
        "clip_id": clip_id,
        "subtitles": subtitles
    }

    es.index(index="clips", id=clip_id, document=doc)

def search_clips(query):
    body = {
        "query": {
            "nested": {
                "path": "subtitles",
                "query": {
                    "match": {
                        "subtitles.text": query
                    }
                }
            }
        }
    }
    res = es.search(index="clips", body=body)
    return res["hits"]["hits"]
