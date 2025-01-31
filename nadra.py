import os
from langchain_community.document_loaders import WebBaseLoader

def extract_combined_text(pages):
    """
    Combines the page content of multiple documents into a single string.
    """
    return " ".join([page.page_content for page in pages])

def web_database(question):
    loader = WebBaseLoader() # Initialize the WebBaseLoader
    """
    Fetches relevant information from NADRA's official websites and subdomains
    based on the given question.
    """
    pages = [
        "https://www.nadra.gov.pk",
        "https://ns.nadra.gov.pk",
        "https://ftp2.nadra.gov.pk",
        "https://visa.nadra.gov.pk",
        "https://smtp.nadra.gov.pk",
        "https://vpn.nadra.gov.pk",
        "https://owa.nadra.gov.pk",
        "https://webmail.nadra.gov.pk",
        "https://payment.nadra.gov.pk",
        "https://ftp.nadra.gov.pk",
        "https://www.nadra.gov.pk",
        "https://mail.nadra.gov.pk",
        "https://autodiscover.nadra.gov.pk",
        "https://mail1.nadra.gov.pk",
        "https://vpn2.nadra.gov.pk",
        "https://test.nadra.gov.pk",
        "https://dms.nadra.gov.pk",
        "https://oma.nadra.gov.pk",
        "https://mailtest.nadra.gov.pk",
        "https://id.nadra.gov.pk",
        "https://email.nadra.gov.pk",
        "https://careers.nadra.gov.pk",
        "https://ns1.nadra.gov.pk",
        "https://nims.nadra.gov.pk",
        "https://e-sahulat.nadra.gov.pk",
        "https://ebil.nadra.gov.pk",
        "https://supremecourt.nadra.gov.pk",
        "https://succession.nadra.gov.pk",
        "https://ehsaas.nadra.gov.pk",
        "https://onlinemrp.nadra.gov.pk",
        "https://ehsaaslabour.nadra.gov.pk",
        "https://crms.nadra.gov.pk",
        "https://cdcp.nadra.gov.pk",
        "https://e-visa.nadra.gov.pk",
        "https://esahulat-cms.nadra.gov.pk",
        "https://nser.nadra.gov.pk",
        "https://passport.nadra.gov.pk",
        "https://poc.nadra.gov.pk"
    ]

    docs = []
    for data in pages:
        loader = WebBaseLoader(data)
        for doc in loader.load():
            docs.append(doc)
    return extract_combined_text(docs)

    # try:
    #     vector_store = InMemoryVectorStore.from_documents(docs, OpenAIEmbeddings())
    #     documents = vector_store.similarity_search(question)
    #     return extract_combined_text(documents)
    # except Exception as e:
    #     return f"An error occurred during similarity search: {e}"


# import os
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_core.vectorstores import InMemoryVectorStore
# from langchain_openai import OpenAIEmbeddings

# def extract_combined_text(pages):
#     return " ".join([page.page_content for page in pages])

# def web_database(question):
#     pages = [
#         "https://www.nadra.gov.pk",
#         "ns.nadra.gov.pk",
#         "ftp2.nadra.gov.pk",
#         "visa.nadra.gov.pk",
#         "smtp.nadra.gov.pk",
#         "vpn.nadra.gov.pk",
#         "owa.nadra.gov.pk",
#         "webmail.nadra.gov.pk",
#         "payment.nadra.gov.pk",
#         "ftp.nadra.gov.pk",
#         "www.nadra.gov.pk",
#         "mail.nadra.gov.pk",
#         "autodiscover.nadra.gov.pk",
#         "mail1.nadra.gov.pk",
#         "vpn2.nadra.gov.pk",
#         "test.nadra.gov.pk",
#         "dms.nadra.gov.pk",
#         "oma.nadra.gov.pk",
#         "mailtest.nadra.gov.pk",
#         "id.nadra.gov.pk",
#         "email.nadra.gov.pk",
#         "careers.nadra.gov.pk",
#         "ns1.nadra.gov.pk",
#         "nims.nadra.gov.pk",
#         "e-sahulat.nadra.gov.pk",
#         "ebil.nadra.gov.pk",
#         "supremecourt.nadra.gov.pk",
#         "succession.nadra.gov.pk",
#         "ehsaas.nadra.gov.pk",
#         "onlinemrp.nadra.gov.pk",
#         "ehsaaslabour.nadra.gov.pk",
#         "crms.nadra.gov.pk",
#         "cdcp.nadra.gov.pk",
#         "e-visa.nadra.gov.pk",
#         "esahulat-cms.nadra.gov.pk",
#         "nser.nadra.gov.pk",
#         "passport.nadra.gov.pk",
#         "poc.nadra.gov.pk"
#     ]
#     docs = []
#     for data in pages:
#         loader = WebBaseLoader(data)
#         for doc in loader.load():
#             docs.append(doc)
        
#     vector_store = InMemoryVectorStore.from_documents(docs,OpenAIEmbeddings())
#     documents = vector_store.similarity_search(question)
#     return extract_combined_text(documents)
