import pymysql
import configparser


class SQLStatements():
    SELECT_PRODUCTS = "SELECT * FROM products"
    INSERT_USER = "INSERT INTO users (name, email) VALUES (?, ?)"
    UPDATE_PRODUCT = "UPDATE products SET price = ? WHERE id = ?"

class MysqlUtil:
    # 配置文件路径
    CONFIG_FILE_PATH = "mysql.properties"

    # 静态变量，用于存储配置文件中的信息
    properties = None

    # 静态初始化
    @staticmethod
    def init():
        MysqlUtil.properties = configparser.ConfigParser()
        MysqlUtil.properties.read(MysqlUtil.CONFIG_FILE_PATH, encoding="utf-8")

    # 获取数据库连接
    @staticmethod
    def get_connection():
        if MysqlUtil.properties is None:
            MysqlUtil.init()

        host = MysqlUtil.properties.get("mysql", "host")
        user = MysqlUtil.properties.get("mysql", "user")
        password = MysqlUtil.properties.get("mysql", "password")
        database = MysqlUtil.properties.get("mysql", "database")
        charset = MysqlUtil.properties.get("mysql", "charset")
        serverTimezone = MysqlUtil.properties.get("mysql", "serverTimezone")
        
        try:
            connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                charset=charset,
                ssl={'use_ssl': False},  # 禁用 SSL
                cursorclass=pymysql.cursors.DictCursor,  # 设置结果返回为字典形式
                init_command="SET time_zone='+00:00'"  # 设置时区为 UTC
            )
            return connection
        except pymysql.Error as e:
            print("数据库连接失败：", e)
            return None
        

    # 设置SQL语句
    def set_sql(sql):
        print("执行SQL：", sql)
        
    def disconnect(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()


# 使用示例
if __name__ == "__main__":
    connection = MysqlUtil.get_connection()
    if connection:
        print("数据库连接成功")
    else:
        print("数据库连接失败")

    sql = "SELECT * FROM products"
    MysqlUtil.set_sql(sql)
    MysqlUtil.set_sql(SQLStatements.INSERT_USER)
    # 在这里执行您的业务逻辑，例如查询数据并处理结果
