from elasticsearch import Elasticsearch
import json
import re
import sys

# 명령줄 인자로부터 결과 파일 경로와 인덱스 이름 받기
input_file_path = sys.argv[1]
output_file_path = sys.argv[2]
index_name = sys.argv[3]  # 사용자가 입력한 인덱스 이름

# Apache Benchmark 결과 데이터 읽기
with open(input_file_path, 'r') as file:
    ab_result = file.read()

# 결과 데이터를 저장할 딕셔너리
result_data = {}

# 필요한 정보를 추출하기 위한 정규 표현식 패턴과 키 매핑
patterns = {
    r"Requests per second:\s*([\d.]+)": "requests_per_second",
    r"Total transferred:\s*(\d+) bytes": "total_transferred",
    r"HTML transferred:\s*(\d+) bytes": "html_transferred",
    r"Time taken for tests:\s*([\d.]+) seconds": "time_taken_for_tests",
    r"Complete requests:\s*(\d+)": "complete_requests",
    r"Failed requests:\s*(\d+)": "failed_requests",
    r"Concurrency Level:\s*(\d+)": "concurrency_level",
    r"Transfer rate:\s*([\d.]+) \[Kbytes/sec\] received": "transfer_rate",
    #timeout으로 실패한 요청 수
    r"Non-2xx responses:\s*(\d+)": "non_2xx_responses"  # 2xx가 아닌 응답의 수

}

# 결과 문자열에서 정보 추출
for line in ab_result.splitlines():
    for pattern, key in patterns.items():
        match = re.search(pattern, line)
        if match:
            result_data[key] = float(match.group(1)) if '.' in match.group(1) else int(match.group(1))

# JSON 형식으로 변환하여 파일에 저장
with open(output_file_path, 'w') as f:
    json.dump(result_data, f, indent=4)

# Elasticsearch 인스턴스 생성
es = Elasticsearch('http://localhost:9200')

# Elasticsearch에 데이터 저장, 사용자가 입력한 인덱스 이름 사용
res = es.index(index=index_name, body=result_data)
print(res['result'])

