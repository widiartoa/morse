import sys
import bigquery_encryptor
import job_config
import yaml
import table_config
from utils import (output_utils, string_utils)

yaml_path = sys.argv[1]
job_conf = job_config.JobConfig(yaml_path)

with open(yaml_path, "r") as stream:
    try:
        yaml_configs = yaml.safe_load(stream)

        output_utils.generate_folder(string_utils.bq_encrypted_output_path(), 
                                     job_conf.get_project_id(), 
                                     job_conf.get_dataset_id())

        for yaml_conf in yaml_configs:
            table = table_config.TableConfig(job_conf, yaml_conf)
            
            bigquery_encryptor.BigQueryEncryptor(table).generate_encrypted_table_sql()


    except yaml.YAMLError as exc:
        print(exc)