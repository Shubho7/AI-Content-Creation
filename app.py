import streamlit as st
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os

load_dotenv()

serper_api_key = os.getenv("SERPER_API_KEY")

#streamlit ui
st.set_page_config(page_title="AI-Content-Creation", page_icon=":robot_face:", layout="wide")
st.title("We write it all! 😁")
st.markdown("Built with CrewAI")
st.markdown("---")

with st.sidebar:
    topic = st.text_area("What can I help with? 👀", height=80, placeholder="Enter your topic here")
    st.markdown("---")
    generate_button = st.button("Generate content", type="primary", use_container_width=True)

def generate_content(topic):
    llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.5
    )

    websearch_tool = SerperDevTool(n=10)

    ## Agents
    research_analyst_agent = Agent(
        role="Senior Research Analyst",
        goal="Research, analyze and summarize comprehensive information on {topic} from reliable web sources.",
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

    content_writer_agent = Agent(
        role="Content Writer",
        goal="Write a detailed engaging article on {topic} based on the research provided by the research analyst while maintaining accuracy.",
        backstory="You are a skilled content writer with 10 years of experience in writing engaging content from research reports."
                "You have a deep understanding of the audience and their interests. You have a strong command of english"
                "language, grammar, and style. You work closely with the research analyst to transform complex research"
                "findings into well-structured article that is easy to read and understand ensuring all the facts, data,"
                "references and citations from the research report are incorporated. Your writing is clear, engaging and tailored.",
        allow_delegation=False,
        verbose=True,
        llm=llm
    )


    ## Tasks
    research_task = Task(
        description=(
            "1. Conduct comprehensive research on {topic} from reliable web sources."
            "2. Evaluate source credibility, fact check and cross-reference information."
            "3. Identify key insights, trends, statistics, and relevant data."
            "4. Summarize complex information with clarity including facts and proper citations."
        ), 
        expected_output=(
            "A detailed research report on {topic} with key insights, trends, statistics, and relevant data. It should include:"
            "- Summary of key findings and insights."
            "- Comprehensive analysis of current trends and developments."
            "- Relevant statistics, data, and certified facts."
            "- All citations and links to original sources."
            "- Clear categorization of themes and patterns."
            "- Clear and engaging writing style."
            "Format with clear sections, proper headings, subheadings, bullet points, and citations."
        ),
        agent=research_analyst_agent
    )

    writing_task = Task(
        description=(
            "Using the research report provided, write an engaging blog post on {topic} that -"
            "1. Maintains all factual accuracy and citations from the research. It should have:"
                "- Attention-grabbing introduction"
                "- Well-structured body sections with proper headings, sub-headings and bullet points"
                "- Compelling conclusion"
            "2. Preserve all source citations in [Source: URL] format"
            "3. Include a References section at the end"
            "4. Summarize complex information with clarity including facts and proper citations"
        ), 
        expected_output=(
            "A polished article in markdown format that -" 
            "1. Engages readers while maintaining accuracy"
            "2. Contains properly structured sections"
            "3. Includes inline citations hyperlinked to the original source url"
            "4. Presents information in an accessible yet informative way"
            "5. Follows proper markdown formatting, use H1 for the title and H3 for the sub-headings"
        ),
        agent=content_writer_agent
    )


    # Crew
    crew = Crew(
        agents=[research_analyst_agent, content_writer_agent],
        tasks=[research_task, writing_task]
    )


    return crew.kickoff(inputs={"topic": topic})


# Streamlit UI
if generate_button:
    with st.spinner("Researching...Writing..."):
        try:
            result = generate_content(topic)
            st.markdown("Here you go! 😎")
            st.markdown(result)

            st.download_button(
                label="Download ➡️",
                data=result.raw,
                file_name=f"{topic.lower().replace(' ', '_')}_article.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"An error occurred: {e}")