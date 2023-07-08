import sys
import bigquery_encryptor

yaml_path = sys.argv[1]
bqe = bigquery_encryptor.BigQueryEncryptor()
bqe.generate_queries(yaml_path)