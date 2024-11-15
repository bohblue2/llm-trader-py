OPENAI_EMBEDDING_DIM=3072
DEFAULT_EMBEDDING_DIM = OPENAI_EMBEDDING_DIM
DEFAULT_CHUNK_SIZE= 500
DEFAULT_CHUNK_OVERLAP = DEFAULT_CHUNK_SIZE * 0.1
DEFAULT_FAISS_FOLDER_PATH='yongin_db'
DEFAULT_FAISS_INDEX_NAME='yongin_index'

NAVER_NEWS_ARTICLE_COLLECTION="naver_news_articles"
NAVER_RESEARCH_REPORT_COLLECTION='naver_research_reports'

MILVUS_METRIC_TYPE='L2'
MILVUS_INDEX_TYPE='IVF_FLAT'
MILVUS_NLIST=1024
MILVUS_NPROBE=32
MILVUS_DIM=DEFAULT_EMBEDDING_DIM
MILVUS_TOP_K=10
