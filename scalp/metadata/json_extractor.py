# 필요한 라이브러리들을 임포트
import os
import json
from collections import defaultdict
import numpy as np

# JSON 파일에서 데이터를 로드하는 함수
def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# 나이와 성별 정보를 결합하여 그룹화 키를 생성하는 함수
def get_age_gender_group(data):
    age = data.get('age', 'Unknown')
    gender = data.get('gender', 'Unknown')
    if age.isdigit():
        age_num = int(age)
        if age_num >= 60:
            age = '60세 이상'
        else:
            age = f"{(age_num // 10) * 10}대"  # 나이를 10대, 20대, ... 로 변환
    return f"{age} {gender}"

# 두 폴더 내의 공통 파일들을 찾는 함수
def get_common_files(folder1, folder2):
    files1 = {f.replace('_META.json', '.json') for f in os.listdir(folder1) if f.endswith('_META.json')}
    files2 = set(os.listdir(folder2))
    return files1.intersection(files2)

# 주어진 폴더들에서 데이터를 처리하는 함수
def process_folders_modified(base_path, meta_folder, data_folder):
    age_gender_sums = defaultdict(lambda: defaultdict(float))
    age_gender_counts = defaultdict(lambda: defaultdict(int))
    age_gender_values = defaultdict(lambda: defaultdict(list))
    age_gender_total_values = defaultdict(list)  # 새로 추가: 그룹별 총합을 저장하기 위한 딕셔너리

    meta_folder_path = os.path.join(base_path, meta_folder)
    data_folder_path = os.path.join(base_path, data_folder)
    common_files = get_common_files(meta_folder_path, data_folder_path)

    total_common_files = len(common_files)
    print(f"Total common files: {total_common_files}")

    file_count = 0
    for file_name in common_files:
        file_count += 1

        if file_count % 10 == 0:
            print(f"Processing file {file_count}...")

        meta_file_path = os.path.join(meta_folder_path, file_name.replace('.json', '_META.json'))
        data_file_path = os.path.join(data_folder_path, file_name)
        meta_data = load_json_data(meta_file_path)
        data = load_json_data(data_file_path)

        group = get_age_gender_group(meta_data)
        total_value_for_file = 0  # 새로 추가: 파일별 총합을 계산하기 위한 변수

        for i in range(1, 7):
            value_key = f"value_{i}"
            value = data.get(value_key, 0)
            if isinstance(value, str):
                value = float(value) if '.' in value else int(value)
            age_gender_sums[group][value_key] += value
            age_gender_counts[group][value_key] += 1
            age_gender_values[group][value_key].append(value)
            total_value_for_file += value  # 새로 추가: 총합에 현재 value 추가

        age_gender_total_values[group].append(total_value_for_file)  # 새로 추가: 그룹별 총합에 파일별 총합 추가

    # 평균, 분산, 표준편차를 계산하고 출력 (기존 코드)
    print(f"Processed {file_count} files. Current averages and standard deviations:")
    for group in sorted(age_gender_sums.keys()):
        values = age_gender_sums[group]
        print(f"Group: {group}")
        for key, sum_val in values.items():
            avg_value = sum_val / age_gender_counts[group][key]
            variance = np.var(age_gender_values[group][key])
            std_dev = np.sqrt(variance)
            print(f"  {key} -> Average: {avg_value:.2f}, Variance: {variance:.2f}, Standard Deviation: {std_dev:.2f}")

    # 총합, 평균, 분산, 표준편차 출력 (새로 추가)
    print("\nGroup-wise Total Sums, Averages, Variances, and Standard Deviations (Sorted):")
    sorted_groups = sorted(age_gender_total_values.keys())  # 그룹 이름을 오름차순으로 정렬
    for group in sorted_groups:
        total_values = age_gender_total_values[group]
        avg = np.mean(total_values)
        var = np.var(total_values)
        std_dev = np.std(total_values)
        print(f"Group: {group} -> Average: {avg:.2f}, Variance: {var:.2f}, Standard Deviation: {std_dev:.2f}")

    print(f"Total processed files: {file_count}")

    if file_count == total_common_files:
        print("All common files were successfully processed.")
    else:
        print(f"Some common files were not processed. Processed {file_count} out of {total_common_files} files.")


# 파일 경로 설정
base_path = 'C:\\Users\\KOLO\\PycharmProjects\\json_realationship\\head_ai'
meta_folder = 'metadata_json\\metadata_json'
data_folder = 'anotation_json\\anotation_json'

# 함수 호출하여 데이터 처리
process_folders_modified(base_path, meta_folder, data_folder)
