#!/bin/bash

# 결과 파일 디렉토리 지정
RESULT_DIR="/home/user1/apachebench/results/"

echo "이전에 실행된 결과 파일을 삭제하시겠습니까? (y/n): "
read deleteOldFiles

if [[ "$deleteOldFiles" == "y" ]]; then
    # 이전 결과 파일 전체 삭제
    rm -f ${RESULT_DIR}result*.txt ${RESULT_DIR}result*.json
    RESULT_PREFIX="result"
else
    # 새로운 파일명으로 저장
    i=1
    while [[ -e "${RESULT_DIR}result$i.txt" ]] || [[ -e "${RESULT_DIR}result$i.json" ]]; do
        let i++
    done
    RESULT_PREFIX="result$i"
fi

# 사용자로부터 Apache Benchmark 설정 받기
echo "Apache Benchmark 설정:"
read -p "-n (총 요청 수)를 입력하세요: " n
read -p "-c (동시 요청 수)를 입력하세요: " c

# 사용자로부터 Elasticsearch 인덱스 이름 받기
read -p "Elasticsearch 인덱스 이름을 입력하세요: " index_name

# Apache Benchmark 실행
ab -n $n -c $c http://211.183.3.102:8080/ > "${RESULT_DIR}${RESULT_PREFIX}.txt"

echo "5초간 대기"
sleep 5

# makejson.py 스크립트 실행, 인덱스 이름을 인자로 전달
python3 makejson.py "${RESULT_DIR}${RESULT_PREFIX}.txt" "${RESULT_DIR}${RESULT_PREFIX}.json" "$index_name"

echo "작업 완료"

