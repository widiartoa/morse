import os

def generate_folder(bq_encrypted_output_path, project_id, dataset_id):
    folder_name = "%s/%s/%s" % (bq_encrypted_output_path, project_id, dataset_id)

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def generate_file(bq_encrypted_output_path, query, project_id, dataset_id, table_id):
    with open("%s/%s/%s/%s.sql" % (bq_encrypted_output_path, 
                                   project_id, 
                                   dataset_id, 
                                   table_id), "w") as file:
        file.write(query)
