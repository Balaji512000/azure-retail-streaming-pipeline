# Databricks notebook source
# config_loader
# Simple utility to load environment configs

import json

def load_config(env="dev"):
    # In production, this path would be dynamic or passed as a widget
    config_path = f"/Workspace/Repos/Production/ecommerce-streaming-platform/configs/{env}/config.json"
    
    try:
        # Fallback for local testing or different workspace structures
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to a relative path for local development
        with open(f"../../configs/{env}/config.json", 'r') as f:
            return json.load(f)

# COMMAND ----------
# Usage in other notebooks:
# %run ./streaming-utils/config_loader
# conf = load_config()
