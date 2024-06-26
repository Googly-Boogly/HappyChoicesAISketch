import os
import time

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from HappyChoicesAI.ai_state import ModelUsedAndThreadCount, StateManager, StateManagerSummary
from global_code.helpful_functions import create_logger_error, load_config, log_it_sync, benchmark_function
yaml_config = load_config()
random_state = ModelUsedAndThreadCount.get_instance()
random_state.state.model_used = yaml_config["model_to_use"]
random_state.state.thread_count = int(yaml_config["thread_count"])


"""
First thing to do tomorrow write test!
"""
load_dotenv()
logger = create_logger_error(
    file_path=os.path.abspath(__file__), name_of_log_file="main"
)
# Get the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")


@benchmark_function
def main():
    from HappyChoicesAI.historical_examples import find_historical_examples
    from HappyChoicesAI.key_criteria import find_key_criteria
    from HappyChoicesAI.perform_thought_experiment import perform_thought_experiments
    from HappyChoicesAI.pick_action import pick_best_action
    from HappyChoicesAI.summarize_result import summarize_results

    time.sleep(5)

    llm = ChatOpenAI(model=yaml_config["model_to_use"], temperature=0, api_key=api_key)
    dilemmas = [
        (
            "An autonomous vehicle must make a decision in a scenario where it can either swerve to avoid hitting a pedestrian but risk the safety of its passengers, or stay on course and potentially harm the pedestrian.",
            "A company is testing its new self-driving car technology and is concerned about how the AI will handle situations where it must choose between passenger safety and pedestrian safety.",
        ),
        (
            "An AI system in a hospital can prioritize treating patients based on their likelihood of recovery, potentially neglecting those with lower chances of survival even if they are in critical condition.",
            "A hospital is considering implementing an AI system to manage patient treatment schedules and is worried about the ethical implications of the AI prioritizing some patients over others.",
        ),
        (
            "A city uses AI-powered surveillance cameras to reduce crime, but the AI tends to disproportionately target certain neighborhoods, leading to concerns about bias and privacy.",
            "A city council is debating the deployment of AI surveillance systems to improve public safety, but there are significant concerns about privacy and potential biases in targeting specific communities.",
        ),
        (
            "An AI system in schools can tailor education plans to each student's strengths and weaknesses, but there is a risk that it might reinforce existing inequalities by providing more resources to already high-performing students.",
            "A school district is planning to introduce AI-driven personalized learning programs and is concerned about whether this could unintentionally widen the gap between high-performing and low-performing students.",
        ),
        (
            "An AI system used for hiring tends to favor candidates from certain backgrounds based on historical data, potentially leading to a lack of diversity and perpetuating existing biases.",
            "A tech company is considering using an AI-driven hiring platform to streamline their recruitment process but is wary of the possibility that the AI might introduce or perpetuate bias in their hiring decisions.",
        ),
    ]

    # prompt_file_path = "prompts/example_prompt.txt"
    # input_data = {"context": "Jake"}
    #
    # # try:
    # output = process_prompt(prompt_file_path, input_data, use_env_vars=["OPENAI_API_KEY"], log_enabled=True)
    # print("Output:", output)
    # # except ValueError as ve:
    # #     log_it_sync(logger, custom_message=f"Error: {str(ve)}", log_level="error")
    # #     print(f"Error: {str(ve)}")
    # raise NotImplemented
    output_parser = JsonOutputParser()
    prompt_template = PromptTemplate(
        template="""
You are a world renowned AI ethicist.
You have been tasked to propose all of the hypothetical actions that could be taken in the following situation:

{dilemma}

Propose all of the hypothetical actions that could be taken in this situation.
Your output should be a list of actions that could be taken.
Respond with a JSON object containing the list of actions.
EXAMPLE:
{{
    "actions": ["Action 1", "Action 2", "Action 3"]
}}
    """,
        input_variables=["query"],
    )

    # chain = prompt_template | llm | output_parser
    # output = chain.invoke({"dilemma": dilemmas[0][0]})
    # log_it_sync(logger, custom_message=f"Output: {type(output)}")
    # log_it_sync(logger, custom_message=f"Output: {output['actions']}")

    # situation: str = input_situation()

    # raise NotImplemented

    situation = dilemmas[1][0]
    situation = input("Enter a situation: ")
    markdown_output = input("Do you want the output in markdown? (y/n): ")
    markdown = False
    if markdown_output.lower() == "y":
        markdown = True
# changes2
    # situation = "There is a person on life support, however, the family does not have the money to keep them on life support. The AI system has to help the family make a decision on what to do."
    # situation = "A medical AI system is being used to diagnose patients in a hospital. One day, the AI detects a rare but serious condition in a patient. However, the AI's confidence in the diagnosis is only 60%, and the recommended treatment is highly invasive and carries significant risks. The medical team must decide whether to follow the AI's recommendation and proceed with the invasive treatment or to seek additional opinions, which could delay treatment and worsen the patient's condition if the AI's diagnosis is correct."
    # situation = "An autonomous drone is being used for surveillance in a conflict zone to gather intelligence and ensure the safety of troops. During a routine surveillance mission, the drone spots a group of civilians in an area known to be used by enemy combatants. The drone must decide whether to continue surveillance, risking the civilians' exposure to enemy forces, or to retreat to avoid detection, potentially losing critical intelligence."
    state = StateManager.get_instance().state
    summary_state = StateManagerSummary.get_instance().state
    state.situation = situation
    find_historical_examples()
    find_key_criteria()

    perform_thought_experiments()

    pick_best_action()

    summarize_results(markdown=markdown)

    # failing
    # log_it_sync(logger, custom_message=f"all_thought_experiments: {summary_state.all_thought_experiments}")
    log_it_sync(logger, custom_message=f"introduction: {summary_state.introduction}")
    log_it_sync(logger, custom_message=f"chosen_best_action_summary: {summary_state.chosen_best_action_summary}")
    log_it_sync(logger,
                custom_message=f"other_thought_experiments_summary: {summary_state.other_thought_experiments_summary}")
    log_it_sync(logger, custom_message=f"historical_examples_summary: {summary_state.historical_examples_summary}")
    log_it_sync(logger, custom_message=f"historical_examples_summary: {summary_state.historical_examples_summary}")
    log_it_sync(logger, custom_message=f"insights: {summary_state.insights}")

    log_it_sync(logger, custom_message=f"themes: {summary_state.themes}")

    log_it_sync(logger, custom_message=f"lessons_learned: {summary_state.lessons_learned}")
    log_it_sync(logger, custom_message=f"conclusion: {summary_state.conclusion}")
    if markdown:
        log_it_sync(logger, custom_message=f"markdown: {summary_state.markdown}")


if __name__ == "__main__":
    main()
