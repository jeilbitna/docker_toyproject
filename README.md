![image](https://github.com/jeilbitna/docker_toyproject/assets/96589387/9ee3f236-3b5c-4591-8206-6c1f724daf3e)


**1. Clustering**
- docker swarm
- ansible playbook


**2. Deploy**
- docker stack


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

**4. Apache Benchmark**
- bare-metal 방식 사용
- 임의로 Worker의 nginx container에 traffic 발생
- 발생한 traffic 을 metricbeat 에서 감지 & data를 Manager 의 elasticsearch 로 전송
