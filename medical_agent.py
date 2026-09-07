import os

from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain_core.tools import tool
from langchain.agents import create_agent

load_dotenv()

# -----------------------------
# OpenRouter Model
# -----------------------------

model = ChatOpenRouter(
    model="openai/gpt-5-mini",
    temperature=0,
    max_tokens=1000
)


# -----------------------------
# Medical Information Tool
# -----------------------------

@tool
def medical_information(query: str) -> str:
    """
    Provides general educational information
    about common medical conditions.
    """

    medical_data = {

        "fever": """
        Fever is an increase in body temperature that can occur
        due to infections or other conditions.

        Common symptoms include:
        - Increased body temperature
        - Chills
        - Sweating
        - Headache
        - Weakness

        Rest and adequate fluid intake may help with mild illness.
        Persistent or severe fever should be evaluated by a
        healthcare professional.
        """,

        "cold": """
        The common cold is generally a viral infection.

        Common symptoms include:
        - Runny nose
        - Sneezing
        - Sore throat
        - Cough
        - Mild fever

        Rest and adequate fluid intake can help recovery.
        """,

        "headache": """
        Headaches can have many causes including stress,
        dehydration, lack of sleep, illness and eye strain.

        Rest and hydration may help.
        A sudden or extremely severe headache requires
        medical evaluation.
        """,

        "dehydration": """
        Dehydration occurs when the body loses more fluid
        than it takes in.

        Common symptoms include:
        - Thirst
        - Dry mouth
        - Weakness
        - Dizziness
        - Reduced urination
        - Dark-colored urine

        Drinking fluids can help with mild dehydration.
        Severe dehydration may require medical attention.
        """,

        "diabetes": """
        Diabetes is a condition in which blood glucose levels
        are consistently too high.

        Possible symptoms include:
        - Increased thirst
        - Frequent urination
        - Increased hunger
        - Fatigue
        - Blurred vision

        Diabetes should be diagnosed and managed by a
        healthcare professional.
        """,

        "hypertension": """
        Hypertension means persistently high blood pressure.

        High blood pressure often does not cause obvious symptoms.
        Regular blood-pressure measurement is important.

        Persistent high blood pressure should be evaluated
        by a healthcare professional.
        """,

        "cough": """
        Coughing is a natural reflex that helps clear the airways.

        It can occur due to:
        - Common cold
        - Allergies
        - Respiratory infections
        - Irritants

        A persistent, severe or blood-producing cough should
        be medically evaluated.
        """
    }

    query_lower = query.lower()

    for condition, information in medical_data.items():

        if condition in query_lower:
            return information

    return """
    I don't have specific information about that topic
    in my basic medical knowledge tool.

    I can provide general educational information about
    common health topics, but I cannot diagnose diseases
    or prescribe medicines.
    """


# -----------------------------
# Medical Agent
# -----------------------------

medical_agent = create_agent(
    model=model,
    tools=[medical_information],

    system_prompt="""
    You are a Medical Information Voice Assistant.

    Your job is to provide simple, clear and educational
    information about health and medical topics.

    You should:
    - Explain common medical conditions.
    - Explain common symptoms.
    - Explain general prevention and self-care.
    - Use the medical_information tool when appropriate.
    - Tell the user when they should consult a healthcare professional.
    - Keep answers concise because the response will be spoken aloud.

    You must NOT:
    - Diagnose the user.
    - Prescribe medicines.
    - Recommend prescription drug doses.
    - Pretend to be a doctor.
    - Replace professional medical advice.

    If the user describes a medical emergency,
    advise them to seek immediate emergency medical care.
    """
)


# -----------------------------
# Ask Agent
# -----------------------------

def ask_medical_agent(question):

    response = medical_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    })

    return response["messages"][-1].content