import os
from config import settings
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Agg 백엔드 사용


def generate_wordcloud(frequency_data):
    word_frequency = {}

    # 빈도수에 따라 단어 카운트 생성
    for record in frequency_data:
        word_frequency[record[1]] = record[2]

    font_path = 'C:/Windows/Fonts/malgun.ttf'

    # 워드클라우드 생성
    wordcloud = WordCloud(width=800, height=400, background_color='black', font_path=font_path).generate_from_frequencies(word_frequency)

    # 이미지 저장
    image_dir = os.path.join(settings.BASE_DIR, 'static', 'wordcloud_images')
    image_path = os.path.join(image_dir, 'wordcloud.png')

    # 디렉토리가 존재하지 않으면 생성
    os.makedirs(image_dir, exist_ok=True)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(image_path, format='png')
    plt.close()

    image_url = '/static/wordcloud_images/wordcloud.png'
    return image_url

# #테스트용 코드 주석처리
# frequency_data=check_cache_and_collect_data()
# generate_wordcloud(frequency_data)
# print("서버 종료?")