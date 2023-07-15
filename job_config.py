from utils import yaml_utils

class JobConfig:
    def __init__(self, yaml_path: str):
        self.project_id = yaml_utils.get_project_id(yaml_path)
        self.dataset_id = yaml_utils.get_dataset_id(yaml_path)
        self.yaml_path = yaml_path

    def get_project_id(self): return self.project_id

    def get_dataset_id(self): return self.dataset_id

    def get_yaml_path(self): return self.yaml_path