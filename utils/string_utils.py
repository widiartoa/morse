bq_query_template = """
SELECT
\tencrypted_table.* (EXCEPT %s),
\t%s
FROM
\t`%s` encrypted_table
\tCROSS JOIN `%s` keyset_table
"""


def bq_query(exception_statement, encrypted_statement, encrypted_table_id, key_table_id) -> str:
    return bq_query_template % (exception_statement, encrypted_statement, encrypted_table_id, key_table_id)


def bq_encrypted_output_path() -> str:
    return "output/encrypted/bq_sql"
