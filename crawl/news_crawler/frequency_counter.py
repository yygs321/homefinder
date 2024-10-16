def count_frequency(title, frequency_data, pub_date):
    transaction_methods = ['매매', '전세', '월세']
    real_estate_types = ['오피스텔', '빌라', '원룸']
    districts = ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구', '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구']

    for transaction_method in transaction_methods:
        if transaction_method in title:
            update_or_add_frequency(frequency_data, '거래방식', transaction_method,pub_date)

    for estate_type in real_estate_types:
        if estate_type in title:
            update_or_add_frequency(frequency_data, '부동산종류', estate_type,pub_date)

    for district in districts:
        if district in title:
            update_or_add_frequency(frequency_data, '자치구', district,pub_date)

    return frequency_data

def update_or_add_frequency(frequency_data, category, value,pub_date):
    # 해당 데이터가 이미 존재하면 빈도수만 +1
    for record in frequency_data:
        if record[0] == category and record[1] == value:
            record[2] += 1
            return

    # 없으면 새로 추가
    frequency_data.append([category, value, 1, pub_date.strftime('%Y-%m-%d')])
