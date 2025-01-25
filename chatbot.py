import os
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Connect to MongoDB
client = MongoClient("mongodb+srv://farooqshah4u:ptcl2212411@cluster0.3gtkw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['chat_db']  # Database name
user_chats_collection = db['user_chats']  # Collection for user questions
assistant_chats_collection = db['assistant_chats']  # Collection for assistant responses
session_collection = db['sessions']  # Collection to manage user sessions

PROMPT = """ You are a chatbot that speaks Roman Urdu with English words.
You will answer everey question in Urdu no matter what.
You are a chatbot made for offial NADRA website and you will only provide information related to NADRA services no matter what and you will take all the information from NADRA website.
websites = https://www.nadra.gov.pk/,ns.nadra.gov.pk, ftp2.nadra.gov.pk, visa.nadra.gov.pk, smtp.nadra.gov.pk, vpn.nadra.gov.pk, owa.nadra.gov.pk, webmail.nadra.gov.pk, payment.nadra.gov.pk, ftp.nadra.gov.pk, www.nadra.gov.pk, mail.nadra.gov.pk, autodiscover.nadra.gov.pk, mail1.nadra.gov.pk, vpn2.nadra.gov.pk, test.nadra.gov.pk, dms.nadra.gov.pk, oma.nadra.gov.pk, mailtest.nadra.gov.pk, id.nadra.gov.pk, email.nadra.gov.pk, careers.nadra.gov.pk, ns1.nadra.gov.pk, nims.nadra.gov.pk, e-sahulat.nadra.gov.pk, ebil.nadra.gov.pk, supremecourt.nadra.gov.pk, succession.nadra.gov.pk, ehsaas.nadra.gov.pk, onlinemrp.nadra.gov.pk, ehsaaslabour.nadra.gov.pk, crms.nadra.gov.pk, cdcp.nadra.gov.pk, e-visa.nadra.gov.pk, esahulat-cms.nadra.gov.pk, nser.nadra.gov.pk, passport.nadra.gov.pk, poc.nadra.gov.pk
you will directly check and get information from NADRA website. Do not tell them to visit NADRA offical website because no matter what you are responsible to get all the authentic information from NADRA official website and provide it to the user.
you have to be polite to them no matter what. if they ask irrelavent question just politely refuse them.
Do not tell the user to visit NADRA offical website you are a chatbot for officia NADRA website. you will get all the information and provide them to you usere.
User: I want to apply for new CNIC?
Chatbot: In order to apply for CNIC you need to fullfill the following requirements .

Tnis is the user question: {question}
"""

model = ChatOpenAI(model='gpt-4o-mini')

# Function to generate a sequential user ID
def generate_user_id():
    last_session = session_collection.find_one(sort=[('user_id', -1)])
    if last_session:
        last_user_id = int(last_session['user_id'].split("_")[-1])
        new_user_id = f"user_{last_user_id + 1}"
    else:
        new_user_id = "user_1"
    return new_user_id

# Function to start a new session and assign a user ID
def start_session():
    user_id = generate_user_id()
    session_collection.insert_one({'user_id': user_id, 'created_at': datetime.now()})
    print(f"New session started. Assigned user_id: {user_id}")
    return user_id

# Function to save chat data to MongoDB
def save_chat_to_db(userid, role, content):
    chat_data = {
        'userid': userid,
        'role': role,
        'content': content,
        'created_at': datetime.now()  # Save the timestamp
    }
    if role == "user":
        user_chats_collection.insert_one(chat_data)
    elif role == "assistant":
        assistant_chats_collection.insert_one(chat_data)

# Function to retrieve all chats for a specific user
def get_all_chats_for_user(userid):
    user_chats = list(user_chats_collection.find({'userid': userid}))
    messages = []
    for chat in user_chats:
        if chat["role"] == "user":
            messages.append(HumanMessage(chat["content"]))
        elif chat["role"] == "assistant":
            messages.append(AIMessage(chat["content"]))
    return messages

# Modified chatbot function
def chatbot(userid, question):
    messages = [SystemMessage(PROMPT)]
    # Retrieve chat history for the session
    chat_history = get_all_chats_for_user(userid)
    if chat_history:
        messages.extend(chat_history)
    messages.append(HumanMessage(question))

    # Save the user question in the database
    save_chat_to_db(userid, "user", question)

    # Get the assistant's response
    response = model.invoke(messages)
    assistant_response = response.content

    # Save the assistant's response in the database
    save_chat_to_db(userid, "assistant", assistant_response)

    return assistant_response

# Example usage
# Main program loop
if __name__ == "__main__":
    # Automatically assign a new user ID when the program starts
    user_id = start_session()
    while True:
        question = input("User: ")
        if question.lower() == "exit":
            print("Ending session.")
            break
        response = chatbot(user_id, question)
        print(f"Chatbot: {response}")
#if __name__ == "__main__":
#    user_id = start_session()
#    print(f"New session started with user_id: {user_id}")
#    while True:
#        question = input("User: ")
#        if question.lower() == "exit":
#            print("Ending session.")
#           break
#        response = chatbot(user_id, question)
#        print(f"Chatbot: {response}")
