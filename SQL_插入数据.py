import pymysql
import configparser
from datetime import datetime

from Tool.Tool_SQL import *

config_file_path = "mysql.properties"
# db_util = MysqlUtil(MysqlUtil.CONFIG_FILE_PATH)
db_util = MysqlUtil(config_file_path)

data_dict = {
    'asin': 'TEST_D_0',
    'country': 'us',
    #'time': datetime.now().strftime("%Y-%m-%d"),
    'time': datetime.now().strftime("%Y-%m-%d"),
    'image': 'https://m.media-amazon.com/images/I/91fSsBq-QUL._AC_UL320_.jpg',
    'title': 'JOYIN Dinosaur Truck for Kids Sound, Flashing Lights, Mini Dinosaur Car Playset, Gift for Boys',
    'brand': 'JOYIN',
    'merchant_token': 1,
    'amz_choice': 2,
    'best_seller': 3,
    'deal_type': 4,
    'is_deal': 0,
    'is_fba': 0,
    'is_amz': 0,
    'is_smb': 0,
    "left_count": 1,
    "lower_price": 1,
    "lower_list": 1,
    "lowest_precent": 1,
    "sale_price": '29.99',
    "rrp_price": 39.99,
    "rrp_type": 1,
    "prime_price": 1,
    "discount": 1,
    "coupon": 1,
    "saving": 1,
    "promotion": 1,
    "promotion_code": 1,
    "rating": 4.9,
    "review": 29,
    "bought": 800,
    "a_rank_name": 'Toys & Games',
    "a_rank": 12816,
    "b_rank_name": 1,
    "b_rank": 1,
    "c_rank_name": 1,
    "c_rank": 1,
    "d_rank_name": 1,
    "d_rank": 1,
}
cursor = db_util.get_cursor()
connection = db_util.get_connection()

# 测试0
cursor.execute("SELECT * FROM asin_info_current")
results = cursor.fetchall()
print(results)

# 测试1
result = cursor.execute(
    "REPLACE INTO asin_info_current (asin, country, image) VALUES ('TEST1', 'CC', 'aaaaaaaaaaaaaaa')"
)
connection.commit()
print(result)

# 测试2
result = cursor.execute(
    "REPLACE INTO asin_info_current (asin, country, time) VALUES ('TEST2', 'CC', '2023-11-06')"
)
connection.commit()
print(result)

# 测试3
value = ('TEST3', 'Aa', 'AXXXXXXXXXa')
result = cursor.execute(
    "REPLACE INTO asin_info_current (asin, country, image) VALUES (%s,%s,%s)",
    value
)
print(value)
connection.commit()
print(result)


# 那么 %s 是合适的占位符。但是，在标准的 SQLite 或 MySQL 数据库中，通常使用 ? 作为占位符。
# result = cursor.execute("INSERT INTO asin_info_current (asin, country, image) VALUES (?, ?, ?)", ("AAAAABBBBB", "CC", "XXXXXXXX"))
# print(result)


# 执行SQL语句
result = cursor.execute(
    "REPLACE INTO asin_info_current (asin, country, time, image, title, brand, merchant_token, amz_choice, best_seller, deal_type, is_deal, is_fba, is_amz, is_smb, left_count, lower_price, lower_list, lowest_precent, sale_price, rrp_price, rrp_type, prime_price, discount, coupon, saving, promotion, promotion_code, rating, review, bought, a_rank_name, a_rank, b_rank_name, b_rank, c_rank_name, c_rank, d_rank_name, d_rank) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)",
    (
        data_dict['asin'],
        data_dict['country'],
        data_dict['time'],
        data_dict['image'],
        data_dict['title'],
        data_dict['brand'],
        data_dict['merchant_token'],
        data_dict['amz_choice'],
        data_dict['best_seller'],
        data_dict['deal_type'],
        data_dict['is_deal'],
        data_dict['is_fba'],
        data_dict['is_amz'],
        data_dict['is_smb'],
        data_dict['left_count'],
        data_dict['lower_price'],
        data_dict['lower_list'],
        data_dict['lowest_precent'],
        data_dict['sale_price'],
        data_dict['rrp_price'],
        data_dict['rrp_type'],
        data_dict['prime_price'],
        data_dict['discount'],
        data_dict['coupon'],
        data_dict['saving'],
        data_dict['promotion'],
        data_dict['promotion_code'],
        data_dict['rating'],
        data_dict['review'],
        data_dict['bought'],
        data_dict['a_rank_name'],
        data_dict['a_rank'],
        data_dict['b_rank_name'],
        data_dict['b_rank'],
        data_dict['c_rank_name'],
        data_dict['c_rank'],
        data_dict['d_rank_name'],
        data_dict['d_rank'],
    )
)
connection.commit()
print(result)

