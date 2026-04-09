from crewai import Agent
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

researcher = Agent(
    role="Researcher",
    goal="Create structured outlines for blog topics",
    backstory="You are an expert content researcher who analyzes topics and creates clear, actionable outlines for blog posts.",
    llm=llm,
    verbose=False,
    allow_delegation=False
)

writer = Agent(
    role="Writer",
    goal="Expand outlines into full blog post drafts",
    backstory="You are a skilled blog writer who takes research outlines and transforms them into engaging, readable blog content.",
    llm=llm,
    verbose=False,
    allow_delegation=False
)

editor = Agent(
    role="Editor",
    goal="Refine and polish blog drafts into final publications",
    backstory="You are an experienced editor who improves clarity, flow, and quality of blog posts for publication.",
    llm=llm,
    verbose=False,
    allow_delegation=False
)