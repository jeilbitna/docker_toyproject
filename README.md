![image](https://github.com/jeilbitna/docker_toyproject/assets/96589387/9ee3f236-3b5c-4591-8206-6c1f724daf3e)


**1. Clustering**
- docker swarm
  - pip 모듈에 docker 등록
  - ansible playbook 방식으로 deploy
  
- ansible playbook
  - ssh 연결
  - host 등록


**2. Deploy**
- docker stack
  1) Manager
     - elasticsearch
     - kibana
  2) Worker
     - metricbeat
     - nginx
     
**3. Visualization**
- elasticsearch
  - container 방식 사용
  - metricbeat 에서 data를 받아서 저장
  - 로컬에 임의의 volume 과 mount 하여, docker stack deploy 를 갱신해도 이전 데이터가 남아있음
  
- kibana
  - container 방식 사용
  - elasticsearch 와 연동되어 시각화
  
- metricbeat
  - container 방식 사용
  - 발생한 traffic 감지 -> elasticsearch 로 전달
 
+ Container 개수 1/10/50 개 일 때 Traffic 30/50/100만 개 요청하여 비교하기

**4. Apache Benchmark**
- bare-metal 방식 사용
- 임의로 Worker의 nginx container에 traffic 발생
- 발생한 traffic 을 metricbeat 에서 감지 & data를 Manager 의 elasticsearch 로 전송
