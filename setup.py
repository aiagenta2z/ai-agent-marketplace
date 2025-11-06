# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = [
    "requests>=2.17.0"
]

setup(
    name="ai_agent_marketplace",   # Required
    version="0.0.3",    # Required
    description="AI Agent Marketplace Utils and API to monitor Web Traffic Data",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author_email="aihubadmin@126.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="AI Agent Marketplace,API,AI Agent",
    packages=find_packages(where="src"),  # Required
    install_requires=install_requires,    # Required        
    package_dir={'': 'src'},
    package_data={'ai_agent_marketplace': ['*.txt', '*.json']
        , 'ai_agent_marketplace.data': ['*.txt', '*.json']
    },    
    python_requires=">=3.4",
    project_urls={
        "homepage": "http://www.deepnlp.org",
        "repository": "https://github.com/aiagenta2z/ai-agent-marketplace"
    },
)
