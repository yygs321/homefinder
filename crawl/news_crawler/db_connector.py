import mysql.connector
import redis
from config.db_config import MYSQL_DB_CONFIG, REDIS_CONFIG
from datetime import datetime


# Redis 연결 설정
redis_client = redis.StrictRedis(host=REDIS_CONFIG['host'], port=REDIS_CONFIG['port'], db=REDIS_CONFIG['db'])


def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=MYSQL_DB_CONFIG['host'],
            user=MYSQL_DB_CONFIG['user'],
            password=MYSQL_DB_CONFIG['password'],
            database=MYSQL_DB_CONFIG['database']
        )
        print("MySQL 데이터베이스 연결 성공!")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")

    return connection

def save_to_db(frequency_data):
    connection = create_connection()
    cursor = connection.cursor()

    # 기존 데이터 삭제
    delete_query = "DELETE FROM NewsFrequency;"
    cursor.execute(delete_query)

    # 새 데이터 삽입
    insert_query = """
    INSERT INTO NewsFrequency (category, value, count, date)
    VALUES (%s, %s, %s, %s);
    """

    try:
        cursor.executemany(insert_query, frequency_data)
        connection.commit()
        print("데이터 저장 완료!")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()
        connection.close()