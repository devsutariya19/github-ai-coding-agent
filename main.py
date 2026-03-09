from dotenv import load_dotenv
import os

# https://docs.langchain.com/oss/python/integrations/text_embedding/google_generative_ai
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

# https://docs.langchain.com/oss/python/integrations/vectorstores/astradb
from langchain_astradb import AstraDBVectorStore

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain import hub

from github import fetch_github_issues
from note import note_tool

load_dotenv()

def connect_to_vstore():
  embeddings = GoogleGenerativeAIEmbeddings(model = "gemini-embedding-001")
  ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
  ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
  desired_namespace = os.getenv("ASTRA_DB_KEYSPACE")
  
  if desired_namespace:
    ASTRA_DB_KEYSPACE = desired_namespace
  else:
    ASTRA_DB_KEYSPACE = None

  vstore = AstraDBVectorStore(
    embedding = embeddings,
    collection_name = "github",
    api_endpoint = ASTRA_DB_API_ENDPOINT,
    token = ASTRA_DB_APPLICATION_TOKEN,
    namespace = ASTRA_DB_KEYSPACE
  )

  return vstore

vstore = connect_to_vstore()

# Refresh the vector store with GitHub issues
add_to_vectorstore = input("Do you want to add GitHub issues to the vector store? (y/N): ").lower() in ['y', 'yes']
if add_to_vectorstore:
  issues = fetch_github_issues("facebook", "docusaurus")

  try:
    vstore.delete_collection()
  except:
    pass

  vstore = connect_to_vstore()
  vstore.add_documents(issues)

  # results = vstore.similarity_search("accessibility", k=3)
  # for res in results:
  #   print(f"* {res.page_content} {res.metadata}")

# Create a retriever tool for the agent
retriever = vstore.as_retriever(search_kwargs={"k": 3})
retriever_tool = create_retriever_tool(
  retriever,
  "github_search",
  "Search for information about github issues. For any questions about github issues, use this tool to search for relevant information."                                      
)

# Create the agent and executor
prompt = ChatPromptTemplate.from_messages([
  (
    "system",
    "You are a helpful AI assistant."
    "Use the provided tools to answer questions when necessary."
  ),
  MessagesPlaceholder("chat_history", optional=True),
  ("human", "{input}"),
  MessagesPlaceholder("agent_scratchpad"),
])
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

tools = [retriever_tool, note_tool]
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Ask Questions
while (question := input("Ask a question about github issues (q to quit): ")) != "q":
  result = agent_executor.invoke({"input": question})
  print(result["output"])

