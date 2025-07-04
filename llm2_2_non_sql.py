import os
from openai import OpenAI
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import VectorStore

# ---------------------------------------------------------
# Load API Key from Environment (.env)
# ---------------------------------------------------------
load_dotenv()
OPENAI_API_KEY = ""
# ⚠️ Optional: Warn if API key not found
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API key. Please set it in your .env file as OPENAI_API_KEY.")

# ---------------------------------------------------------
# Initialize OpenAI Client
# ---------------------------------------------------------
client = OpenAI(api_key=OPENAI_API_KEY)


# ---------------------------------------------------------
# Initialize OpenAI Client
# ---------------------------------------------------------
client = OpenAI(api_key=OPENAI_API_KEY)


# ---------------------------------------------------------
# Respond to General (Non-SQL) Queries
# ---------------------------------------------------------
def respond_to_non_sql_query(user_query: str) -> str:
    """
    Handles general, lifestyle, or informational questions from students 
    that do not require data from the housing database, and also queries 
    related to lease terms or rules of specific apartments.
    
    Args:
        user_query (str): The raw input query from the user.

    Returns:
        str: A friendly, conversational response generated by OpenAI GPT-4o.
    """

    

    # For general queries, use GPT-4o to respond
    prompt = f"""
You are a helpful and knowledgeable assistant working for a student housing platform 
that supports CU Boulder students in finding housing and navigating student life.

You **do not** access any SQL database or return real-time property data. 
Instead, you respond to general, lifestyle, or informational queries about student housing.

Maintain a helpful, professional, and welcoming tone. If a query needs specific data, 
politely explain and suggest next steps.

---

DO Answer Generally:

User: Can you help me find a house?  
Assistant: Yes! I’d love to help. Can you share your budget, preferred location, and room type?

User: Is WiFi usually included in student housing?  
Assistant: Most CU Boulder student apartments include WiFi, especially furnished ones. Still, always double-check the listing.

User: What does a lease typically include?  
Assistant: Leases often cover rent, deposit, rules on pets, maintenance, and termination. Need help with a specific clause?

---

DO NOT Attempt Data-Based Tasks:

User: What’s the rent for “GradHome Suites”?  
Assistant: I don’t have live data, but I can help you estimate typical rents in that area. Would you like that?

User: Show me available listings.  
Assistant: I can’t access listings directly, but I can help you narrow down what to search for and where.

---

User Question:  
{user_query}

Answer:
"""

    # Generate completion using GPT-4o
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a friendly and informed guide for CU Boulder student housing questions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()

# ---------------------------------------------------------
# Search Lease Documents in the Vector Store
# ---------------------------------------------------------
def search_lease_documents(query: str) -> str:
    """
    Searches the Chroma vector store for documents related to lease terms, policies, and other rules.
    
    Args:
        query (str): The user's query related to lease terms.

    Returns:
        str: The most relevant lease details found in the vector store.
    """
    # Search the vector store for the query and retrieve relevant documents
    results = vectordb.similarity_search(query, k=3)
    
    if results:
        # Join the top results for clarity and relevance
        lease_details = "\n\n".join([result.page_content for result in results])
        return lease_details
    else:
        return "Sorry, I couldn't find any relevant lease documents for your query."