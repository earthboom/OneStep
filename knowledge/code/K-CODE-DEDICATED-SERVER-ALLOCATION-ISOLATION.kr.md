# 브랜치마다 올바른 Dedicated Server에 판을 배정하기

상태는 활성입니다. 2026-11-25에 공식 문서를 확인했습니다.

## 사용 방법

Dedicated Server는 화면을 그리지 않고 접속한 플레이어들의 게임 진행을 계산합니다. 매치 서비스가 플레이어를 모아 새 판을 요청하면, 배정 서비스가 대기 중인 서버를 고릅니다. 클라이언트는 배정 결과에 담긴 주소와 포트로 접속합니다.

GameLift Anywhere에서 compute는 직접 준비해 등록한 호스트입니다. 서버 프로세스는 이 compute의 설정과 유효 기간이 있는 인증 토큰으로 AWS에 연결하고 `ProcessReady()`로 준비 상태를 알립니다. Fleet은 배정 대상이 될 서버 자원의 묶음이고, `CreateGameSession`은 지정된 Fleet과 위치의 대기 프로세스에 판을 엽니다. Agones의 `GameServerAllocation`도 Fleet 라벨 등의 조건으로 준비된 서버를 고를 수 있습니다.

## 적용 범위

브랜치별로 빌드가 섞이면 안 되는 테스트에서는 서버가 등록된 Fleet과 매치 서비스가 요청하는 Fleet을 맞춥니다. 대체 대상을 고르는 설정이 있다면 함께 살핍니다. 같은 호스트 주소와 전송 방식으로 여러 서버를 동시에 띄울 때는 각 프로세스의 포트를 나눕니다. 클라이언트가 받은 주소와 포트에도 접속할 수 있어야 합니다. 사설 IP는 경로가 있는 사내망이나 VPN에서 사용할 수 있습니다. 클라이언트와 서버의 패킷 규칙과 게임에서 일치를 요구하는 데이터도 호환되어야 합니다.

## 확인 방법

다른 PC의 클라이언트로 브랜치마다 판을 요청해 올바른 서버 빌드에 배정되는지, 실제로 접속되는지 확인합니다. 한 브랜치에 빈 서버가 없을 때 다른 브랜치에 배정되는지도 확인합니다.

## 근거

- Dedicated Server와 클라이언트 관계. [Epic Games 문서](https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-dedicated-servers-in-unreal-engine)
- Compute, Fleet, 토큰, 준비 신호, 판 생성과 접속 정보. [AWS Anywhere Fleet](https://docs.aws.amazon.com/gameliftservers/latest/developerguide/fleets-creating-anywhere.html) [CreateGameSession](https://docs.aws.amazon.com/gameliftservers/latest/apireference/API_CreateGameSession.html) [GameSession](https://docs.aws.amazon.com/gameliftservers/latest/apireference/API_GameSession.html)
- Agones의 Fleet 선택 방식. [GameServerAllocation](https://agones.dev/site/docs/reference/gameserverallocation/)
- 배정, 접속, 빌드 호환성은 실제 서버에서 실행해 확인하는 단계가 남아 있습니다.
