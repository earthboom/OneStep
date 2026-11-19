# 롤백 재시뮬레이션과 외부 보상 확정 분리하기

**K-GAME-TECH-ROLLBACK** · 입력을 예측하고 스냅샷을 복원해 정정된 틱을 다시 계산한다. 되돌릴 수 없는 보상은 신뢰 가능한 확정 이후에 부여하고 재시도에는 안정적인 키를 쓴다.

## 지침

롤백 넷코드는 미수신 입력을 예측하고 시뮬레이션 상태를 저장한 뒤 실제 입력이 다르면 복원해 다시 계산한다. 예측으로 표시한 소리·파티클·UI도 취소하거나 바로잡는다. 업적이나 재화 같은 비가역적 효과는 자격이 확정된 뒤 지급한다. 세션·이벤트·수신자를 구분하는 멱등 키로 재생과 전달 재시도 중 같은 지급을 식별한다.

## 적용 조건과 예외

롤백 시뮬레이션은 복원된 상태와 입력 순서로 합의된 결과를 재계산할 수 있어야 하고 연산 예산도 충족해야 한다. 피어 프로토콜에서는 최종 입력·검증 상태에 합의하고, 권위형 게임은 권한을 가진 주체가 자격을 확정한다. 애니메이션 완료나 시간 경과로 확정을 대신할 수 없다. 재시작을 넘는 전달에는 영속 상태와 수신자 측 계약도 필요하다.

## 확인 방법

오예측·순서가 바뀐 입력을 주입해 최종 상태 해시를 비교한다. 예측한 KO가 방어로 바뀌면 외부 지급은 0건이어야 한다. 확정 보상을 재생·재시도해도 효과는 한 번만 적용돼야 한다. 같은 틱의 별개 이벤트와 수신자, 확인 응답 손실, 재시작 후 복구를 검사한다.

## 근거

GGPO는 예측과 재시뮬레이션을, Photon Quantum은 예측·검증 프레임과 예측 이벤트 취소를 설명한다. 기존 합성 이벤트 추적에서는 중복 제거만 했을 때 잘못된 지급이 남았다. 네트워크 결정성과 영속 보상 서비스는 확인하지 않았다. 외부 전달은 별도의 설계 요건이다.

- [GGPO — Rollback Networking SDK](https://www.ggpo.net/)
- [Glenn Fiedler — Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)
- [Photon Quantum 3 — Frames, “Which Frame To Read In The View”](https://doc.photonengine.com/quantum/v3/manual/frames)
- [Photon Quantum 2.1.9 — CallbackEventCanceled](https://doc-api.photonengine.com/en/quantum/v2/class_quantum_1_1_callback_event_canceled.html)


## 언리얼 접촉 롤백 검증 — 2026-11-20

이 실험에서는 입력 대기와 예측·롤백이 240틱 전체 상태와 접촉 두 건을 동일하게 확정했다. 예측 접촉 두 건을 취소했고, 34회 복원·181틱 재실행과 회차별 반응·프레임 비용을 기록했다.
