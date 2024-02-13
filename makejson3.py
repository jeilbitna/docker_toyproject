from elasticsearch import Elasticsearch
import json
import re
import sys
from datetime import datetime

# Apache Benchmark 결과 데이터
ab_result = """ """

with open('result3.txt', 'r') as file:
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
    r"Transfer rate:\s*([\d.]+) \[Kbytes/sec\] received": "transfer_rate"
}

# 결과 문자열에서 정보 추출
for line in ab_result.splitlines():
    for pattern, key in patterns.items():
        match = re.search(pattern, line)
        if match:
            result_data[key] = float(match.group(1)) if '.' in match.group(1) else int(match.group(1))

# timestamp 추가
result_data["@timestamp"] = datetime.now().isoformat()

# JSON 형식으로 변환
json_data = json.dumps(result_data, indent=4)

with open('result3.json', 'w') as f:
    json.dump(result_data, f, indent=4)

es = Elasticsearch('http://localhost:9200')

with open('result3.json', 'r') as file:
    doc = json.load(file)

res = es.index(index="ab-results3-2", body=doc)
print(res['result'])

