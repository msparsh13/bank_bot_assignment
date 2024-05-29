import streamlit as st
import uuid
from dataclasses import dataclass
import langchain
from langchain_community.vectorstores.faiss import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
import cohere 
from langchain.document_loaders import PyPDFLoader

co = cohere.Client("r4TYW3pued8wTV0CC8dEYnIoiCPN5MyCBn0ecDej")



@dataclass
class UserDetails:
    personal_details: dict
    address_details: dict
    nominee_details: dict
    customer_id: str = ''
    account_creation_id: str = ''



if "data" not in st.session_state:
    embeddings_model_repo = 'sentence-transformers/all-MiniLM-L6-v2'
    embeddings  = HuggingFaceEmbeddings( model_name =embeddings_model_repo , model_kwargs={'device' : 'cpu'})
    loader = PyPDFLoader(r"C:\Users\Sparsh Mahajan\OneDrive\Documents\c progams\.vscode\.vscode\backend\bank bot\Kulti - Mariana Zapata.pdf")
    docs = loader.load_and_split()
    st.session_state["data"]= FAISS.from_documents(
    embedding = embeddings,
    documents = docs
 )

def generate_unique_id():
    return str(uuid.uuid4())


def search(txt , k=3):
  retrieved_examples = st.session_state.data.similarity_search( txt, k=k )
  return retrieved_examples


def for_prompt(retrieved_documents , k=3):
  PROMPT = f""" You are an assistant for answering questions.
    You are given a document and a question. Provide a conversational answer.
    If you don't know the answer, just say "I do not know." Don't make up an answer.
    ## Question {prompt}   ##  Document """
  for idx in range(k) :
    PROMPT+= f"{retrieved_documents[idx].page_content}\n"
  PROMPT = PROMPT.replace("\t" , " ")
  return PROMPT



def generate(prmt):
   
    txt= search(prmt)## get similar documents
    prompt= for_prompt(txt) ## use that in prompt
    ans = co.chat(message=prompt).text
    return ans

if "user details" not in st.session_state:
    st.session_state['user_details']=UserDetails( personal_details={} ,address_details={} ,  nominee_details={} , customer_id='' , account_creation_id=''  )
  
if not "step" in st.session_state:
        st.session_state['step']=0

st.title("Banking Assitant Bot")

prompt=""


if st.session_state['step']==0:

    if "messages" not in st.session_state:
        st.session_state.messages = []


    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask Your Query"):

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        response = generate(prompt)
        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
        

if  st.session_state['step']==0:
    acc = st.button("create account")
    if acc:
        st.session_state['step']=1

if st.session_state['step']>=0 :
    email=""
    first_name=""
    last_name=""
    mobile_number=""

    if st.session_state["step"]==1:
        form= st.form("Personal Details")
        email = form.text_input("Email Address", key="email")
        first_name = form.text_input("First Name", key="first_name")
        last_name = form.text_input("Last Name", key="last_name")
        mobile_number = form.text_input("Mobile Number", key="mobile_number")
        if form.form_submit_button("Review Personal Details"):
            st.session_state["step"]=2


    if st.session_state["step"]==2:
        st.header("Review Personal Details")

        sub = st.button("Confirm Details" , key="abc")

        if sub:
            st.session_state["user_details"].personal_details={"email": email , "first name": first_name , "last_name":last_name , "mobile":mobile_number}
            st.session_state["step"]=3

        
        else :
            st.write("Email:", email)
            st.write("First Name:", first_name)
            st.write("Last Name:", last_name)
            st.write("Mobile Number:", mobile_number)
        
        

        


    addr=""
    city=""
    country=""
    pincode=""

    if st.session_state["step"]==3:
        form= st.form("Address Details")
        addr = form.text_input("Address", key="addr")
        city= form.text_input("city", key="city")
        country = form.text_input("Country", key="country")
        pincode = form.text_input("Pincode", key="pincode")
        if form.form_submit_button("Review Address Details"):
            st.session_state["step"]=4


    if st.session_state["step"]==4:

        sub = st.button("Confirm Details")

        if sub:
            st.session_state["user_details"].address_details={"address": addr , "City": city , "Country": country, "mobile":mobile_number}
            st.session_state["step"]=5

        else:
            st.header("Review Personal Details")
            st.write("Adrress:", addr)
            st.write("City:", city)
            st.write("Country:", country)
            st.write("Pincode:", pincode)
        

        


    name=""
    email=""
    contact=""
        
    if st.session_state["step"]==5:
        form= st.form("Nominee Details")
        name = form.text_input("name", key="name")
        email= form.text_input("email", key="email")
        contact = form.text_input("Contact", key="phone")
        if form.form_submit_button("Review Address Details"):
            st.session_state["step"]=6


    if st.session_state["step"]==6:

        sub= st.button("Confirm Details")
       
        if sub:
            st.session_state["user_details"].nominee_details={"email": email , "name": name  , "mobile": contact}
            st.session_state["step"]=7
            
        else:
            st.header("Review Nominee Details")
            st.write("Name:", name)
            st.write("email:", email)
            st.write("Mobile Number:", contact)
           

        

    if st.session_state["step"]==7:
        st.session_state["user_details"].customer_id=generate_unique_id()
        st.session_state["user_details"].account_creation_id=generate_unique_id()
        st.write("Your account has been created with customer id "+st.session_state["user_details"].customer_id + "and account id" + st.session_state["user_details"].account_creation_id)

    
            



    
            
            
                
       

        