
SELECT
	encrypted_table.* (EXCEPT name, email, address, birth_date),
	AEAD.ENCRYPT(keyset_table.key, encrypted_table.name, encrypted_table.user_id), 
	AEAD.ENCRYPT(keyset_table.key, encrypted_table.email, encrypted_table.user_id), 
	AEAD.ENCRYPT(keyset_table.key, encrypted_table.address, encrypted_table.user_id), 
	AEAD.ENCRYPT(keyset_table.key, encrypted_table.birth_date, encrypted_table.user_id)
FROM
	`users` encrypted_table
	CROSS JOIN `key-project-id.key_dataset_id.key_table_id_1` keyset_table
