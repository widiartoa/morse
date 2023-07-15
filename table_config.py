from utils import yaml_utils
import job_config
import yaml

class TableConfig:
    def __init__(self, job: job_config.JobConfig, yaml_config: yaml):
        self.project_id = job.get_project_id()
        self.dataset_id = job.get_dataset_id()
        self.set_table_config(yaml_config)

    def set_table_config(self, yaml_config):
        self.encrypted_table_id = yaml_utils.get_encrypted_table_id(yaml_config)
        self.encrypted_columns = yaml_utils.get_encrypted_columns(yaml_config)
        self.encrypted_primary_key = yaml_utils.get_encrypted_primary_key(yaml_config)

        self.key_table_id = yaml_utils.get_key_table_id(yaml_config)
        self.key_column = yaml_utils.get_key_column(yaml_config)
    
    def get_project_id(self): return self.project_id
    
    def get_dataset_id(self): return self.dataset_id

    def get_encrypted_table_id(self): return self.encrypted_table_id

    def get_encrypted_columns(self): return self.encrypted_columns

    def get_encrypted_primary_key(self): return self.encrypted_primary_key

    def get_key_table_id(self): return self.key_table_id

    def get_key_column(self): return self.key_column 
