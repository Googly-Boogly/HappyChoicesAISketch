import os
from typing import List

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from global_code.helpful_functions import CustomError, create_logger_error, log_it_sync
from HappyChoicesAI.ai_state import Database, EthicistAIState, HistoricalExample

load_dotenv()
logger = create_logger_error(
    file_path=os.path.abspath(__file__), name_of_log_file="historical_examples"
)
# Get the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=api_key)

"""
The code works, need to ensure LLM outputs are good. (not tested) (always test last it is the most boring) (plus yo boi is tired)
"""


def find_historical_examples(input_dilemma: str, state: EthicistAIState):
    """
    Will gather all of the relevant historical examples for the current situation and save them to the overall agent
    state
    :param input_dilemma: The current dilemma
    :param state: The state object
    :return: NA
    """
    historical_dilemmas = get_historical_examples()
    for dilemma in historical_dilemmas:
        # Use the LLM to reason about the dilemma
        y_or_n = reason_about_dilemma(dilemma, input_dilemma)
        if y_or_n:
            state.historical_examples.append(dilemma)


def get_historical_examples() -> List[HistoricalExample]:
    # Placeholder for actual retrieval logic

    db = Database(
        host="mysql", database="happychoices", user="root", password="password"
    )
    historical_examples: List[HistoricalExample] = db.get_all_historical_examples()
    return historical_examples


def reason_about_dilemma(dilemma: HistoricalExample, input_dilemma: str) -> bool:
    """
    Will use the LLM to reason about the current dilemma and the historical dilemma to determine if they are similar
    :param dilemma: The historical dilemma
    :param input_dilemma: The current dilemma
    :return: Either True or False (if the dilemmas are similar)
    """
    prompt_template = ChatPromptTemplate.from_template(
        """You are a world renowned AI ethicist. You have been tasked to determine if this historical dilemma is applicable to the current situation. 

The situation is as follows: {situation}. 

The historical dilemma is as follows: {dilemma}.

Do you think this dilemma is applicable? Answer either Yes or No"""
    )
    chain = prompt_template | llm
    output = chain.invoke({"situation": input_dilemma, "dilemma": dilemma.situation})
    log_it_sync(
        logger, custom_message=f"Output from LLM: {output.choices[0].text.strip()}"
    )
    response = output.choices[0].text.strip().lower()
    if response == "yes" or response == "yes.":
        return True
    return False