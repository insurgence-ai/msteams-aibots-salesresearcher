import os
import openai
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
load_dotenv()

pinecone_api_key = os.environ.get('PINECONE_API_KEY')

def get_response_from_query(question, rag_chain, chat_history):
    response = rag_chain.invoke({"input": question, "chat_history": chat_history})
    chat_history.extend([HumanMessage(content=question), HumanMessage(content=response['answer'])])
    print(response['answer'])

    answer = response['answer']
    context_documents = response['context']

    link = []
    source = []
    for i, doc in enumerate(context_documents):
        page_content = doc.page_content
        pdf_name = doc.metadata['name']
        page_number = doc.metadata['page_number']
        link.append(doc.metadata['doc_link'])
        source.append(pdf_name + ", p. " + str(int(page_number) + 1))
        if i == 2:
            break

    return {
        "Answer": f"{answer}",
        "link": link,
        "source": source,
        "page_content": page_content
    }

def filterResponse(response):
    client = openai.AzureOpenAI(
        azure_endpoint = "https://salesiqtest.openai.azure.com/", 
        api_key=os.environ["API_KEY_GPT_4"],  
        api_version="2023-07-01-preview",
    )

    completion = client.chat.completions.create(
        model='sfslackbot',
        messages=[
            {"role": "system", "content": f"""You are a response verifier. User is answering a question based on the data provided and in case he is not able to find relevant data, his response is that he was not able to find relevant information. Now I will provide you with the response and if you think that the response is indeed saying I am not able to find relevant information, output "YES" otherwise output "NO"
            UNDER NO CIRCUMSTANCES WRITE ANYTHING EXCEPT FOR "YES" or a "NO"."""},
            {"role": "user", "content": f"""Here is the Response:{response}"""}
        ],
        temperature=0.1,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    response = completion.choices[0].message.content
    if "YES" in response:
        return "YES"
    else:
        return "NO"


def create_chain(namespace, Prompt):

    embeddings = AzureOpenAIEmbeddings(
        model= "text-embedding-3-large",
        azure_endpoint = "https://salesiqdemo.openai.azure.com/", 
        api_key=os.environ["API_KEY"],  
        api_version="2024-02-15-preview",
        azure_deployment="langchain-test",
    )
    
    vectorstore = PineconeVectorStore(
        index_name="data",
        embedding=embeddings,
        namespace = namespace
    )
    retriever = vectorstore.as_retriever()

    llm = AzureChatOpenAI(
        azure_endpoint = "https://salesiqtest.openai.azure.com/", 
        api_key=os.environ["API_KEY_GPT_4"],  
        api_version="2023-07-01-preview",
        azure_deployment='sfslackbot',
    )


    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    qa_system_prompt = Prompt

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain

