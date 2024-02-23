import re # Importing the regex pattern
import pandas as pd # Importing the Pandas package with an alias, pd
from sqlalchemy import create_engine, text # Importing the SQL interface

class DataAssembler:

    def __init__(self, db=None, csv1=None, csv2=None, csv3=None, csv4=None):

        if db is not None:

            # Create an engine for the database
            engine = create_engine(f'sqlite:///{db}') # Ensure that the db variable contains the path to the .db file
            # Create a connection object
            self.co = engine.connect()

            print('Engine created sucessfully \n')

            
            tables = [] # Set up a list of the tables of the database
            result = self.co.execute(text("SELECT name FROM sqlite_master WHERE type='table';")) # SQL query to retrieve table names
            for row in result: # Iterate in the query result
                tables.append(re.sub(r'[^\w\s]','', str(row))) # Add each processed table name to the list created before
            
            print('Tables :')
            for table in tables:
                print(f'    {table}')
                
            table_columns = {} # A dictionary to store table names and their columns
            for table in tables: # For each table in the list created before
                sql_query1 = f"PRAGMA table_info({table});" # SQL query to retrieve table info
                info = self.co.execute(text(sql_query1)) # Store the result in a variable
                table_columns[table] = [row[1] for row in info] # Add the table name as a key and the columns it contains as values
            
            common_col = set(table_columns[tables[0]]) # Get the common column between the tables
            for name, col in table_columns.items():
                common_col.intersection_update(col)
            co_col = list(common_col) # Turn the set into a list
            print("\nCommon column:", co_col[0], "\n")
        
            col = f'({re.sub(r'[^\w\s]', '', co_col[0])})' # Make the commun column suitable for a SQL query

            # SQL query to join the join the tables in one table using the common column
            sql_query2 = f'''
            SELECT *
            FROM {tables[0]}'''
            for rest in tables[1:]: # Make the query scalable regarding the the number of tables in the database
                sql_query2 += f'''
            LEFT JOIN {rest} USING {col}'''

            self.df0 = pd.read_sql_query(text(sql_query2), self.co) # Create a dataframe

            print(f'SQL query used:{sql_query2}\n')
            print(f'The DataFrame of the joined tables is under the class attribute: df0\n')

        if csv1 is not None:
            if "/" in csv1:
                self.df1 = pd.read_csv(csv1)
                name_csv1 = re.search(r'/([^/]+)$', csv1).group(1)
                print(f'The DataFrame of {name_csv1} is under the class attribute: df1\n')
            else:
                self.df1 = pd.read_csv(csv1)
                print(f'The DataFrame of {csv1} is under the class attribute: df1\n')

        if csv2 is not None:
            if "/" in csv2:
                self.df2 = pd.read_csv(csv2)
                name_csv2 = re.search(r'/([^/]+)$', csv2).group(1)
                print(f'The DataFrame of {name_csv2} is under the class attribute: df2\n')
            else:
                self.df2 = pd.read_csv(csv2)
                print(f'The DataFrame of {csv2} is under the class attribute: df2\n')

        if csv3 is not None:
            if "/" in csv3:
                self.df3 = pd.read_csv(csv3)
                name_csv3 = re.search(r'/([^/]+)$', csv3).group(1)
                print(f'The DataFrame of {name_csv3} is under the class attribute: df3\n')
            else:
                self.df3 = pd.read_csv(csv3)
                print(f'The DataFrame of {csv3} is under the class attribute: df3\n')

        if csv4 is not None:
            if "/" in csv4:
                self.df4 = pd.read_csv(csv4)
                name_csv4 = re.search(r'/([^/]+)$', csv4).group(1)
                print(f'The DataFrame of {name_csv4} is under the class attribute: df4\n')
            else:
                self.df4 = pd.read_csv(csv4)
                print(f'The DataFrame of {csv4} is under the class attribute: df4\n')