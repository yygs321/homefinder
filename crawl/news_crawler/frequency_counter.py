def count_frequency(title, frequency_data, pub_date):
    transaction_methods = ['매매', '전세', '월세', '보증금', '분양', '재건축']
    real_estate_types = ['아파트', '오피스텔', '빌라', '원룸']
    districts = ['강남', '강동', '강북', '강서', '관악', '광진', '구로', '금천', '노원', '도봉', '동대문', '동작', '마포', '서대문', '서초', '성동', '성북', '송파', '양천', '영등포', '용산', '은평', '종로', '중구', '중랑']

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
