from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from groq import Groq

import os
from dotenv import load_dotenv
load_dotenv()

# Tool 1
llm = Groq(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.1-8b-instant", temperature=0.5)

# Tool 2
websearch_tool = SerperDevTool(n=5)

# Agent 1
research_analyst_agent = Agent(
    role="Senior Research Analyst",
    goal=f"Research, analyze and summarize comprehensive information on {topic} from reliable web sources.",
    backstory="You are an expert with 10 years of experience in research and analysis. You have a keen eye for" 
              "detail and can quickly identify key insights and right information from a variety of sources across"
              "the web using search tools. You are skilled at distinguishing between credible and unreliable sources," 
              "fact checking, cross referencing information, identifying key insights and can summarize complex information"
              "with clarity. You provide well organized research reports with proper citations with source verification."
              "Your analysis includes both raw data and interpreted insights.",
    allow_delegation=False,
    verbose=True,
    tools=[websearch_tool],
    llm=llm
)


