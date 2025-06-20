import os
from dotenv import load_dotenv

load_dotenv()

# Global Configuration variables
ffd4_URL = os.getenv("FFD4_URL")
index_path = os.getenv("INDEX_PATH")
doc_path = os.getenv("DOC_PATH")
persist_dir = os.getenv("PERSIST_DIR")
embedding_model_ = os.getenv("EMBEDDING_MODEL")
llm_model = os.getenv("LLM_MODEL")
evaluation_model = os.getenv("EVAL_MODEL")