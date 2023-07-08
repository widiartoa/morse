
SELECT
	encrypted_table.* (EXCEPT email, account_id),
	AEAD.ENCRYPT(keyset_table.key, encrypted_table.email, encrypted_table.user_id), 
	AEAD.ENCRYPT(keyset_table.key, encrypted_table.account_id, encrypted_table.user_id)
FROM
	`bigquery-project-id.bigquery_dataset_id.accounts` encrypted_table
	CROSS JOIN `key-project-id.key_dataset_id.key_table_id_2` keyset_table
