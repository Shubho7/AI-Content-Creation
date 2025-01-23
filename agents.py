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

# Agent 2
content_writer_agent = Agent(
    role="Content Writer",
    goal=f"Write a detailed engaging article on {topic} based on the research provided by the research analyst while maintaining accuracy.",
    backstory="You are a skilled content writer with 10 years of experience in writing engaging content from research reports."
              "You have a deep understanding of the audience and their interests. You have a strong command of english"
              "language, grammar, and style. You work closely with the research analyst to transform complex research"
              "findings into well-structured article that is easy to read and understand ensuring all the facts, data,"
              "references and citations from the research report are incorporated. Your writing is clear, engaging and tailored.",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

