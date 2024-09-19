import logging
import json
import openai
import os
from dotenv import load_dotenv
from test_connection import DataCollector
from load_data import DataLoader
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager, ConversableAgent
from pydantic import BaseModel, ValidationError
from typing import List, Dict
import textwrap

# Configure logging Ensure debug logs are captured
logger = logging.getLogger(__name__)
#set the log level
logger.setLevel(logging.INFO)

# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')


if not openai_api_key:
    logger.error("OPENAI_API_KEY is not set in environment variables.")
    exit(1)

openai.api_key = openai_api_key

#create a private function to creaate the agents
def create_agents():
     # Initialize AssistantAgent with the latest OpenAI model
    network_agent = AssistantAgent(
        name="Assistant",
        system_message="You are an expert in UniFi networks and network security and you analyze the network configuration and data provided to provide best practice recommendations for configuraiton, performance, and security.",
        llm_config={"config_list": [{"model": os.getenv("MODEL_AGENT"), "api_key": os.getenv("OPENAI_API_KEY")}]}
    )
    
    # Initialize UserProxyAgent with Docker disabled
    user_proxy = UserProxyAgent(
        name="User",
        system_message="You are a human who analyzes the recommendation of the network agent and either asks for clarifications or approves the recommendaitons",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
        code_execution_config={
            "use_docker": False,  # Disable Docker for code execution
            # You can add other configurations here if necessary
        },
    )
    
    human_agent = ConversableAgent(
        name="Human_Agent",
        system_message="You are a human who analyzes the recommendation of the network agent and either asks for clarifications or approves the recommendaitons",
        llm_config={"config_list": [{"model": os.getenv("MODEL_AGENT"), "api_key": os.getenv("OPENAI_API_KEY")}]},
        human_input_mode="ALWAYS"
    )
    return network_agent, user_proxy, human_agent

#create a private function that calls the DataCollector class and returns the data

def _format_analysis_result(chat_history):
    """
    Formats the chat history into a readable string with bullet points.

    Args:
        chat_history (List[Dict]): The chat history containing messages from agents.

    Returns:
        str: A formatted string representation of the analysis with bullet points.
    """
    formatted_output = "=== Network Analysis Report ===\n\n"
    
    for idx, message in enumerate(chat_history, start=1):
        agent_name = message.get('agent', 'Unknown Agent')
        content = message.get('content', '')
        formatted_output += f"--- Message {idx} from {agent_name} ---\n"
        # Split content into lines and format each line as a bullet point
        for line in content.split('\n'):
            if line.strip():  # Avoid empty lines
                formatted_output += f"  - {line.strip()}\n"
        formatted_output += "\n"
    
    formatted_output += "===============================\n"
    return formatted_output



def print_recommendations_to_file(recommendations):
    with open("recommendations.txt", "w") as file:
        for recommendation in recommendations:
            file.write(recommendation + "\n")


def main():
    logger.info("Starting UniFi AI Agents workflow.")

    data_collector = DataCollector()
    
    

    try:
        logging.info("Starting data collection")
        data_collector.collect_data()
        logging.info("Data collection completed successfully")
    except Exception as e:
        logging.error(f"Error during data collection: {str(e)}")
        return f"Data collection failed: {str(e)}"

    logging.info("Creating agents")
    network_agent, user_proxy, human_agent = create_agents()
    logging.info("Agents created successfully")
    
    #load all the unifi data and configuration into a single prompt string
    data_loader = DataLoader()
   
    prompt = data_loader.generate_prompt()

    # [Existing code to set up llm_prompt]

    logger.info("AssistantAgent: Initialized successfully.")
    logger.info("UserProxyAgent: Initialized successfully.")

    # Initialize GroupChat with agents and configuration
    group_chat = GroupChat(
        agents=[network_agent, user_proxy, human_agent],
        messages=[],
        max_round=2
    )
    logger.info("GroupChat: Initialized successfully.")

    group_chat_manager = GroupChatManager(
        groupchat=group_chat,
        llm_config={"config_list": [{"model": os.getenv("MODEL_AGENT"), "api_key": os.getenv("OPENAI_API_KEY")}]}
    )
    logger.info("GroupChatManager: Initialized successfully.")

    analysis_result = user_proxy.initiate_chat(
        group_chat_manager, 
        message=prompt, 
        summary_method="reflection_with_llm",
        max_turns=6,
        speaker_selection_method="round_robin",
        allow_repeat_speaker=False,
    )
    #this needs work to format the output to be human readable
    #formatted_output = _format_analysis_result(analysis_result.chat_history)
    

if __name__ == "__main__":
    main()
