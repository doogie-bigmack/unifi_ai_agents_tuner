from autogen import ConversableAgent, GroupChat, GroupChatManager
import os
import openai
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Retrieve the single model name from environment variables
MODEL_AGENT = os.getenv('MODEL_AGENT')

# Initialize agents with the same model
number_agent = ConversableAgent(
    name="Number_Agent",
    system_message="You return the numbers I give you, one number each line.",
    llm_config={"config_list": [{"model": MODEL_AGENT, "api_key": os.getenv("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",
)

adder_agent = ConversableAgent(
    name="Adder_Agent",
    system_message="You add 1 to each number I give you and return the new numbers, one number each line.",
    llm_config={"config_list": [{"model": MODEL_AGENT, "api_key": os.getenv("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",
)

multiplier_agent = ConversableAgent(
    name="Multiplier_Agent",
    system_message="You multiply each number I give you by 2 and return the new numbers, one number each line.",
    llm_config={"config_list": [{"model": MODEL_AGENT, "api_key": os.getenv("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",
)

subtracter_agent = ConversableAgent(
    name="Subtracter_Agent",
    system_message="You subtract 1 from each number I give you and return the new numbers, one number each line.",
    llm_config={"config_list": [{"model": MODEL_AGENT, "api_key": os.getenv("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",
)

divider_agent = ConversableAgent(
    name="Divider_Agent",
    system_message="You divide each number I give you by 2 and return the new numbers, one number each line.",
    llm_config={"config_list": [{"model": MODEL_AGENT, "api_key": os.getenv("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",
)

human_agent = ConversableAgent(
    name="Human_Agent",
    system_message="You analyze the recommendations and ask questions as needed.",
    llm_config={"config_list": [{"model": MODEL_AGENT, "api_key": os.getenv("OPENAI_API_KEY")}]},
    human_input_mode="ALWAYS",
)

def define_interaction_triggers(chat_result):
    try:
        # Access the last message from the chat history using dot notation
        last_message = chat_result.chat_history[-1].content
        # Assuming the expected final number is 13
        expected_number = 13
        final_number = float(last_message.strip())
        if final_number != expected_number:
            return True
    except (AttributeError, IndexError, ValueError) as e:
        # Log the exception for debugging purposes
        logger.error(f"Error in define_interaction_triggers: {e}")
        return True
    return False

def main():
    group_chat_manager = GroupChatManager(
        agents=[number_agent, adder_agent, multiplier_agent, subtracter_agent, divider_agent, human_agent],
        llm_config={"config_list": [{"model": MODEL_AGENT, "api_key": os.getenv("OPENAI_API_KEY")}]},
    )

    chat_result = number_agent.initiate_chat(
        group_chat_manager,
        message="My number is 3, I want to turn it into 13.",
        summary_method="reflection_with_llm",
    )
    
    trigger = define_interaction_triggers(chat_result)
    logger.info(f"Trigger for human intervention: {trigger}")
    if trigger:
        intervention_message = (
            "After processing, the final number does not match the desired outcome of 13. "
            "Could you please review the calculations and identify any discrepancies or suggest alternative operations?"
        )
        
        human_chat_result = human_agent.initiate_chat(
            group_chat_manager,
            message=intervention_message,
            summary_method="reflection_with_llm"
        )
        
        # Logging human agent's response using dot notation
        logger.info(f"Human_Agent response: {human_chat_result.chat_history}")

if __name__ == "__main__":
    main()