import os
from supabase import create_client, Client
from dotenv import load_dotenv
import datetime as dt
import psycopg
import pandas as pd

### Load the .env file
load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
print(url, key)
supabase: Client = create_client(url, key)



# with psycopg.connect(
#     'postgresql://postgres.slbeklsinybfmmcvscqn:boulder_gym_project@aws-0-us-west-1.pooler.supabase.com:6543/postgres'
# ) as conn:
#     with conn.cursor() as cur:
#         cur.execute('create table if not exists expenses (expense_id varchar,expense_type varchar, expense_description varchar, branch_id varchar,  created_at timestamp)')
#         cur.execute('select * from customers')
#         print(40*'-')
#         print(cur.fetchall())
#         print(40*'-')
#     conn.commit()

# CREATE TABLE access_registry (
#     transaction_id varchar NOT NULL,
#     member_id int NOT NULL,
#     plan_id int NOT NULL ,
#     branch_id int NOT NULL,
#     status varchar NOT NULL,
#     created_at timestamp NOT NULL,
#     PRIMARY KEY (transaction_id),
#     FOREIGN KEY (member_id) REFERENCES customers(member_id)
# );


with psycopg.connect(
    'postgresql://postgres.slbeklsinybfmmcvscqn:boulder_gym_project@aws-0-us-west-1.pooler.supabase.com:6543/postgres'
) as conn:
    df = pd.read_sql('SELECT * FROM customers', conn)
# supabase.from_('customers').insert([
#   {
#     'name': 'Levi',
#     'last_name' : 'Murillo',
#     'gender' : 'Male',
#     'birth_date' : dt.datetime(1991,11,4).isoformat(),
#     'phone_number' : 473123123,
#     'email' : 'islitagame@hotmail.com',
#     'adress' : 'Neza',
#   },
#   {
#     'name': 'Bruno',
#     'last_name' : 'Rodriguez',
#     'gender' : 'Male',
#     'birth_date' : dt.datetime(1991,11,4).isoformat(),
#     'phone_number' : 473125129,
#     'email' : 'deku_momentum@hotmail.com',
#     'adress' : 'Barranca del muerto',
#   },
# ]).execute()

print(df)

# response = supabase.table("customers").select("*").execute()
# print(response)
