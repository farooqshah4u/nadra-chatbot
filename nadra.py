import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

def extract_combined_text(pages):
    return " ".join([page.page_content for page in pages])

def web_database(question):
    pages = [
        "https://www.nadra.gov.pk",
        "ns.nadra.gov.pk",
        "ftp2.nadra.gov.pk",
        "visa.nadra.gov.pk",
        "smtp.nadra.gov.pk",
        "vpn.nadra.gov.pk",
        "owa.nadra.gov.pk",
        "webmail.nadra.gov.pk",
        "payment.nadra.gov.pk",
        "ftp.nadra.gov.pk",
        "www.nadra.gov.pk",
        "mail.nadra.gov.pk",
        "autodiscover.nadra.gov.pk",
        "mail1.nadra.gov.pk",
        "vpn2.nadra.gov.pk",
        "test.nadra.gov.pk",
        "dms.nadra.gov.pk",
        "oma.nadra.gov.pk",
        "mailtest.nadra.gov.pk",
        "id.nadra.gov.pk",
        "email.nadra.gov.pk",
        "careers.nadra.gov.pk",
        "ns1.nadra.gov.pk",
        "nims.nadra.gov.pk",
        "e-sahulat.nadra.gov.pk",
        "ebil.nadra.gov.pk",
        "supremecourt.nadra.gov.pk",
        "succession.nadra.gov.pk",
        "ehsaas.nadra.gov.pk",
        "onlinemrp.nadra.gov.pk",
        "ehsaaslabour.nadra.gov.pk",
        "crms.nadra.gov.pk",
        "cdcp.nadra.gov.pk",
        "e-visa.nadra.gov.pk",
        "esahulat-cms.nadra.gov.pk",
        "nser.nadra.gov.pk",
        "passport.nadra.gov.pk",
        "poc.nadra.gov.pk"
    ]
    docs = []
    for data in pages:
        loader = WebBaseLoader(data)
        for doc in loader.load():
            docs.append(doc)
        
    vector_store = InMemoryVectorStore.from_documents(docs,OpenAIEmbeddings())
    documents = vector_store.similarity_search(question)
    return extract_combined_text(documents)
