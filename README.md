## Welcome to the first steps of creating a PLEXOS AI

### First Step: Choosing A Large Language Model(LLM)
In this script, the llama 3.1 LLM was used with the help of Ollama to run the LLM locally
Go to https://ollama.com/ and install ollama 
Choose an LLM, run the following command in the terminan/cmd in order to download the LLM
        
    ollama pull llama3.1
To test, run the following and type a prompt:
    
    ollama run llama3.1 
### Second Step: Gather Data
Create a folder/directory named Extracted_Data, place all the files you want to train your LLM on in this case, 
we will be using well documented PLEXOS API code.

### Third Step: RAG Script
Install the following dependencies 
        
    pip install llama-index
    pip install llama-index-llms-ollama
    pip install llama_index.embeddings.huggingface
note if you are using windows you have to do this extra step:
    
    pip uninstall torch
    pip install torch==2.2


The RAG.py has three functions 

    construct_index()
        this function takes in a dirctory path, loads the files, then generates an index
        and saves it in the model Folder/Directory
    
    load_index()
        this function takes the model Folder/Directory from the storage returns it as an index
    
    save_to_excel():
        Saves query results to an Excel file. If the file exists, it prompts whether to append or overwrite.
    
        
### Fourth Step: Run and create training data
first time using the program you must call the construct_index to create a index. After it has been created 
you can call the load_index() instead. After you ask a prompt, an answer will be generated, it will ask if you want 
to save it by typing yes/y. After you create enough data that is saved in the excel file,
we can upload this data for it to be fine tune the model.
