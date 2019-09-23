import pandas as pd
from credentials import HOST, PORT, USERNAME, PASSWORD, DATABASE, TABLE

conn_string = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'


def dump():
    renfe = pd.read_sql_table(table_name=TABLE, con=conn_string)
    
    #dump
    renfe.to_parquet('renfe.parquet')
    renfe.to_csv('renfe.csv', index=False)


if __name__ == '__main__':
    dump()
