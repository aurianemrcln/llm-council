"""Configuration for the Local Distributed LLM Council."""
import os
from dotenv import load_dotenv

load_dotenv()

# Liste des machines du conseil
COUNCIL_NODES = [
    {"name": "OMEN-Iliana", "url": "http://25.41.57.50:11434", "model": "qwen2:7b"},
    {"name": "Ordi-Auriane", "url": "http://25.31.79.122:11434", "model": "gemma3:4b"},
    {"name": "PC_Tristan", "url": "http://25.29.137.82:11434", "model": "deepseek-r1:7b"},
]

# Le Chairman 
CHAIRMAN_NODE = {
    "name": "Chairman",
    "url": "http://localhost:11434",
    "model": "mistral"
}

# Stockage des conversations
DATA_DIR = "data/conversations"