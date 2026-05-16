#!/usr/bin/env python
# coding: utf-8

# In[25]:


from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY
)

chat_history = []

prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a helpful Indian language learning assistant.

Help users learn Indian languages through:
- simple explanations
- real-life phrases
- pronunciation
- meaning
- cultural context

Answer clearly and shortly.
"""),
    ("human", """
Chat history:
{chat_history}

User question:
{question}
""")
])

chain = prompt | llm

def ask(question):
    global chat_history

    history_text = "\n".join(chat_history)

    result = chain.invoke({
        "chat_history": history_text,
        "question": question
    })

    answer = result.content

    chat_history.append(f"User: {question}")
    chat_history.append(f"Assistant: {answer}")

    return answer


# In[27]:


print(ask("how to say thank you in bengali"))


# In[12]:


from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.5
)

# embeddings = GoogleGenerativeAIEmbeddings(
#     model="models/text-embedding-004",
#     google_api_key=GOOGLE_API_KEY
# )

from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

knowledge_docs = [
    Document(page_content="""
Feature: Native speaker connection
The app should connect learners with native speakers based on target language,
known language, interests, availability, and learning goal.
Example: A Hindi speaker learning Bengali can be matched with a Bengali speaker learning Hindi.
"""),

    Document(page_content="""
Feature: Short daily conversation
The app should encourage 5 to 10 minute daily conversations instead of long grammar lessons.
Conversation topics can include greetings, travel, shopping, friendship, food, festivals, and daily life.
"""),

    Document(page_content="""
Feature: Cultural exchange
The app should explain cultural context behind phrases, greetings, festivals, food habits,
regional etiquette, and polite expressions.
"""),

    Document(page_content="""
Bengali formal greeting:
Phrase: Nomoshkar
Script: নমস্কার
Meaning: Hello / respectful greeting
Pronunciation: no-mo-shkar
Use with elders, teachers, strangers, or formal situations.
"""),

    Document(page_content="""
Bengali casual greeting:
Phrase: Ki khobor?
Script: কী খবর?
Meaning: What's up? / How are things?
Pronunciation: kee kho-bor
Use with friends or people your age.
"""),

    Document(page_content="""
Bengali shopping phrase:
Phrase: Eta koto daam?
Script: এটা কত দাম?
Meaning: How much does this cost?
Pronunciation: eta ko-to daam
Use in shops or local markets.
"""),

    Document(page_content="""
Hindi greeting:
Phrase: Namaste
Script: नमस्ते
Meaning: Hello / respectful greeting
Pronunciation: na-mas-te
Use respectfully with anyone.
"""),

    Document(page_content="""
Reward system:
Users can earn points, streaks, badges, and level progress for daily practice,
completing conversations, helping other learners, and learning real-life phrases.
""")
]

vector_db = FAISS.from_documents(knowledge_docs, embedding)

chat_history = []
user_progress = {
    "points": 0,
    "sessions": 0,
    "phrases_learned": []
}

prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are VibeLingo, a conversational Indian language learning assistant.

Your app goal:
Help people learn another Indian language through real conversations,
native speaker practice, short daily sessions, cultural exchange, and real-life phrases.

Use the retrieved context when relevant.
If the user asks something outside the knowledge base, still answer generally,
but guide the conversation back to language learning when appropriate.

You can help with:
- Bengali, Hindi, Tamil, Telugu, Marathi, Gujarati, Punjabi, Malayalam, Kannada, Odia, Assamese
- greetings
- travel phrases
- shopping phrases
- friendship conversations
- pronunciation
- cultural context
- daily practice tasks
- native speaker matching suggestions
- progress motivation

Keep answers short, practical, and beginner-friendly.

When teaching a phrase, use this format:

Phrase:
Script:
Meaning:
Pronunciation:
When to use:
Practice:
"""),
    ("human", """
Retrieved context:
{context}

Chat history:
{chat_history}

User progress:
{progress}

User question:
{question}
""")
])

chain = prompt | llm


def ask(question):
    global chat_history, user_progress

    docs_with_score = vector_db.similarity_search_with_score(question, k=3)

    context_parts = []
    for doc, score in docs_with_score:
        if score < 1.0:
            context_parts.append(doc.page_content)

    if context_parts:
        context = "\n\n".join(context_parts)
    else:
        context = "No exact knowledge base match found. Answer using general Indian language learning knowledge."

    history_text = "\n".join(chat_history[-8:])

    result = chain.invoke({
        "context": context,
        "chat_history": history_text,
        "progress": str(user_progress),
        "question": question
    })

    answer = result.content

    user_progress["sessions"] += 1
    user_progress["points"] += 5

    chat_history.append(f"User: {question}")
    chat_history.append(f"Assistant: {answer}")

    return answer


