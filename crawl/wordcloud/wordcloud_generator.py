import os

from wordcloud import WordCloud
import matplotlib.pyplot as plt

from crawl.news_crawler.news_crawler import check_cache_and_collect_data


def generate_wordcloud(frequency_data):
    word_frequency = {}

    # 빈도수에 따라 단어 카운트 생성
    for record in frequency_data:
        word_frequency[record[1]] = record[2]

    # 워드클라우드 생성
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_frequency)

    # 이미지 저장
    image_dir = 'static/wordcloud_images'
    image_path = os.path.join(image_dir, 'wordcloud.png')

    # 디렉토리가 존재하지 않으면 생성
    os.makedirs(image_dir, exist_ok=True)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(image_path, format='png')
    plt.close()

# frequency_data=check_cache_and_collect_data()
# generate_wordcloud(frequency_data)