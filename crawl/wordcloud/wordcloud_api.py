from django.http import JsonResponse
from crawl.news_crawler.news_crawler import check_cache_and_collect_data
from wordcloud_generator import generate_wordcloud
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/get-wordcloud', methods=['GET'])
def create_wordcloud():
    frequency_data = check_cache_and_collect_data()
    if not frequency_data:
        return jsonify({"error": "데이터가 없습니다."}), 404

    # 워드클라우드 이미지 생성
    generate_wordcloud(frequency_data)

    image_url = f'crawl/wordcloud/static/wordcloud_images/wordcloud.png'

    # 클라이언트에게 이미지 URL 반환
    return jsonify({'image_url': image_url})
