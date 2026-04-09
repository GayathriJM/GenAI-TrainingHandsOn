from crewai import Task
from agents import researcher, writer, editor

research_task = Task(
    description="""
    Act like a professional content researcher. Your objective is to create a clear, structured outline for a blog post on the given topic: {topic}.

    Steps:
    1. Analyze the topic for key themes and audience value.
    2. Identify 3-5 main sections (e.g., Introduction, Key Points, Conclusion).
    3. For each section, list 2-3 bullet points with specific ideas or talking points.

    Output Format: Return only a bullet-point outline with section headers. No introductory text or explanations.
    Example:
    - Introduction
      - Hook with surprising fact
      - State the main thesis
    - Main Body
      - Point 1 with example
      - Point 2 with data
    """,
    agent=researcher,
    expected_output="A bullet-point outline for the blog topic."
)

write_task = Task(
    description="""
    Act like a skilled blog writer. Your objective is to expand the provided outline into a full, engaging blog post draft.

    The outline is: {outline}

    Steps:
    1. Use the outline as your structure guide.
    2. Write an introduction paragraph based on the intro bullets.
    3. Expand each body section into 1-2 paragraphs with details and examples.
    4. End with a conclusion paragraph that summarizes and calls to action.

    Output Format: Return the full blog post as plain text with section headers (e.g., ## Introduction). Keep it 400-600 words. No meta-comments.
    """,
    agent=writer,
    expected_output="A full blog post draft based on the outline."
)

edit_task = Task(
    description="""
    Act like an experienced blog editor. Your objective is to refine and polish the draft into a publication-ready blog post.

    The draft is: {draft}

    Steps:
    1. Read the draft and identify areas for improvement (clarity, flow, grammar).
    2. Enhance readability: shorten sentences, improve transitions, add engaging language.
    3. Ensure the post is cohesive, error-free, and engaging for readers.
    4. Maintain the original structure but elevate the quality.

    Output Format: Return the final blog post as plain text with section headers. Include a title at the top. No notes about changes made.
    """,
    agent=editor,
    expected_output="The final polished blog post."
)