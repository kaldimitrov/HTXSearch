import chromadb

DB_PATH = "/var/htx-search/chroma"

client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_or_create_collection(name="test")
