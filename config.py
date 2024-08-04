import yaml
from pathlib import Path

config_path = Path(__file__).parent / "config.yml"
with open(config_path, "r") as f:
    config = yaml.safe_load(f)

bot_token = config["telegram"]["bot_token"]
user_ids = config["telegram"]["user_ids"]
claude_api = config["claude"]["api"]
bard_api = config["bard"]["api"]

default_mode = "Claude" if claude_api else "Bard"
single_mode = not (claude_api and bard_api)

# New line for default Claude model
claude_default_model = config['claude'].get('default_model', 'claude-3-opus-20240229')

