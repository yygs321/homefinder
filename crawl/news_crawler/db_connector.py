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
        # hmset으로 값을 저장할 때 모든 값은 문자열로 저장됨
        redis_client.hmset(redis_key, {"count": count, "date": date})
    print(f"Redis에 데이터 저장")


def check_cache_and_update_if_needed():
    keys = redis_client.keys()
    if not keys:  # 캐시가 없으면 크롤링 진행
        print("캐시 데이터가 없어 크롤링 진행")
        return True

    cached_data = redis_client.hgetall(keys[0])
    if b'date' in cached_data:
        # 바이트 문자열을 UTF-8로 디코딩
        cached_date = datetime.strptime(cached_data[b'date'].decode('utf-8'), '%Y-%m-%d')

    if datetime.now() - cached_date > timedelta(days=7):
        print("캐시가 만료되어 크롤링 진행")
        return True

    print("캐시가 유효하여 크롤링을 진행하지 않습니다.")
    return False

def get_cached_data():
    keys = redis_client.keys()
    all_data = []

    for key in keys:
        key_decoded = key.decode('utf-8')
        category, value = key_decoded.split(':')

        cached_data = redis_client.hgetall(key)

        count = int(cached_data[b'count'])  # count는 정수로 변환
        date = cached_data[b'date'].decode('utf-8')  # date는 UTF-8로 변환

        # 데이터를 리스트에 추가
        all_data.append((category, value, count, date))

    return all_data