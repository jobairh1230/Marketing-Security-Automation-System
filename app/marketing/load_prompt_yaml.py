import yaml

def load_prompt_yaml(file_path: str):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
