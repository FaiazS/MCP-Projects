import sqlite3

import json

from dotenv import load_dotenv

from datetime import datetime

load_dotenv(override=True)

EQUITY_DATABASE = 'equity_accounts.db'

with sqlite3.connect(EQUITY_DATABASE) as database_connection:

    database_cursor = database_connection.cursor()

    database_cursor.execute(
        
                            '''
                            
                            CREATE TABLE IF NOT EXISTS Equity_Accounts (
                            
                            Account holder name TEXT PRIMARY KEY, 
                            
                            Account TEXT
                            
                            )
                            
                            '''
                            
                            )

    database_cursor.execute(
        
    '''
                            
                               CREATE TABLE IF NOT EXISTS Equity_Logs 
                            
                               (
                               
                               Log id PRIMARY KEY AUTOINCREMENT, 
                            
                               Log name TEXT, 
                            
                               Time DATETIME, 
                            
                               Log type TEXT, 
                            
                               Log message TEXT
                               
                               )
                            
                            '''
                                                  
    )

    database_cursor.execute(
        
                           ''' 
                                CREATE TABLE IF NOT EXISTS Equity_Market(
                            
                                Market date TEXT PRIMARY KEY, 
                            
                                Market data TEXT
                            
                            )
                            
                            '''
                            )
    database_connection.commit()


def register_equity_account(equity_account_name, equity_account_info):

    equity_data_json = json.dumps(equity_account_info)

    with sqlite3.connect(EQUITY_DATABASE) as database_connection:

        database_cursor = database_connection.cursor()

        database_cursor.execute(
            
                                 '''
                                 
                                   INSERT INTO Equity_Accounts(Account holder name, Account) 
                                
                                   VALUES (?, ?)
                                
                                   ON CONFLICT (Account holder name) 
                                   
                                   DO UPDATE SET Account = excluded.Account

        ''',

        (equity_account_name.lower(), equity_data_json)

        )

def get_equity_account(equity_account_name):

    with sqlite3.connect(EQUITY_DATABASE) as database_connection:

        database_cursor = database_connection.cursor()

        database_cursor.execute(
            
                                   '''
                                   
                                   SELECT Account 
                                
                                   FROM Equity_Accounts 
                                   
                                   WHERE Account holder name = ?
                                
                                   ''', 
                                   
                                   (equity_account_name.lower(),)
                                   
                                   )

        table_row = database_cursor.fetchone()

        return json.loads(table_row[0]) if table_row else None


def update_equity_database_log(log_name: str, log_type: str, log_message: str):

    current_time = datetime.now().isoformat()

    with sqlite3.connect(EQUITY_DATABASE) as database_connection:

        database_cursor = database_connection.cursor()

        database_cursor.execute(
            
                                '''
                                
                                INSERT INTO Equity_Logs(
                                
                                Log name,

                                Time,
                                
                                Log type,
                                
                                Log message) 
                                
                                VALUES 
                                
                                (?, 
                                
                                ?,
                                
                                ? , 
                                
                                ?)
                                
                                ''', 
                                
                                (log_name.lower(), current_time, log_type, log_message)
                                
                                )
        
        database_connection.commit()
        

def get_equity_database_log_entries(log_name: str, recent_logs = 10):

    with sqlite3.connect(EQUITY_DATABASE) as database_connection:

        database_cursor = database_connection.cursor()

        database_cursor.execute(
            
                                ''' 
                                
                                    SELECT Time, Log type, Log message 
                                
                                    FROM Equity_Logs 
                                
                                    WHERE Log name = ?
                                
                                    ORDER BY Time DESC
                                
                                    LIMIT ?

                               ''', 
                               
                               (log_name.lower(), recent_logs)
                               
                               )
        
        return reversed(database_cursor.fetchall())

def update_equity_market_data(date: str, equity_market_data: str) -> None:

    equity_market_data_json =  json.dumps(equity_market_data)

    with sqlite3.connect(EQUITY_DATABASE) as database_connection:

        database_cursor = database_connection.cursor()

        database_cursor.execute(
            
                                   '''
                                
                                   INSERT INTO Equity_Market(Market date, Market data)
                                
                                   VALUES (?, ?) 

                                   ON CONFLICT(Market date)

                                   DO UPDATE SET Market data = excluded.Market data
                                
                                   ''', 

                                    (date, equity_market_data_json)

        )

        database_connection.commit()

def get_equity_market_data(date: str) -> dict | None:

    with sqlite3.connect(EQUITY_DATABASE) as database_connection:

        database_cursor = database_connection.cursor()

        database_cursor.execute('''

                                 SELECT Market data
                                
                                 FROM Equity_Market
                                
                                 WHERE Market date = ?
                                
                                ''', (date, )
                                
                                )
        
        table_row = database_cursor.fetchone()

        return json.loads(table_row[0]) if table_row else None
    
    