data_dict = {
    'asin': 'TEST_D_2',
    'country': 'us',
    #'time': datetime.now().strftime("%Y-%m-%d"),
    'time': None,
    'image': 'https://m.media-amazon.com/images/I/91fSsBq-QUL._AC_UL320_.jpg',
    'title': 'JOYIN Dinosaur Truck for Kids with 6 Soft Rubber Dinosaur Car Vehicles, 1 Toy Dinosaur Transport Carrier Truck with Music and Roaring Sound, Flashing Lights, Mini Dinosaur Car Playset, Gift for Boys',
    'brand': 'JOYIN',
    'merchant_token': 1,
    'amz_choice': 'XXXXX',
    'best_seller': 1,
    'deal_type': 1,
    'is_deal': 1,
    'is_fba': 1,
    'is_amz': 1,
    'is_smb': 1,
    "left_count": 1,
    "lower_price": 1,
    "lower_list": 1,
    "lowest_precent": 1,
    "sale_price": '29.99',
    "rrp_price": 139.99,
    "rrp_type": 2,
    "prime_price": 2,
    "discount": 2,
    "coupon": 1,
    "saving": 1,
    "promotion": 1,
    "promotion_code": 1,
    "rating": 4.9,
    "review": 29,
    "bought": 800,
    "a_rank_name": 'Toys & Games',
    "a_rank": 12816,
    "b_rank_name": 2,
    "b_rank": 2,
    "c_rank_name": 2,
    "c_rank": 2,
    "d_rank_name": 2,
    "d_rank": 2,
}
columns = ', '.join(data_dict.keys())
placeholders = []
for d in data_dict:
    placeholders.append('%s')
placeholders_str = ', '.join(placeholders)
values = tuple(data_dict.values())
# 构建插入或更新语句
query = (
    f'REPLACE INTO asin_info_current ({columns}) VALUES ({placeholders_str})'
)
print(columns)
print(placeholders_str)
print(values)
print(query)
try:
    cursor.execute(query, values)
    connection.commit()
except pymysql.Error as e:
    print("执行更新出错:", e)
print(result)

# 提交更改并关闭连接
connection.commit()


data_dict2 = {
    'asin': 'TEST_D_3',
    'country': 'us',
    #'time': datetime.now().strftime("%Y-%m-%d"),
    'time': None,
    'image': 'https://m.media-amazon.com/images/I/91fSsBq-QUL._AC_UL320_.jpg',
    'title': 'JOYIN Dinosaur Truck for Kids with 6 Soft Rubber Dinosaur Car Vehicles, 1 Toy Dinosaur Transport Carrier Truck with Music and Roaring Sound, Flashing Lights, Mini Dinosaur Car Playset, Gift for Boys',
    'brand': 'JOYIN',
    'merchant_token': 1,
    'amz_choice': 'XXXXX',
    'best_seller': 1,
    'deal_type': 1,
    'is_deal': 1,
    'is_fba': 1,
    'is_amz': 1,
    'is_smb': 1,
    "left_count": 3,
    "lower_price": 3,
    "lower_list": 3,
    "lowest_precent": 3,
    "sale_price": 339.99,
    "rrp_price": 339.99,
    "rrp_type": 3,
    "prime_price": 3,
    "discount": 3,
    "coupon": 3,
    "saving": 3,
    "promotion": 3,
    "promotion_code": 3,
    "rating": 4.9,
    "review": 39,
    "bought": 800,
    "a_rank_name": 'Toys & Games',
    "a_rank": 33836,
    "b_rank_name": 3,
    "b_rank": 3,
    "c_rank_name": 3,
    "c_rank": 3,
    "d_rank_name": 3,
    "d_rank": 2
}
result = db_util.replace_by_dict('asin_info_current', data_dict2)
print(result)
# 执行查询
select_sql = "SELECT * FROM asin_info_current"
results = db_util.query(select_sql)
if results:
    for row in results:
        print(row)

results = db_util.query(SQLStatements.SELECT_PRODUCTS)

# 断开数据库连接
db_util.disconnect()