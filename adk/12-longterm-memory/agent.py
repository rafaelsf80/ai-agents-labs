import os
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.memory import VertexAiMemoryBankService
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

from .memory import search_memory, set_user_name

# Note - bracket {} syntax grabs variables from session state.
# https://google.github.io/adk-docs/sessions/state/#using-key-templating
# This state gets dynamically injected with each turn, and the updated prompt is then passed to the agent's model.
BASE_PROMPT = """
You are a helpful Python programming tutor. Your job is to help students learn about Python dictionaries.

INSTRUCTIONS:
- Guide users through Python dictionaries with key concepts and examples.
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

MEMORY_INSTRUCTIONS = """
You have long-term memory. Your job is to help students learn about Python dictionaries, and you can remember their progress across sessions.

MEMORY INSTRUCTIONS:
- **First interaction**: Always ask for the user's name so you can personalize their learning experience and remember their progress.
- When users return, search your memory to recall their previous progress and areas they struggled with.
- When a user introduces themselves, use search_memory(query={user_name}) to recall their history. If other students' histories show up, ignore it.
- Use memory insights to provide targeted help and encouragement
- When a user completes the quiz, make sure to store the score % in memory.

MEMORY TOOLS:
- search_memory(query): Search past learning sessions. IMPORTANT: the search query should be state.user_name , aka {user_name}
- set_user_name(name): Set the user's name in the state for memory tracking.

PERSONALIZATION EXAMPLES:
- "Welcome back, [Name]! I remember you scored [X]% last time and had some trouble with [topic]. Let's work on that!"
- "Great to see you again! You've been making steady progress with dictionaries."
- "I notice this is your first time learning about dictionaries. Let's start with the basics!"
"""

QUIZ_INSTRUCTIONS = """
QUIZ MANAGEMENT PROCESS:
1. **User identification**: Ask for their name if not provided
2. **Memory check**: Search for their previous learning history using search_memory()
3. **Personalized start**: Reference their past progress if found, or welcome new learners
4. **Quiz flow**:
   - When user wants to start: Use start_quiz()
   - Present questions clearly with proper formatting
   - When user answers: Use submit_answer(answer="[user's answer]")
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

# Callback to initialize quiz state and detect username
def before_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """Initialize quiz state and detect user name from messages"""
    state = callback_context.state
    if "quiz_initialized" not in callback_context.state:
        callback_context.state["quiz_initialized"] = True
        callback_context.state["current_question_index"] = 0
        callback_context.state["correct_answers"] = 0
        callback_context.state["total_answered"] = 0
        callback_context.state["score_percentage"] = 0
        callback_context.state["quiz_started"] = False
        callback_context.state["user_name"] = None
    print("[Callback] Initialized quiz state")

    # Try to extract user name from the current message if we don't have it yet
    if state.get("user_name") is None:
        # Get the current user message from the invocation context
        if hasattr(callback_context, "_invocation_context"):
            inv_ctx = callback_context._invocation_context

            # Check if there's a current user message
            if hasattr(inv_ctx, "user_message") and inv_ctx.user_message:
                user_text = (
                    inv_ctx.user_message.text.lower()
                    if hasattr(inv_ctx.user_message, "text")
                    else ""
                )

                # Look for name patterns
                name_patterns = [
                    "my name is ",
                    "i'm ",
                    "i am ",
                    "call me ",
                    "name's ",
                    "this is ",
                    "it's ",
                ]

                for pattern in name_patterns:
                    if pattern in user_text:
                        parts = user_text.split(pattern, 1)
                        if len(parts) > 1:
                            # Extract the name part
                            remaining_text = parts[1]
                            # Take first word after pattern
                            name_part = (
                                remaining_text.split()[0]
                                if remaining_text.split()
                                else ""
                            )

                            # Clean up punctuation
                            name_part = (
                                name_part.replace(".", "")
                                .replace(",", "")
                                .replace("!", "")
                                .replace("?", "")
                                .replace("'", "")
                                .replace('"', "")
                            )

                            # Basic validation - ensure it's a valid name
                            if name_part and len(name_part) > 1 and name_part.isalpha():
                                state["user_name"] = name_part.lower()
                                print(
                                    f"🎯 Detected and set user name: {state['user_name']}"
                                )
                                break

    return None


# Source: https://github.com/serkanh/adk-with-memorybank/blob/main/agents/memory_assistant/agent.py
async def auto_save_to_memory_callback(callback_context):
    """Automatically save completed sessions to memory bank using default session user_id"""
    try:
        session_id = None

        # Extract session information from invocation context
        if hasattr(callback_context, "_invocation_context"):
            inv_ctx = callback_context._invocation_context

            # Extract session ID
            if hasattr(inv_ctx, "session") and hasattr(inv_ctx.session, "id"):
                session_id = inv_ctx.session.id

        # Get the session from the invocation context
        session = callback_context._invocation_context.session

        if not session_id:
            return

        # Initialize memory service
        agent_engine_id = os.getenv("AGENT_ENGINE_ID")
        if not agent_engine_id:
            return

        memory_service = VertexAiMemoryBankService(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
            agent_engine_id=agent_engine_id,
        )

        # Check if session has meaningful content
        has_content = False
        content_count = 0

        if hasattr(session, "events") and session.events:
            content_count = len(session.events)
            has_content = content_count >= 2  # At least user message + agent response
        elif hasattr(session, "contents") and session.contents:
            content_count = len(session.contents)
            has_content = content_count >= 2

        if not has_content:
            return

        await memory_service.add_session_to_memory(session)
        print(f"🧠 Session auto-saved to memory bank")

    except Exception as e:
        print(f"⚠️ Error auto-saving to memory: {e}")


enhanced_quiz_tools = [
    get_quiz_questions,
    start_quiz,
    submit_answer,
    get_current_question,
    get_quiz_status,
    reset_quiz,
    search_memory,
    set_user_name,
]

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="python_tutor_long_term",
    instruction=BASE_PROMPT + MEMORY_INSTRUCTIONS + QUIZ_INSTRUCTIONS,
    tools=enhanced_quiz_tools,
    before_agent_callback=before_agent_callback,
    after_agent_callback=auto_save_to_memory_callback,
)