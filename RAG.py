import os
import pandas as pd
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext, load_index_from_storage
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


def save_to_excel(prompt, combined_context, response_str):
    # File path
    file_path = 'query_results.xlsx'

    # Prepare data for DataFrame
    new_data = {
        'Instruction': [prompt],
        'Context': [combined_context],
        'Response': [response_str]
    }
    new_df = pd.DataFrame(new_data)

    # Check if the file exists
    if os.path.exists(file_path):
        # Load existing data
        existing_df = pd.read_excel(file_path, engine='openpyxl')
        # Append new data
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        # If file does not exist, use new_df as the DataFrame
        updated_df = new_df

    # Save DataFrame to Excel
    updated_df.to_excel(file_path, index=False, engine='openpyxl')
    print("Results saved to query_results.xlsx")


# Uncomment this line if you need to construct a new index
# ChatIndex = construct_index(directory_path="Extracted_Data")

# Load existing index
ChatIndex = load_index()
leave = True
while leave:
    print("Please enter a question regarding PLEXOS (or type 'quit' to exit)")
    prompt = input()
    if prompt.lower() == "quit":
        exit()

    query_engine = ChatIndex.as_query_engine()
    response = query_engine.query(prompt)

    # Extract and combine contexts
    contexts = [source_node.get_content() for source_node in response.source_nodes]
    combined_context = "\n\n".join(contexts)  # Combine all contexts into a single string

    # Print the response
    print(response)

    # Ask user if they want to save the result
    user_input = input("Do you want to save this result to Excel? (yes/no): ").strip().lower()
    if user_input in ['yes', 'y']:
        # Save to Excel
        save_to_excel(prompt, combined_context, response.response)
