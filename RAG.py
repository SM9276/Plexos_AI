from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, PromptHelper, PromptHelper, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama


def construct_index(directory_path):
    Settings.llm = Ollama(model="llama3.1", request_timeout=360.0)
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
    documents = SimpleDirectoryReader(directory_path).load_data()
    storage_context = StorageContext.from_defaults()
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True
    )
    storage_context.persist(persist_dir='model')
    print("Construction Complete!")
    return index


def load_index():
    print("Loading last model ...")
    Settings.llm = Ollama(model="llama3.1", request_timeout=360.0)
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
    storage_context = StorageContext.from_defaults(persist_dir=f'model')
    index = load_index_from_storage(storage_context=storage_context)
    print("Loading Complete!")
    return index


# ChatIndex = construct_index(directory_path="/home/mangoblop/PycharmProjects/RAG/Extracted_Data")
ChatIndex = load_index()
leave = True
while leave:
    print("Please enter a question regarding PLEXOS")
    prompt = input()
    if prompt == "quit":
        exit()
    query_engine = ChatIndex.as_query_engine()
    # prompt_adder= "\nKeep in mind this is a question regarding PLEXOS, Once you find the answer, state it and explain in simpler terms\n "
    # print(prompt + prompt_adder)
    response = query_engine.query(prompt)
    print(response)

