# -*- coding: utf-8 -*-
# @Time    : 2025/03/01

import json
import ai_agent_marketplace as agtm

def run_setup_config_deepnlp():
    ## you can choose other website to reuse this package
    agtm.set_endpoint("deepnlp")

def run_search_api():
    result = agtm.search(query="coding agent", page_id=0, count_per_page=20, mode="dict", timeout=5)
    item_map = result.get("item_map")
    item_list = item_map.get("coding agent")
    print (f"DEBUG: run_search_api return result {len(item_list)}")
    print (item_list[0:5] if len(item_list) > 0 else None)

def run_search_api_id():
    """
        Google Map MCP
        Agent Detail: https://deepnlp.org/store/mcp-server/map/pub-google-maps/google-maps
    """
    unique_id = "google-maps/google-maps"
    result = agtm.search(id=unique_id)
    print (f"DEBUG: run_search_api_id return result {len(result)}")
    print (result)

    unique_id = "google-maps/google-maps"
    result = agtm.search(id=unique_id)
    print (f"DEBUG: run_search_api_id return result {len(result)}")
    print (result)

def run_search_api_batch():

    unique_id_list =  ["google-maps/google-maps", "cursor/cursor-ai", "openai/codex"]
    params_list = [{"id": id} for id in unique_id_list]
    result = agtm.search_batch(params_list)
    print(f"DEBUG: run_search_api_batch return result {result}")

def register_ai_agent_from_dict():
    """
        access_key can be obtained from your personal page:

        https://www.deepnlp.org/workspace/my_ai_services
        once you submit, it's pending approval and you can track the data then
        get your access_key from https://www.deepnlp.org/workspace/my_ai_services
    """
    access_key = "${your_access_key}"
    name = "My First AI Coding Agent"

    item_info = {}
    item_info["name"] = name
    item_info["content"] = "This AI Agent can do complicated programming work for humans"
    item_info["website"] = "https://www.my_first_agent.com"
    item_info["field"] = "AI AGENT"
    item_info["subfield"] = "Coding Agent"
    item_info["content_tag_list"] = "coding,python"

    # Optional for API and Price
    item_info["api"] = "https://www.my_first_agent.com/agent"
    item_info["price_type"] = "API Call"
    item_info["price_per_call_credit"] = 100.0
    result = agtm.add(item_info, access_key=access_key)
    print (f"## DEBUG: AI Agent Marketplace Post url {result.get("url", "")} and message {result.get("msg", "")}")

def show_on_badge():

    import ai_agent_marketplace as agtm
    ## Explore AI Agent Register Meta of Google Map MCP Agent
    unique_id = "google-maps/google-maps"
    result = agtm.search(id=unique_id)
    print (f"DEBUG: run_search_api_id return result {len(result.get("items", []))} and {result}")

    ## Search AI Agent Marketplace Find Similar AI Agents
    result = agtm.search(query="coding agent", page_id=0, count_per_page=20, mode="dict", timeout=5)
    item_map = result.get("item_map")
    item_list = item_map.get("coding agent")
    print (f"DEBUG: run_search_api return result {len(item_list)} and {item_list}")

    # curl 'https://www.deepnlp.org/api/ai_agent_marketplace/v2?id=google-maps/google-maps'

    ## Registry New AI Agent: https://deepnlp.org/workspace/my_ai_services

def register_ai_agent_from_github():
    """
        Register your AI Agent if you have open sourced on GitHub
        Access_key can be obtained from generation: https://deepnlp.org/workspace/keys

        Website : https://www.deepnlp.org/workspace/my_ai_services
        once you submit, it's pending approval and you can track the data then
        get your access_key from https://www.deepnlp.org/workspace/my_ai_services
    """
    access_key = "${your_access_key}"

    item_info = {}
    item_info["github"] = "https://github.com/AI-Hub-Admin/FinanceAgent"
    result = agtm.add(item_info, access_key=access_key)
    print (f"## DEBUG: AI Agent Marketplace Post Result URL {result.get("url")} and message {result.get("msg")}")

def main():

    run_search_api()
    run_search_api_id()
    run_search_api_batch()
    register_ai_agent_from_dict()
    register_ai_agent_from_github()

if __name__ == '__main__':
    main()
