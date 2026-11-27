# 한 판이 끝난 Dedicated Server를 교체하고 대기 서버 유지하기

상태는 활성입니다. 2026-11-25에 공식 문서를 확인했습니다.

## 사용 방법

한 프로세스가 한 판을 맡는 방식에서는 Dedicated Server가 시작해 준비 상태를 알리고, 판을 진행한 뒤 종료합니다. 다음 파티가 서버 부팅을 기다리지 않도록 대기 서버를 미리 띄워 둡니다. 수동으로 운영하는 GameLift Anywhere 환경에서는 런처나 프로세스 관리 도구가 새 서버를 띄우고 준비 신호를 기다릴 수 있습니다. Amazon GameLift Servers Agent도 설정에 따라 등록과 프로세스 실행을 맡을 수 있습니다.

Docker는 서버와 실행에 필요한 파일을 이미지로 묶습니다. 컨테이너는 그 이미지가 실제로 실행된 상태입니다. Kubernetes는 배포된 컨테이너를 관리하고, Agones는 그 위에 게임 서버의 준비, 배정, 종료 관리를 더합니다. Agones Fleet은 서버 템플릿과 목표 개수를 정합니다. `Ready`는 배정 가능한 서버, `Allocated`는 판에 배정된 서버를 뜻합니다. `Shutdown()`을 호출하면 GameServer와 이를 실행하는 Pod가 종료됩니다.

## 적용 범위

한 프로세스가 한 판을 맡는 것은 게임의 선택입니다. 판 뒤에 상태를 초기화하는 게임은 같은 서버를 대기로 돌려 재사용할 수 있습니다. Agones Fleet의 고정 개수에는 준비된 서버와 배정된 서버가 모두 들어갑니다. 판이 진행 중이어도 일정한 대기 서버가 필요하면 `FleetAutoscaler`의 Buffer 정책으로 정해진 범위 안에서 서버 수를 조절합니다.

## 확인 방법

대기 서버에 판을 배정하고 게임의 정상 종료 흐름을 밟은 뒤, 다음 판을 받을 만큼 서버가 `Ready`가 되는지 확인합니다. 여러 판이 동시에 열릴 때는 대기 중과 사용 중인 서버 개수를 따로 봅니다.

## 근거

- GameLift Anywhere의 수동 실행, Agent, 준비 신호. [AWS Anywhere Fleet](https://docs.aws.amazon.com/gameliftservers/latest/developerguide/fleets-creating-anywhere.html)
- Agones Fleet 개수와 Buffer 정책, 준비와 종료 및 재사용. [Fleet](https://agones.dev/site/docs/reference/fleet/) [FleetAutoscaler](https://agones.dev/site/docs/reference/fleetautoscaler/) [Game Server SDKs](https://agones.dev/site/docs/guides/client-sdks/)
- Docker 이미지와 컨테이너. [Docker 문서](https://docs.docker.com/learn/content/what-is-a-container/)
- 실제로 판을 열어 종료하거나 부하를 주는 검증은 이번 문서 확인에 포함되지 않았습니다.
