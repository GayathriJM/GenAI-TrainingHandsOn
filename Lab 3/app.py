import streamlit as st
from crewai import Crew, Process
from agents import researcher, writer, editor
from tasks import research_task, write_task, edit_task
import os
from dotenv import load_dotenv
import time

load_dotenv()

# Check if API key is set
if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "your_openai_api_key_here":
    st.error("Please set your OPENAI_API_KEY in the .env file.")
    st.stop()

# Custom CSS for colors and styling
st.markdown("""
<style>
    .main-title {
        color: #4CAF50;
        font-size: 3em;
        text-align: center;
        font-weight: bold;
    }
    .subtitle {
        color: #2196F3;
        text-align: center;
        font-size: 1.2em;
    }
    .research-section {
        background-color: #E8F5E8;
        padding: 10px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
    .writer-section {
        background-color: #FFF3E0;
        padding: 10px;
        border-radius: 10px;
        border-left: 5px solid #FF9800;
    }
    .editor-section {
        background-color: #F3E5F5;
        padding: 10px;
        border-radius: 10px;
        border-left: 5px solid #9C27B0;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 1.2em;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stTextInput>div>div>input {
        font-size: 1.1em;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🚀 CrewAI Blog Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Generate blog posts using a 3-agent team: Researcher, Writer, and Editor.</p>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    topic = st.text_input("Enter blog topic", placeholder="e.g., Benefits of AI in Healthcare", key="topic_input")

with col2:
    regenerate_final = st.checkbox("🔄 Regenerate only final blog", help="Skip research and writing, re-edit the previous draft")

if st.button("✨ Generate Blog"):
    if not topic.strip():
        st.error("❌ Please enter a blog topic.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with st.spinner("🤖 Agents are working..."):
            try:
                # Step 1: Research
                status_text.text("🔍 Researcher is gathering ideas...")
                progress_bar.progress(10)
                time.sleep(0.5)  # Simulate progress
                
                if not regenerate_final:
                    research_crew = Crew(agents=[researcher], tasks=[research_task], process=Process.sequential)
                    outline_result = research_crew.kickoff(inputs={"topic": topic})
                    outline = outline_result.raw
                    st.session_state.outline = outline
                else:
                    if "outline" not in st.session_state:
                        st.error("No previous outline found. Please generate from scratch first.")
                        st.stop()
                    outline = st.session_state.outline

                progress_bar.progress(30)
                status_text.text("✍️ Writer is drafting the blog...")
                time.sleep(0.5)

                # Step 2: Writing
                if not regenerate_final:
                    write_crew = Crew(agents=[writer], tasks=[write_task], process=Process.sequential)
                    draft_result = write_crew.kickoff(inputs={"topic": topic, "outline": outline})
                    draft = draft_result.raw
                    st.session_state.draft = draft
                else:
                    if "draft" not in st.session_state:
                        st.error("No previous draft found. Please generate from scratch first.")
                        st.stop()
                    draft = st.session_state.draft

                progress_bar.progress(70)
                status_text.text("✨ Editor is polishing the final blog...")
                time.sleep(0.5)

                # Step 3: Editing
                edit_crew = Crew(agents=[editor], tasks=[edit_task], process=Process.sequential)
                final_result = edit_crew.kickoff(inputs={"topic": topic, "draft": draft})
                final_blog = final_result.raw
                st.session_state.final_blog = final_blog

                progress_bar.progress(100)
                status_text.text("✅ Blog generation complete!")
                time.sleep(1)
                progress_bar.empty()
                status_text.empty()

                st.success("🎉 Your blog is ready!")

                # Display results with colors
                st.markdown("### 📊 Agent Outputs")
                
                with st.expander("🔍 Research Outline", expanded=True):
                    st.markdown('<div class="research-section">', unsafe_allow_html=True)
                    st.markdown(st.session_state.outline)
                    st.markdown('</div>', unsafe_allow_html=True)

                with st.expander("✍️ Draft Blog", expanded=True):
                    st.markdown('<div class="writer-section">', unsafe_allow_html=True)
                    st.markdown(st.session_state.draft)
                    st.markdown('</div>', unsafe_allow_html=True)

                with st.expander("✨ Final Edited Blog", expanded=True):
                    st.markdown('<div class="editor-section">', unsafe_allow_html=True)
                    st.markdown(st.session_state.final_blog)
                    st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("💡 Make sure your OpenAI API key is valid and you have credits.")

# Display previous results if available
if "outline" in st.session_state:
    st.markdown("---")
    st.subheader("📚 Previous Results")
    with st.expander("🔍 Last Research Outline"):
        st.markdown('<div class="research-section">', unsafe_allow_html=True)
        st.markdown(st.session_state.outline)
        st.markdown('</div>', unsafe_allow_html=True)
    if "draft" in st.session_state:
        with st.expander("✍️ Last Draft Blog"):
            st.markdown('<div class="writer-section">', unsafe_allow_html=True)
            st.markdown(st.session_state.draft)
            st.markdown('</div>', unsafe_allow_html=True)
    if "final_blog" in st.session_state:
        with st.expander("✨ Last Final Blog"):
            st.markdown('<div class="editor-section">', unsafe_allow_html=True)
            st.markdown(st.session_state.final_blog)
            st.markdown('</div>', unsafe_allow_html=True)