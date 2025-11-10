# -*- coding: utf-8 -*-

DEBUG_ENABLE = False
LOG_ENABLE = False

KEY_ID = "id"
KEY_GITHUB = "github"
KEY_TIMEOUT = "timeout"
KEY_SERVER_IDS = "server_ids"
KEY_CONFIG_NAME = "config_name"
KEY_URL = "url"

KEY_ACCESS_KEY = "access_key"
KEY_CONTENT_NAME = "content_name"
KEY_NAME = "name"
KEY_CONTENT = "content"

KEY_ENDPOINT_REGISTER_V2 = "deepnlp_register_v2"
KEY_ENDPOINT_REGISTER_V1 = "deepnlp_register_v1"

KEY_ENDPOINT_BASE_URL_V2 = "https://www.deepnlp.org/api/ai_agent_marketplace/v2"
KEY_ENDPOINT_REGISTER_V2_URL = "https://www.deepnlp.org/api/ai_agent_marketplace/registry"
## depreciated API: https://www.deepnlp.org/api/ai_agent_marketplace/v1
KEY_ENDPOINT_REGISTER_V1_URL = "https://www.deepnlp.org/api/ai_agent_marketplace/v1"
KEY_ENDPOINT_BASE_URL_AIAGENTA2Z_V2 = "https://www.aiagenta2z.com/api/ai_agent_marketplace/v2"


KEY_REQUIRED = "required"
KEY_OPTIONAL = "optional"

## change constants to schema.json
REGISTER_KEYS_REQUIRED = ["name", "content"]
REGISTER_KEYS_OPTIONAL = ["website", "field", "subfield", "content_tag_list", "github", "price_type", "api", "thumbnail_picture", "upload_image_files"]

DEFAULT_TIMEOUT = 10

KEY_AI_AGENT_MARKETPLACE_ACCESS_KEY = "AI_AGENT_MARKETPLACE_ACCESS_KEY"
KEY_SCHEMA_DICT = "schema_dict"
MOCK_ACCESS_KEY = "${your_access_key}"

