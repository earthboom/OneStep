# 아핀 변환·주사선별 의사 원근

기준 항목: K-GAME-TECH-RETRO · 확인일: 2026-11-07 · 참고 지식. 엔진 실행·성능·실제 플레이 검증은 별도다.

## 원리와 구현 요점

수학적 유도: 2D 아핀 변환 p'=A*p+b는 평행성을 유지한다. 바닥 원근 표현은 깊이별 배율이 필요하므로 주사선마다 아핀 매개변수를 바꾸는 식으로 근사할 수 있다. 평면 지면의 스타일화 효과나 고전 렌더링 학습에 쓴다.

### 추가 조사로 보완한 구현

bsnes의 renderMode7은 부호 있는 행렬 계수·중심·오프셋을 읽고 고정소수점 절삭으로 주사선 원점을 계산한다. 이후 행렬 증분으로 소스 좌표를 진행시키고 타일·팔레트·영역 밖 처리를 적용한다. README보다 구체적인 래스터 구현을 확인했다. 의사 원근 바닥은 게임이 주사선별 매개변수를 바꿔야 하며 단일 아핀 변환만으로는 부족하다. 정확한 에뮬레이션에서는 부호 비트 폭·중간 절삭·범위 처리·레지스터 래치 타이밍을 임의의 실수 연산으로 대체하지 않는다.

## 적용 조건과 한계

bsnes의 아핀 샘플링 코드를 확인했다. 하드웨어 버스 타이밍·레지스터 래치 정확성·원본 마리오 카트의 주사선 코드는 이 렌더러 읽기만으로 입증되지 않는다.

## 적용 전 점검

적용 전 점검: 체크무늬로 일반 변환을 확인하고 정확한 Mode 7 구현 전 에뮬레이터·하드웨어 출처를 추가 확인한다.

## 근거

- [Godot — Matrices and transforms](https://docs.godotengine.org/en/latest/tutorials/math/matrices_and_transforms.html)
- [DerKoun — bsnes-hd README](https://github.com/DerKoun/bsnes-hd/blob/master/README.md)

### 추가 조사 출처

- [bsnes — renderMode7 source](https://github.com/bsnes-emu/bsnes/blob/master/bsnes/sfc/ppu-fast/mode7.cpp) — renderMode7; public master source read 2026-11-07, no emulator/hardware run; original Mario Kart code and cycle-exact timing not established.

추가 조사 출처의 영문 주석은 정확한 절·함수·접근 범위를 보존한다. 원본 슬라이드·문서·공개 코드의 확인과 실제 엔진·하드웨어 실행은 구분한다. 영상 설명·세션 개요만 확인한 자료를 전체 발표 확인으로 간주하지 않는다.

출발 영상: V57. [영상별 대응표](K-GAME-TECH-GUIDE.kr.md).
