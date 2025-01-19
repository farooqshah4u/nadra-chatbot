import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage,SystemMessage, HumanMessage,ToolMessage
#from langchain_core.tools import Tool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
#from langchain_core.tools import tool




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
messages = [SystemMessage(PROMPT)]

def chatbot(question):
    messages.append(HumanMessage(question))
    response = model.invoke(messages)
    messages.append(response)
    return response.content

# while True:
#     question = input("User: ")
#     if question == "exit":
#         break
    
#     messages.append(HumanMessage(question))
#     response = model.invoke(messages)
#     messages.append(response)
    
#     print("Chatbot: ", response.content)
#     print("")
    
    
    