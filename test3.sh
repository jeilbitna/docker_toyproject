#!/bin/bash

# apache benchmark 로 http://211.183.3.102 로 트래픽 발생시키고 result.txt에 저장함.
ab -n 500000 -c 3 http://211.183.3.102:8080/ > result3.txt

echo "---------- 5초간 대기하기 ----------"

sleep 5

# makejson.py 실행해서 elasticsearch로 보내줌
python3 makejson3.py 

#sleep 5

#echo "---------- 남은 파일 제거 ----------"
# 남은 파일 제거(result.txt, result.json)
#rm result.txt result.json
