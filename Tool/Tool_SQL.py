import pymysql
import configparser
from datetime import datetime


class SQLStatements:
    SELECT_PRODUCTS = "SELECT * FROM asin_info_current"
    INSERT_USER = "INSERT INTO users (name, email) VALUES (%s, ?)"
    UPDATE_PRODUCT = "UPDATE asin_info_current SET price = ? WHERE id = ?"


class MysqlUtil:
    # 配置文件路径
    CONFIG_FILE_PATH = "mysql.properties"

    def __init__(self, config_file_path=None):
        self.config_file_path = config_file_path
        if not config_file_path:
            self.config_file_path = self.CONFIG_FILE_PATH
        self.properties = configparser.ConfigParser()
        self.properties.read(self.config_file_path, encoding="utf-8")
        self.host = self.properties.get("mysql", "host")
        self.user = self.properties.get("mysql", "user")
        self.password = self.properties.get("mysql", "password")
        self.database = self.properties.get("mysql", "database")
        self.charset = self.properties.get("mysql", "charset")
        self.serverTimezone = self.properties.get("mysql", "serverTimezone")
        self.connection = None
        self.cursor = None
        self.connect()

    # 获取数据库连接
    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset,
                ssl={'use_ssl': False},  # 禁用 SSL
                cursorclass=pymysql.cursors.DictCursor,  # 设置结果返回为字典形式
                init_command="SET time_zone='+00:00'",  # 设置时区为 UTC
            )
            self.cursor = self.connection.cursor()
            print("数据库连接成功")
        except pymysql.Error as e:
            print("数据库连接失败:", e)

    def query(self, sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except pymysql.Error as e:
            print("执行查询出错:", e)
            return None

    def update(self, sql, params=None):
        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
            return True
        except pymysql.Error as e:
            print("执行更新出错:", e)
            return False

    def replace_by_dict(self, table_name, data_dict):
        # 尝试插入数据，如果数据已存在则更新
        placeholders = []
        #for d in data_dict:
        #    placeholders.append('%s')
        placeholders = ['%s' for _ in data_dict]
        placeholders_str = ', '.join(placeholders)
        columns = ', '.join(data_dict.keys())
        values = tuple(data_dict.values())
        # 构建插入或更新语句
        query = (
            f'REPLACE INTO {table_name} ({columns}) VALUES ({placeholders_str})'
        )
        try:
            print(query)
            print(columns)
            print(values)
            self.cursor.execute(query, values)
            self.connection.commit()
            return (True, None)
        except pymysql.Error as e:
            print("执行更新出错:", e)
            return (False, e)

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.cursor

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


# 使用示例
if __name__ == "__main__":
    print("测试模块")
