import yaml
from utils import (output_utils, string_utils, yaml_utils)

class BigQueryEncryptor:
    def __init__(self, yaml_path):
        self.project_id = yaml_utils.get_project_id(yaml_path)
        self.dataset_id = yaml_utils.get_dataset_id(yaml_path)
        self.yaml_path = yaml_path


    def set_table_config(self, yaml_config):
        print("===== \n")
        print(yaml_config)
        print("\n===== \n")

        self.encrypted_table_id = yaml_utils.get_encrypted_table_id(yaml_config)
        self.encrypted_columns = yaml_utils.get_encrypted_columns(yaml_config)
        self.encrypted_primary_key = yaml_utils.get_encrypted_primary_key(yaml_config)

        self.key_table_id = yaml_utils.get_key_table_id(yaml_config)
        self.key_column = yaml_utils.get_key_column(yaml_config)
 

    def generate_queries(self):
        with open(self.yaml_path, "r") as stream:
            try:
                yaml_configs = yaml.safe_load(stream)

                output_utils.generate_folder(string_utils.bq_encrypted_output_path(), 
                                           self.project_id, 
                                           self.dataset_id)

                for yaml_config in yaml_configs:
                    self.set_table_config(yaml_config)
                    
                    output_utils.generate_file(string_utils.bq_encrypted_output_path(), 
                                             self.query_builder(),
                                             self.project_id, 
                                             self.dataset_id, 
                                             self.encrypted_table_id)

            except yaml.YAMLError as exc:
                print(exc)


    def query_builder(self):
        query = string_utils.bq_query(self.exception_statement(self.encrypted_columns), 
                                      self.encrypted_statement(self.encrypted_columns, 
                                                               self.key_column, 
                                                               self.encrypted_primary_key), 
                                      self.encrypted_table_id, 
                                      self.key_table_id)
        
        print(query)
        return query

    
    def exception_statement(self, encrypted_columns):
        exclude_statement = ''
        columns_left = len(encrypted_columns)

        for exclude_column in encrypted_columns:
            exclude_statement += list(exclude_column.keys())[0]
            if columns_left > 1: exclude_statement = exclude_statement + ', '
            columns_left -= 1
        
        return exclude_statement

    
    def encrypted_statement(self, encrypted_columns, key, primary_key):
        encrypted_statement = ''
        columns_left = len(encrypted_columns)

        for encrypted_column in encrypted_columns:
            encrypted_statement += 'AEAD.ENCRYPT(keyset_table.%s, encrypted_table.%s, encrypted_table.%s)' % \
                (key, list(encrypted_column.keys())[0], primary_key)
            
            if columns_left > 1: encrypted_statement = encrypted_statement + ', \n\t'
            columns_left -= 1
        
        return encrypted_statement
    