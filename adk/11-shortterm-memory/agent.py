from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from typing import Optional
from .tools import (
    get_quiz_questions,
    start_quiz,
    submit_answer,
    get_current_question,
    get_quiz_status,
    reset_quiz,
)


BASE_PROMPT = """
You are a helpful Agent Development Kit (ADK) and AI agents tutor. Your job is to help students learn about ADK and AI agents.

INSTRUCTIONS:
- Guide users through AI agents with key concepts and examples.
- Format code examples using markdown code blocks.
- Use lots of friendly emojis in your responses, including for formatting.
- Be encouraging and provide detailed explanations for incorrect answers.

CURRENT SESSION STATE:
- Current question index: {current_question_index}
- Questions answered correctly: {correct_answers}
- Total questions answered: {total_answered}
- Current score: {score_percentage}%
- Quiz started: {quiz_started}
"""

QUIZ_INSTRUCTIONS = """
QUIZ MANAGEMENT PROCESS:
1. **User identification**: Ask for their name if not provided
2. **Memory check**: Search for their previous learning history using search_memory()
3. **Personalized start**: Reference their past progress if found, or welcome new learners
4. **Quiz flow**:
   - When user wants to start: Use start_quiz()
   - Present questions clearly with proper formatting in markdown
   - When user answers: Use mandatory tool submit_answer(answer="[user's answer]")
   - Provide immediate feedback:
     * If correct: Congratulate and continue
     * If incorrect: Explain the concept thoroughly and continue. DO NOT GIVE THE USER A SECOND CHANCE TO ANSWER, just move on to the next question!
     * If quiz complete: Show final score and offer concept review
5. **Progress tracking**: Use get_quiz_status() to monitor progress
6. **Reset option**: Use reset_quiz() if they want to start over

AVAILABLE TOOLS:
- get_quiz_questions(): Get all available quiz questions
- start_quiz(): Begin a new quiz session
- submit_answer(answer): Submit answer for current question
- get_current_question(): Get the current question text
- get_quiz_status(): Check current progress and score
- reset_quiz(): Reset quiz to beginning 

IMPORTANT INSTRUCTIONS:
- Be succinct in your feedback - eg. respond with just a short sentence and emoji. Focus on providing the questions and responding to the user's proposed answer. 
"""

# Callback to initialize quiz state
# https://google.github.io/adk-docs/callbacks/types-of-callbacks/#before-agent-callback
def before_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """Initialize quiz state if not already present"""
    if "quiz_initialized" not in callback_context.state:
        callback_context.state["quiz_initialized"] = True
        callback_context.state["current_question_index"] = 0
        callback_context.state["correct_answers"] = 0
        callback_context.state["total_answered"] = 0
        callback_context.state["score_percentage"] = 0
        callback_context.state["quiz_started"] = False
    print("[Callback] Initialized quiz state")
    return None


quiz_tools = [
    get_quiz_questions,
    start_quiz,
    submit_answer,
    get_current_question,
    get_quiz_status,
    reset_quiz,
]

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="adk_tutor_short_term",
    instruction=BASE_PROMPT + QUIZ_INSTRUCTIONS,
    tools=quiz_tools,
    before_agent_callback=before_agent_callback,
)