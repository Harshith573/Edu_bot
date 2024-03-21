# Description: This is the main file for the chatbot.
# It is used to initialize the database and the large language model.
# It also contains the conversation function which is used to generate the response for the user input.
# The main function is used to initialize the telegram bot.


from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings 
from langchain_community.llms import HuggingFacePipeline
from langchain_community.llms import HuggingFaceHub
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
import dotenv

dotenv.load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get('TELE_TK')#telegram bot token for EDU-BOT
llm_name1 = "mistralai/Mistral-7B-Instruct-v0.2"#model name
file_path = "inputFile.pdf"#path to the pdf file 



#This is level1 of the chatbot its initialized with the database
def initialize_database( chunk_size, chunk_overlap):
    list_file_path = [file_path]
    doc_splits = load_doc(list_file_path, chunk_size, chunk_overlap)
    vector_db = create_db(doc_splits)
    return vector_db

# Load PDF document and create doc splits
def load_doc(list_file_path, chunk_size, chunk_overlap):
    loaders = [PyPDFLoader(x) for x in list_file_path]
    pages = []
    for loader in loaders:
        pages.extend(loader.load())
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size, 
        chunk_overlap = chunk_overlap)
    doc_splits = text_splitter.split_documents(pages)
    return doc_splits

# Create vector database
def create_db(splits):
    embedding = HuggingFaceEmbeddings()
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
    )
    return vectordb

#This is level2 of the chatbot its initialized with the llm chain 
def initialize_llmchain(llm_model, temperature, max_tokens, top_k, vector_db):
    '''
    if llm_model == "microsoft/phi-2":
        llm = HuggingFaceHub(
            repo_id=llm_model, 
            model_kwargs={"temperature": temperature, "max_new_tokens": max_tokens, "top_k": top_k, "trust_remote_code": True, "torch_dtype": "auto"},
            huggingfacehub_api_token=""
        )
    else:
    '''
    #initialize language model using huggine face hub
    llm = HuggingFaceHub(
        repo_id=llm_model, 
        model_kwargs={"temperature": temperature, "max_new_tokens": max_tokens, "top_k": top_k},huggingfacehub_api_token=os.environ.get('HUGGINGFACE_TK'))
    #initialize memory to store and retrieve the conversation
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key='answer',
        return_messages=True
    )
    #it is responsible for reteriving the revelant documents infomation based on used input
    retriever=vector_db.as_retriever()

    #handle conversational interaction and reterive relvent information 
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        chain_type="stuff", 
        memory=memory,
        return_source_documents=True,
    )
    return qa_chain

def initialize_LLM(llm_option, llm_temperature, max_tokens, top_k, vector_db):
    llm_name = llm_option
    print("llm_name: ",llm_name)
    qa_chain = initialize_llmchain(llm_name, llm_temperature, max_tokens, top_k, vector_db)
    return qa_chain


def conversation(qa_chain, message, history):
    formatted_chat_history = format_chat_history(message, history)
   
    # Generate response using QA chain
    response = qa_chain({"question": message, "chat_history": formatted_chat_history})
    response_answer = response["answer"]
    '''
    response_sources = response["source_documents"]
    response_source1 = response_sources[0].page_content.strip()
    response_source2 = response_sources[1].page_content.strip()
    # Langchain sources are zero-based
    response_source1_page = response_sources[0].metadata["page"] + 1
    response_source2_page = response_sources[1].metadata["page"] + 1
    # print ('chat response: ', response_answer)
    # print('DB source', response_sources)
    '''
    # Append user message and response to chat history
    new_history = history + [(message, response_answer)]
    #print("new_history: ",new_history)
    return  new_history

def format_chat_history(message, chat_history):
    formatted_chat_history = []
    for user_message, bot_message in chat_history:
        formatted_chat_history.append(f"User: {user_message}")
        formatted_chat_history.append(f"Assistant: {bot_message}")
    return formatted_chat_history



#From here the telegram bot starts
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to the edu-Bot! ask me a questions on Computer network module-1.")

def handle_text(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    history = context.chat_data.get('history', [])
    chat_history=conversation(qa_chain,user_message,history)
    update.message.reply_text(chat_history[-1][1])

def handle_document(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Sorry, I don't process documents. Please ask a question.")

def main() -> None:
    #Telegram bot Message Handler
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_text))
    dp.add_handler(MessageHandler(Filters.document, handle_document))

    updater.start_polling()
    updater.idle()

import json
if __name__ == "__main__":
    
    # Documents Handler
    vector_db=initialize_database(600,40)
    print("vector_db sucessfully initialized")
    qa_chain=initialize_LLM(llm_name1,0.1,1024,3,vector_db)
    print("qa_chain sucessfully initialized, starting telegram bot")
    main()
    
    '''
    #This is used to terminal conversation with the Large language model
    vector_db=initialize_database(600,40)
    docs=vector_db.get()
    #download the vector database as json file
    with open('documents.json', 'w') as f:
        json.dump(docs, f)
    qa_chain=initialize_LLM(llm_name1,0.7,1024,3,vector_db)
    c_hst=[]

    while True:
        msg=input("Enter your question: ")
        if msg=="bye":
            break
        chat_history=conversation(qa_chain,msg,c_hst)
        c_hst.append((msg))
        c_hst.append((chat_history))
        human_message_content = chat_history[-1][0]
        print(f"Human: {human_message_content}")
        ai_message_content = chat_history[-1][1]
        print(f"AI: {ai_message_content}")
    '''
