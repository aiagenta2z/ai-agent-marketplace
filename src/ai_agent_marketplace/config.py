# -*- coding: utf-8 -*-
import os
from typing import Dict, Optional

class Configuration:
    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: str = "",
        timeout: int = 30,
        max_retries: int = 3,
        **kwargs
    ):
        self.api_key = api_key or os.getenv("AI_AGENT_MARKETPLACE_API_KEY")
        self.endpoint = endpoint
        self.timeout = timeout
        self.max_retries = max_retries
        self.kwargs = kwargs

class ConfigurationManager:
    _instance = None
    _configurations: Dict[str, Configuration] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._configurations['default'] = Configuration()
        return cls._instance
    
    def configure(
        self,
        name: str = "default",
        api_key: Optional[str] = None,
        **kwargs
    ):
        self._configurations[name] = Configuration(api_key=api_key, **kwargs)
    
    def get_config(self, name: str = "default") -> Configuration:
        if name not in self._configurations:
            raise ValueError(f"Configuration '{name}' not found")
        return self._configurations[name]
    
    def remove_config(self, name: str):
        if name in self._configurations:
            del self._configurations[name]
