import yaml


def load_config():
    file_path = './config.yml'
    # Load the YAML file into a Python object
    with open(file_path, "r", encoding='utf-8') as file:
        data = yaml.safe_load(file)
        return data
