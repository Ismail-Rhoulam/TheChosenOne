import re # Importing the regex pattern
import os
import logging
import pandas as pd # Importing the Pandas package with an alias, pd
from sqlalchemy import create_engine, text # Importing the SQL interface

# Name our logger so we know that logs from this module come from the data_ingestion module
logger = logging.getLogger('DataAssembler')

# Set a basic logging message up that prints out a timestamp, the name of our logger, and the message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DataAssembler:

    def __init__(self, db=None, csv1=None, csv2=None, csv3=None, csv4=None):

        if db is not None:

            if not os.path.exists(db):
                logger.error(f"Database file '{db}' not found.")
                raise FileNotFoundError(f"Database file '{db}' not found.")

            try:
                # Attempt to create an engine without connecting
                engine = create_engine(f'sqlite:///{db}', pool_pre_ping=True)
                # Test connection
                with engine.connect() as conn:
                    # Check if the connection is established
                    conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))  # This is a simple query to check the connection
                # If the connection is successful, log a message
                logger.info("Connection to the database established successfully.")

                # Set the connection attribute
                self.co = engine.connect()

                # log the successful engine creation
                logger.info('Engine created successfully\n')

            except ImportError as e:  # If we get an ImportError, inform the user SQLAlchemy is not installed
                logger.error("SQLAlchemy is required to use this function. Please install it first.")
                raise e
            except exc.ArgumentError as e:  # If there's an invalid database URL
                logger.error(f"Invalid database URL: {e}")
                raise e
            except exc.DBAPIError as e:  # If there's an error connecting to the database
                logger.error(f"Failed to connect to the database. Error: {e}")
                raise e
            except Exception as e:  # If we fail to create an engine inform the user
                logger.error(f"Failed to create database engine. Error: {e}")
                raise e
            
            tables = [] # Set up a list of the tables of the database
            result = self.co.execute(text("SELECT name FROM sqlite_master WHERE type='table';")) # SQL query to retrieve table names
            for row in result: # Iterate in the query result
                tables.append(re.sub(r'[^\w\s]','', str(row))) # Add each processed table name to the list created before
            
            print('Tables & their columns :\n')
                
            table_columns = {} # A dictionary to store table names and their columns
            for table in tables: # For each table in the list created before
                print(f'        {table}')
                sql_query1 = f"PRAGMA table_info({table});" # SQL query to retrieve table info
                info = self.co.execute(text(sql_query1)) # Store the result in a variable
                columns = []
                for row in info:
                    columns.append(row[1])
                table_columns[table] = columns # Add the table name as a key and the columns it contains as values
                print(f'            {columns}')
            
            common_col = set(table_columns[tables[0]]) # Get the common column between the tables
            for name, col in table_columns.items():
                common_col.intersection_update(col)
            co_col = list(common_col) # Turn the set into a list
            print('')

            if not co_col:
                print('No common column in the tables\n')
            else:
                print("Common columns: ", f'{co_col}\n')

                if len(co_col) > 1:
                    col = input('Choose a column to use for joining tables: ')
                else:
                    col = f'({re.sub(r'[^\w\s]', '', co_col[0])})' # Make the commun column suitable for a SQL query

                # SQL query to join the join the tables in one table using the common column
                sql_query2 = f'''
        SELECT *
        FROM {tables[0]}'''
                for rest in tables[1:]: # Make the query scalable regarding the the number of tables in the database
                    sql_query2 += f'''
        LEFT JOIN {rest} USING {col}'''

                self.df0 = pd.read_sql_query(text(sql_query2), self.co) # Create a dataframe

                print(f'SQL query used: {sql_query2}\n')

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