from utils import (output_utils, string_utils)
import table_config

class BigQueryEncryptor:
    def __init__(self, table: table_config.TableConfig):
        self.table_conf = table
    
    def generate_encrypted_table_sql(self):
        output_utils.generate_file(string_utils.bq_encrypted_output_path(), 
                                   self.query_builder(),
                                   self.table_conf.get_project_id(), 
                                   self.table_conf.get_dataset_id(), 
                                   self.table_conf.get_encrypted_table_id())

    def query_builder(self):
        query = string_utils.bq_query(self.exception_statement(self.table_conf.get_encrypted_columns()), 
                                      self.encrypted_statement(self.table_conf.get_encrypted_columns(), 
                                                               self.table_conf.get_key_column(), 
                                                               self.table_conf.get_encrypted_primary_key()), 
                                      self.table_conf.get_encrypted_table_id(), 
                                      self.table_conf.get_key_table_id())
        
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
    