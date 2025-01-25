import os
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool
from datetime import datetime
from nadra import web_database

# Load environment variables from .env file
load_dotenv()

@tool
def web_db(question):
    """
    Get the web database data for the given question by passing question variable.
    This contains data about NADRA services that they provide to the customers from NADRA main domain and all its sub-domains.
    """
    return web_database(question)

tools = [web_db]

# Connect to MongoDB
client = MongoClient(os.getenv("mongodb+srv://farooqshah4u:ptcl2212411@cluster0.3gtkw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"))
db = client['chat_db']  # Database name
user_chats_collection = db['user_chats']  # Collection for user questions
assistant_chats_collection = db['assistant_chats']  # Collection for assistant responses
session_collection = db['sessions']  # Collection to manage user sessions

PROMPT = """You are a chatbot that speaks Roman Urdu with English words.
You will answer every question in Urdu no matter what.
You are a chatbot made for the official NADRA website, and you will only provide information related to NADRA services no matter what.
You will dynamically fetch information from NADRA's official websites using an integrated tool.
You must not tell users to visit NADRA's website; instead, you are responsible for providing authentic information directly.
You must be polite at all times and refuse irrelevant questions gently.
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

# Chatbot function
def chatbot(userid, question):
    messages = [SystemMessage(PROMPT)]
    chat_history = get_all_chats_for_user(userid)
    if chat_history:
        messages.extend(chat_history)
    messages.append(HumanMessage(question))

    save_chat_to_db(userid, "user", question)

    # Get the assistant's response
    response = model.invoke(messages)
    assistant_response = response.content

    # Process tool calls if any
    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call['name'] == "web_db":
                web_data = web_db(tool_call['args']['question'])
                messages.append(AIMessage(web_data))
                assistant_response = web_data

    save_chat_to_db(userid, "assistant", assistant_response)
    return assistant_response

# Main program loop
if __name__ == "__main__":
    user_id = start_session()
    while True:
        question = input("User: ")
        if question.lower() == "exit":
            print("Ending session.")
            break
        try:
            response = chatbot(user_id, question)
            print(f"Chatbot: {response}")
        except Exception as e:
            print(f"Error: {e}")

# import os
# from dotenv import load_dotenv
# from pymongo import MongoClient
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
# from langchain_core.tools import tool
# from datetime import datetime
# from nadra import web_database

# # Load environment variables from .env file
# load_dotenv()

# @tool
# def web_db(question):
#     """
#     Get the web database data for the given question by passing question variable.
#     This contains data about NADRA services that they provide to the customers from NADRA main domain and all it's sub-domains
#     """
#     return web_database(question)

# tools = [web_db]
# # Connect to MongoDB
# client = MongoClient("mongodb+srv://farooqshah4u:ptcl2212411@cluster0.3gtkw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# db = client['chat_db']  # Database name
# user_chats_collection = db['user_chats']  # Collection for user questions
# assistant_chats_collection = db['assistant_chats']  # Collection for assistant responses
# session_collection = db['sessions']  # Collection to manage user sessions

# PROMPT = """ You are a chatbot that speaks Roman Urdu with English words.
# You will answer every question in Urdu no matter what.
# You are a chatbot made for the official NADRA website, and you will only provide information related to NADRA services no matter what.
# You will dynamically fetch information from NADRA's official websites using an integrated tool.
# You must not tell users to visit NADRA's website; instead, you are responsible for providing authentic information directly.
# You must be polite at all times and refuse irrelevant questions gently.
# User: I want to apply for new CNIC?
# Chatbot: In order to apply for CNIC you need to fullfill the following requirements .

# Tnis is the user question: {question}
# """

# model = ChatOpenAI(model='gpt-4o-mini')

#  if response.tool_calls:
#         for tool_call in response.tool_calls:
#             if tool_call['name'] == "web_db":
#                     web_data = web_db(tool_call['args']['question'])
#                     tool_output = ToolMessage(web_data,tool_call_id=tool_call["id"])
#                     messages.append(ToolMessage(web_db(tool_call['args']['question']),tool_call_id=tool_call["id"]))



# # Function to generate a sequential user ID
# def generate_user_id():
#     last_session = session_collection.find_one(sort=[('user_id', -1)])
#     if last_session:
#         last_user_id = int(last_session['user_id'].split("_")[-1])
#         new_user_id = f"user_{last_user_id + 1}"
#     else:
#         new_user_id = "user_1"
#     return new_user_id

# # Function to start a new session and assign a user ID
# def start_session():
#     user_id = generate_user_id()
#     session_collection.insert_one({'user_id': user_id, 'created_at': datetime.now()})
#     print(f"New session started. Assigned user_id: {user_id}")
#     return user_id

# # Function to save chat data to MongoDB
# def save_chat_to_db(userid, role, content):
#     chat_data = {
#         'userid': userid,
#         'role': role,
#         'content': content,
#         'created_at': datetime.now()  # Save the timestamp
#     }
#     if role == "user":
#         user_chats_collection.insert_one(chat_data)
#     elif role == "assistant":
#         assistant_chats_collection.insert_one(chat_data)

# # Function to retrieve all chats for a specific user
# def get_all_chats_for_user(userid):
#     user_chats = list(user_chats_collection.find({'userid': userid}))
#     messages = []
#     for chat in user_chats:
#         if chat["role"] == "user":
#             messages.append(HumanMessage(chat["content"]))
#         elif chat["role"] == "assistant":
#             messages.append(AIMessage(chat["content"]))
#     return messages

# # Modified chatbot function
# def chatbot(userid, question):
#     messages = [SystemMessage(PROMPT)]
#     # Retrieve chat history for the session
#     chat_history = get_all_chats_for_user(userid)
#     if chat_history:
#         messages.extend(chat_history)
#     messages.append(HumanMessage(question))

#     # Save the user question in the database
#     save_chat_to_db(userid, "user", question)

#     # Get the assistant's response
#     response = model.invoke(messages)
#     assistant_response = response.content

#     # Save the assistant's response in the database
#     save_chat_to_db(userid, "assistant", assistant_response)

#     return assistant_response

# # Example usage
# # Main program loop
# if __name__ == "__main__":
#     # Automatically assign a new user ID when the program starts
#     user_id = start_session()
#     while True:
#         question = input("User: ")
#         if question.lower() == "exit":
#             print("Ending session.")
#             break
#         response = chatbot(user_id, question)
#         print(f"Chatbot: {response}")
# #if __name__ == "__main__":
# #    user_id = start_session()
# #    print(f"New session started with user_id: {user_id}")
# #    while True:
# #        question = input("User: ")
# #        if question.lower() == "exit":
# #            print("Ending session.")
# #           break
# #        response = chatbot(user_id, question)
# #        print(f"Chatbot: {response}")