def show_progress():
    return user_progress


def suggest_match(user_language, target_language, interest):
    return f"""
Suggested match:
A native {target_language} speaker who wants to learn {user_language}
and is interested in {interest}.

Conversation idea:
Start with greetings, then discuss {interest} using simple daily phrases.
"""


def daily_practice(target_language, topic):
    question = f"Give me a 5 minute daily conversation practice in {target_language} about {topic}"
    return ask(question)


# In[13]:


print(ask("Teach me how to greet someone in Bengali"))


# In[7]:


print(ask("Give me a shopping conversation in Bengali"))


# In[9]:


from dotenv import load_dotenv
import os
from datetime import date

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.5
)

users = [
    {
        "name": "Rahul",
        "native_language": "Bengali",
        "learning_language": "Hindi",
        "interests": ["travel", "food", "friendship"],
        "mode": ["text", "voice"]
    },
    {
        "name": "Priya",
        "native_language": "Hindi",
        "learning_language": "Bengali",
        "interests": ["shopping", "culture", "festivals"],
        "mode": ["text"]
    }
]

user_progress = {
    "points": 0,
    "streak": 0,
    "sessions_completed": 0,
    "phrases_learned": [],
    "last_practice_date": None
}

chat_history = []

prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are VibeLingo, an Indian language learning assistant.

Your job is to support these 8 app features:
1. Connect learners with native speakers
2. Encourage short daily conversation sessions
3. Match users based on language interests
4. Reward consistent participation and practice
5. Support voice and text communication
6. Track learning progress informally
7. Promote cultural exchange between regions
8. Highlight commonly used real-life phrases

Keep answers short, practical, beginner-friendly, and focused on real conversation.
"""),
    ("human", """
Chat history:
{chat_history}

User question:
{question}
""")
])

chain = prompt | llm


# Feature 1 + 3: Connect and match learners
def match_native_speaker(user_name, native_language, learning_language, interests):
    matches = []

    for user in users:
        if (
            user["native_language"].lower() == learning_language.lower()
            and user["learning_language"].lower() == native_language.lower()
        ):
            common_interests = set(interests).intersection(set(user["interests"]))

            matches.append({
                "name": user["name"],
                "native_language": user["native_language"],
                "learning_language": user["learning_language"],
                "common_interests": list(common_interests),
                "communication_mode": user["mode"]
            })

    if not matches:
        return "No perfect match found right now. Try changing interests or language."

    return matches


# Feature 2: Short daily conversation
def daily_conversation(language, topic):
    question = f"""
Create a short 5-minute beginner conversation practice in {language}
about {topic}. Include meaning and pronunciation.
"""
    return ask(question)


# Feature 4: Reward consistent practice
def reward_user():
    user_progress["points"] += 10
    user_progress["sessions_completed"] += 1

    today = str(date.today())

    if user_progress["last_practice_date"] != today:
        user_progress["streak"] += 1
        user_progress["last_practice_date"] = today

    return {
        "message": "Practice completed. You earned 10 points.",
        "points": user_progress["points"],
        "streak": user_progress["streak"],
        "sessions_completed": user_progress["sessions_completed"]
    }


# Feature 5: Voice and text support
def communication_mode(mode, message):
    if mode.lower() == "voice":
        return f"Voice mode selected. Convert this speech to text first, then process: {message}"
    elif mode.lower() == "text":
        return ask(message)
    else:
        return "Please choose voice or text mode."


# Feature 6: Track learning progress
def show_progress():
    return user_progress


# Feature 7: Cultural exchange
def cultural_exchange(language, topic):
    question = f"""
Explain the cultural context of {topic} in {language}-speaking regions.
Give simple examples for a beginner learner.
"""
    return ask(question)


# Feature 8: Real-life phrases
def real_life_phrases(language, situation):
    question = f"""
Give commonly used real-life {language} phrases for {situation}.
Include script, pronunciation, meaning, and when to use.
"""
    return ask(question)


# Main conversational assistant
def ask(question):
    global chat_history

    history_text = "\n".join(chat_history[-8:])

    result = chain.invoke({
        "chat_history": history_text,
        "question": question
    })

    answer = result.content

    chat_history.append(f"User: {question}")
    chat_history.append(f"Assistant: {answer}")

    return answer


# In[10]:


print(match_native_speaker(
    user_name="Reshav",
    native_language="Hindi",
    learning_language="Bengali",
    interests=["food", "travel"]
))


# In[11]:


print(daily_conversation("Bengali", "shopping"))

