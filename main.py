import sys
import bigquery_encryptor

yaml_path = sys.argv[1]
bqe = bigquery_encryptor.BigQueryEncryptor(yaml_path)
bqe.generate_queries()