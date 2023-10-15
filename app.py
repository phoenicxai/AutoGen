from flask import Flask, jsonify, request
from flask import render_template
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json, Completion
from search import search

app = Flask(__name__)

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

assistant = AssistantAgent("assistant", llm_config={
    "seed": 42,  # seed for caching and reproducibility
    "use_cache": True,
    "config_list": config_list,
    "functions": [
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
            }
        }
    ]
})

user_proxy = UserProxyAgent(
    "user_proxy",
    code_execution_config={"work_dir": "coding"},
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    function_map={"Search": search}
)


def search(query):
    # Dummy data for demonstration
    return {
        "Title": "Dummy Title for " + query,
        "Link": "http://dummy-link.com",
        "Snippet": "This is a dummy snippet for " + query
    }


@app.route('/search', methods=['GET'])
def search_query():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    user_proxy.initiate_chat(
        assistant, message=f"Find the latest news about {query} that explain the current stock price")

    messages = user_proxy.chat_messages[assistant]

    return jsonify(messages)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
