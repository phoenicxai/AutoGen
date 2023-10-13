from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from search import search

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

assistant = AssistantAgent("assistant", llm_config={
                           "config_list": config_list, "functions": [
                               {
                                   "name": "Search",
                                   "description": "Search at Google and returns Title, Link, and Snippet",
                                   "parameters": {
                                       "type": "object",
                                       "properties": {
                                           "query": {
                                               "type": "string",
                                               "description": "The search query",
                                           }
                                       },
                                       "required": ["query"],
                                   },
                               }
                           ]})

user_proxy = UserProxyAgent(
    "user_proxy",
    code_execution_config={"work_dir": "coding"},
    human_input_mode="NEVER",
    function_map={"Search": search}
)

user_proxy.initiate_chat(
    assistant, message="Find the latest news about NVIDIA that explain the current stock price")
