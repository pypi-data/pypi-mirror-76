import pymysql
import time


class DataBase:
    def __init__(self, db_ip='localhost', db='recommend_system', user_name='root', password='root', port=3306):
        self.db_ip, self.db, self.user_name, self.password, self.port = db_ip, db, user_name, password, port
        self.cursor = self.connect()
        self.db_name = db


    def connect(self):
        """
        :param dp_ip: the ip address of database
        :param db: the database name
        :param user_name: the user name to login the database
        :param port: the port to connect the database
        :return the cursor of connection. if connection failed, return None
        """
        for i in range(10):#try 10 times if connection failed
            try:
                self.connection = pymysql.connect(host = self.db_ip, user = self.user_name,password = self.password, port = self.port, db = self.db)
                return self.connection.cursor()
            except pymysql.err.OperationalError:
                print('database connection failed: retrying ...')
                time.sleep(1)

    def create_table(self,table_cmd):
        """
        :param table_cmd: the commends to create table
        """
        if self.cursor is None:
            self.cursor = self.connect() #reconnect
        if self.cursor is None:
            print('failed to create table, connection failed')
            return
        if table_cmd == "":
            return
        self.cursor.execute(f'use {self.db_name}')
        self.cursor.execute(table_cmd)
    
    def save_table(self,data,table_name):
        """
        :param data: column_name -> [value1, value2 ...]
        """
        if self.cursor is None:
            self.cursor = self.connect()
        if self.cursor is None:
            print('failed to save table, connection failed')
            return
        if data is None or len(data)==0 or table_name is None or table_name == "": 
            return
        for i in range(len(list(data.values())[0])):
            info = {k:v[i] for k,v in data.items()}
            keys = ', '.join(info.keys())
            values = ', '.join(['%s'] * len(info))
            cmd = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table_name, keys=keys, values=values)
            params = list(info.values())+list(info.values())
            params = [str(i) for i in params]
            params = ['null' if i == '' else i for i in params]
            params = ['\'' + i + '\'' if i != 'null' else i for i in params]
            update = ','.join([" {key} = %s".format(key=key) for key in info])
            cmd += update
            cmd = cmd%tuple(params)
            for _ in range(5):
                try:
                    self.cursor.execute(cmd)
                    self.connection.commit()
                    break
                except BaseException as e:
                    print('failed to save table')
                    print(e)
                    time.sleep(1)
                    self.cursor = self.connect()
