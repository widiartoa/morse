import yaml
import os

query_template = """
SELECT
\tencrypted_table.* (EXCEPT %s),
\t%s
FROM
\t`%s` encrypted_table
\tCROSS JOIN `%s` keyset_table
"""

encrypted_output_path = "output/encrypted/bq_sql"

class BigQueryEncryptor:
    def __init__(self):
        self
    

    def generate_queries(self, yaml_path):
        path = yaml_path.split("/")

        with open(yaml_path, "r") as stream:
            try:
                yaml_configs = yaml.safe_load(stream)

                self.generate_folder(path[1], path[2])

                for yaml_config in yaml_configs:
                    print("===== \n")
                    print(yaml_config)
                    print("\n===== \n")
                    
                    self.generate_file(self.query_builder(yaml_config),
                                       path[1], path[2], yaml_config['encrypted_table_id'])

            except yaml.YAMLError as exc:
                print(exc)


    def query_builder(self, yaml_config):
        encrypted_columns = yaml_config['pii_columns']

        query = query_template % (self.exception_statement(encrypted_columns), 
                                   self.encrypted_statement(encrypted_columns, yaml_config['key_column'], yaml_config['primary_key']), 
                                   yaml_config['encrypted_table_id'], 
                                   yaml_config['key_table_id'])
        
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


    def generate_folder(self, project_id, dataset_id):
        folder_name = "%s/%s/%s" % (encrypted_output_path, project_id, dataset_id)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)


    def generate_file(self, query, project_id, dataset_id, table_id):
        with open("%s/%s/%s/%s.sql" % (encrypted_output_path, project_id, dataset_id, table_id.split(".")[2]), "w") as file:
            file.write(query)

            