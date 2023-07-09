def get_project_id(yaml_path):
    return yaml_path.split("/")[1]

def get_dataset_id(yaml_path):
    return yaml_path.split("/")[2].split(".")[0]

def get_encrypted_table_id(yaml_config):
    return yaml_config['encrypted_table_id'].split(".")[2]

def get_encrypted_columns(yaml_config):
    return yaml_config['encrypted_columns']

def get_encrypted_primary_key(yaml_config):
    return yaml_config['primary_key']

def get_key_table_id(yaml_config):
    return yaml_config['key_table_id']

def get_key_column(yaml_config): 
    return yaml_config['key_column']