import argparse
import json
import yaml
import os
import sys

import ai_agent_marketplace as agtm
from .constants import *

AI_AGENT_MARKETPLACE_ACCESS_KEY = "AI_AGENT_MARKETPLACE_ACCESS_KEY"

DEFAULT_ACCESS_KEY = "${your_access_key}"

def get_access_key():
    key = os.environ.get(AI_AGENT_MARKETPLACE_ACCESS_KEY)
    if not key:
        print(f"Error: Access key not found as environment variable. Will return results using the mocked access_key for illustration \"${{your_access_key}}\". Please set the environment variable '{AI_AGENT_MARKETPLACE_ACCESS_KEY}' by command export AI_AGENT_MARKETPLACE_ACCESS_KEY=\"${{your_access_key}}\" or .env file",
              file=sys.stderr)
        print("You can get your access key from: https://www.deepnlp.org/workspace/keys", file=sys.stderr)
        return DEFAULT_ACCESS_KEY
    return key

def load_config_file(file_path):
    """Loads a .json or .yaml file and returns the dictionary content."""
    try:
        with open(file_path, 'r') as f:
            if file_path.endswith(('.yaml', '.yml')):
                return yaml.safe_load(f)
            elif file_path.endswith('.json'):
                return json.load(f)
            else:
                raise ValueError(f"Unsupported configuration file format. Must be .json or .yaml. Your input {file_path}")
    except FileNotFoundError:
        print(f"Error: Configuration file not found at '{file_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error loading configuration file: {e}", file=sys.stderr)
        sys.exit(1)

