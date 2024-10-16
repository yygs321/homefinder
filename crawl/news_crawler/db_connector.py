import mysql.connector
import redis
from crawl.news_crawler.db_config import MYSQL_DB_CONFIG, REDIS_CONFIG
from datetime import datetime, timedelta

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
        print("MySQL DB에 데이터 저장")
    except mysql.connector.Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()
        connection.close()

# redis에 데이터 저장
def save_to_redis(frequency_data):
    for record in frequency_data:
        category, value, count, date = record

        redis_key = f"{category}:{value}"
        redis_client.hmset(redis_key, {"count": count, "date": date})
    print(f"Redis에 데이터 저장")


def check_cache_and_update_if_needed():
    keys = redis_client.keys()
    if not keys:  # 캐시가 없으면 크롤링 진행
        print("캐시 데이터가 없어 크롤링 진행")
        return True

    # 첫 번째 데이터의 날짜 확인
    cached_data = redis_client.hgetall(keys[0])
    cached_date = datetime.strptime(cached_data['date'], '%Y-%m-%d')

    if datetime.now() - cached_date > timedelta(days=7):
        print("캐시가 만료되어 크롤링 진행")
        return True

    print("캐시가 유효하여 크롤링을 진행하지 않습니다.")
    return False