def upload_command(args):
    """
    Handles the 'agtm upload' command.
    Uploads AI Agent meta information either from a GitHub URL or a config file.
    """
    try:
        access_key = get_access_key()
        if access_key == DEFAULT_ACCESS_KEY:
            print("\n✅ Mock Registration Successful! Set up your own access key in variable AI_AGENT_MARKETPLACE_ACCESS_KEY")
            print(f"   URL: https://www.deepnlp.org/store/ai-agent/ai-agent/pub-AI-Hub-Admin/My-First-AI-Coding-Agent")
            print(f"   Message: You have successfully registered AI Agent from url https://www.deepnlp.org/store/ai-agent/ai-agent/pub-AI-Hub-Admin/My-First-AI-Coding-Agent")
            print(f"   Track its status at: https://www.deepnlp.org/store/ai-agent/ai-agent/pub-AI-Hub-Admin/My-First-AI-Coding-Agent")
            return

        item_info = {}

        endpoint = args.endpoint
        customized_endpoint_enable = True if endpoint != "" else False
        if customized_endpoint_enable:
            agtm.set_endpoint(url=endpoint)

        if args.github:
            print(f"Attempting to register agent from GitHub: {args.github}")
            item_info["github"] = args.github
            result = agtm.add(item_info, access_key=access_key)
            if LOG_ENABLE:
                print(
                    f"## DEBUG: AI Agent Marketplace Post Result URL {result.get("url")} and message {result.get("msg")}")

        elif args.config:
            print(f"Attempting to register agent from config file: {args.config}")
            file_content = load_config_file(args.config)

            if not file_content.get('name') or not file_content.get('content'):
                print("Error: Config file must contain 'name' and 'content' fields.", file=sys.stderr)
                sys.exit(1)
            item_info.update(file_content)
            result = agtm.add(data=item_info, access_key=access_key)
            if LOG_ENABLE:
                print(
                    f"## DEBUG: AI Agent Marketplace Post Result URL {result.get("url", "")} and message {result.get("msg", "")}")

        else:
            # This case should ideally be caught by argparse (either/or),
            # but is a good safeguard.
            print("Error: 'upload' command requires either '--github' or '--config'.", file=sys.stderr)
            sys.exit(1)

        # --- Call the SDK ---
        print("Submitting agent information to the marketplace...")
        try:
            # --- Output Results ---
            result_url = result.get("url", "N/A")
            result_msg = result.get("msg", "No message provided.")

            if result.get("url") or result.get("msg") in ["Success", "Pending Approval"]:
                print("\n✅ Registration Successful!")
                print(f"   URL: {result_url}")
                print(f"   Message: {result_msg}")
                print(f"   Track its status at: {result_url}")
            else:
                print("\n❌ Registration Failed.")
                print(f"   Response Message: {result_msg}")
                sys.exit(1)

        except Exception as e:
            print(f"\n❌ An unexpected error occurred during submission: {e}", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print (f"DEBUG: upload_command failed with exception: {e}")

def search_command(args):
    """
    Handles the 'agtm search' command.
    """
    query = args.q
    agent_id = args.id
    count_per_page = args.count_per_page
    page_id = args.page_id
    mode = args.mode

    if query:
        if query.strip() == "":
            print(f"Searching for agents with empty query: '' return no results.")
            return
        result = agtm.search(query=query, page_id=0, count_per_page=count_per_page, mode="dict", timeout=5)
        item_map = result.get("item_map", {})
        item_list = item_map.get(query)
        if item_list:
            print(f"Command agtm search command return result {len(item_list)}")
            print(item_list[0:count_per_page] if len(item_list) >= count_per_page else item_list)
        else:
            print(f"Command agtm search command return empty result please try again later.")

    elif agent_id:
        result = agtm.search(id=agent_id)
        print(f"Retrieving specific agent with unique ID: {agent_id}")
        if result:
            print(f"Result: {result}")
        else:
            print(f"Command agtm search command return empty result please try again later.")
    else:
        print("Error: 'search' command requires either '--q' (query) or '--id' (Agent ID).", file=sys.stderr)
        sys.exit(1)

def main():
    """Main entry point for the 'agtm' CLI."""
    parser = argparse.ArgumentParser(
        description="An Open Source Command-line Tool AI Agents meta registry, AI Agents Marketplace Management, AI Agents Search and AI Agents Index Services. Help users to explore interesting AI Agents. Documentation: https://www.deepnlp.org/doc/ai_agent_marketplace, Marketplace: https://www.deepnlp.org/store/ai-agent"
    )

    # --- Subparsers for different commands (e.g., 'upload', 'download', 'list') ---
    subparsers = parser.add_subparsers(title='Available Commands', dest='command')
    subparsers.required = True

    upload_parser = subparsers.add_parser(
        'upload',
        help='Register or upload AI Agent meta information in the marketplace and endpoint'
    )

    # Group for mutually exclusive arguments: --github OR --config
    group = upload_parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        '--github',
        type=str,
        help='The GitHub repository URL for the open-sourced agent.'
    )
    group.add_argument(
        '--config',
        type=str,
        help='Path to a .json or .yaml file containing the agent\'s meta information.'
    )
    upload_parser.add_argument(
        '--endpoint',
        type=str,
        default="",
        help='The endpoint URL for the open-sourced agent registry service to post data to the marketplace. Default to '
    )

    upload_parser.set_defaults(func=upload_command)

    ## 2. 'agtm search' search command
    search_parser = subparsers.add_parser(
        'search',
        help='Search for registered AI Agents by query or specific ID.'
    )

    # Group for mutually exclusive arguments: -q OR --id
    search_group = search_parser.add_mutually_exclusive_group(required=True)
    # exclusive
    search_group.add_argument(
        '--q',
        type=str,
        help='A free-text query string to search for agents (e.g., "coding agent" or "finance").'
    )
    search_group.add_argument(
        '--id',
        type=str,  # Assuming agent ID is an integer
        help='The specific unique ID of the AI Agent to retrieve from the marketplace index, such as "cursor/cursor-ai" or "openai/codex", for github published agents, the uniqueid should be "{owner_id}/{repo_id}" as in https://github.com/{owner_id}/{repo_id} '
    )
    ## all available
    search_parser.add_argument(
        '--count_per_page',
        type=int,
        default=10,
        help='default Count per page of search results returned'
    )
    search_parser.add_argument(
        '--page_id',
        type=int,
        default=0,
        help='Search default page index starting from 0...'
    )
    search_parser.add_argument(
        '--mode',
        type=str,
        default="dict",
        help='Default mode of search result "dict", "list"'
    )
    search_parser.set_defaults(func=search_command)

    # --- Parse and execute ---
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
