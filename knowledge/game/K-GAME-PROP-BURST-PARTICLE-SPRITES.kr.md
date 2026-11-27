# 상자·폭발·먼지 스프라이트의 종료 상태와 노출 시간 설계

열린 상자는 마지막 자세를 유지하고, 폭발은 사라지며, 바람 먼지는 각 입자의 수명이 서로 다른 시점에 끝난다. 먼저 플레이어가 마지막에 무엇을 봐야 하는지 정한다. 아래의 노출표는 고정 카메라와 투명 시트를 전제로 한 연습 설계다. 기존 부두 착지 예시에서 관찰한 결과와 구분한다.

## 그리는 방법

- **경첩 달린 상자.** 같은 시점에서 닫힘과 열림을 그리고 뒤쪽 경첩 양 끝, 뚜껑의 앞 모서리와 몸체의 고정점을 표시한다. 뚜껑 안쪽, 테두리와 빈 내부를 설계한다. 중간 자세에서 어느 면이 앞턱 뒤로 가는지 정하고 두께와 걸쇠의 투영을 추적한다. 발과 몸체는 승인된 레이어를 재사용한다. 시점이 여러 개면 간단한 경첩 모형으로 호를 확인한다. 닫는 동작은 별도로 설계할 수 있다. Frakassets의 10프레임 열림·6프레임 닫힘은 한 작가의 사례다. 무거운 쇠 상자와 가볍게 튀는 상자는 같은 타이밍을 요구하지 않는다.
- **폭발.** 시작점과 범위를 고정하고 응축된 시작, 불균일한 최대 충격, 틈이 벌어진 꼬리를 검은 실루엣으로 재생한다. 대표 돌출부 두 개가 어디로 이동하고 갈라지는지 따라간다. 밝은 중심이 꺼진 뒤에도 연기는 커질 수 있다. GDC의 블로킹 사례처럼 주요 프레임의 외곽부터 확인한 뒤 조각과 연기의 변화 경로를 그린다. 신호 범위와 예고 시간은 실제 게임 이벤트에 맞춘다.
- **바람 먼지.** 특정 순간에 창턱을 지나는 바람을 단일 클립으로 낼 때는 공통 캔버스 위에 여러 알갱이의 이동과 어긋난 탄생을 굽는다. 반복 클립은 경계 양쪽의 밀도·방향·속도를 맞춘다. 방출기용 시트에서는 안정된 피벗 주위에 한 입자가 생겨 흐트러지고 사라지는 모양만 그린다. 세계 이동, 생성 위치, 시점과 수명은 방출기가 맡는다. 단발 입자의 변형 행은 생성 시 고르고 같은 행에서 나이에 따라 진행한다. 무작위 시작 프레임은 소멸 직전부터 보일 수 있다.

## 노출표와 판정 예시

시간은 각 셀의 시작이며 다음 경계는 포함하지 않는다. 좌표 원점은 왼쪽 위다.

| 대상 | 제안한 키 | 내보낸 뒤 확인할 것 |
| --- | --- | --- |
| 상자, 48×48, 피벗 (24, 43) | 0 ms 닫힘, 80 잠금 해제, 140 뚜껑이 턱을 넘음, 200 안쪽 노출, 280 열린 끝점, 360 안정 | 유효한 상호작용에서 한 번 시작하고 열린 상태가 지속되는지 확인한다. 광택과 보상 레이어를 가리고, 잘라낸 프레임에서 경첩과 바닥 모서리를 겹쳐 본다. 열린 뒤 재입력 규칙도 확인한다. |
| 폭발, 64×64, 원점 (32, 32) | 0 ms 작은 섬광, 35 비대칭 확장, 80 최대 연기와 줄어드는 중심, 145 갈라짐, 230 남은 파편, 340 비움 | 밝고 어두운 배경에서 실루엣과 채색본을 비교한다. 340 ms 뒤 잔상이 없고 다시 실행하면 첫 셀부터 시작해야 한다. 런타임에서 명시적으로 지워도 된다. |
| 먼지, 16×16, 수명 400 ms | 뭉침·가장자리 풀림·분리·마지막 점을 정규화 나이 [0, .25), [.25, .55), [.55, .80), [.80, 1)에 배치한다. 시작은 0, 100, 220, 320 ms다. | 0과 160 ms에 생성하면 240 ms에서 첫 입자는 셀 3, 둘째는 셀 1이다. 방출을 멈추면 560 ms에 마지막 입자도 사라진다. 단일 합성 시트에서도 같은 순간들을 비교한다. |

## 진단과 근거의 범위

상자가 들리면 원본 몸체와 잘라낸 셀을 각각 겹쳐 작화 이동과 트림 오프셋을 구분한다. 폭발이 부풀기만 하면 외곽만 재생한 뒤 내부 밝기와 피크를 따로 본다. 먼지는 밝고 어두운 배경의 단일 시트, 바람을 끈 입자 하나, 시차를 둔 입자 무리 순으로 확인한다. 이중 이동이면 셀과 방출기의 역할을 나누고 일제히 맥동하면 생성 간격을 고친다. 사각 테두리는 알파·블렌딩·필터를 조사한다. 실제 엔진의 행 순서로 다시 잘라 빈 프레임의 삭제나 중복 프레임 병합이 홀드·제거 의미를 바꾸는지 본다.

Unity 텍스처 시트는 행과 수명·속도·FPS 기준을 선택할 수 있다. Godot 4.5에서는 CanvasItemMaterial의 파티클 애니메이션, 가로·세로 프레임 수와 진행 설정을 확인한다. Aseprite의 빈 프레임 제외, 중복 병합과 패딩을 확인한다. 이는 문서에 근거한 경로다. 세 연습의 엔진 임포트, 관찰자의 인지율, 생성기 합격률은 측정하지 않았다. 플레이어 검수는 같은 크기와 배경에서 설명 없이 무엇이 어디서 변하고 끝에 무엇이 남았는지 묻는다.

## 출처

[dock-landing study](https://github.com/earthboom/OneStep/blob/b04100021437b4489116e97199fca61ef0507526/output/2d-character-test/landing-effects-01/example.md) · [Dynamic Sprites](https://onlinelibrary.wiley.com/doi/10.1002/cav.1608) · [As-Rigid-As-Possible Shape Manipulation](https://www-ui.is.s.u-tokyo.ac.jp/~takeo/research/rigid/) · [Creator’s sheet layout and playback notes](https://frakassets.itch.io/treasure-chests-pack) · [Wishforge Games opening tutorial](https://www.youtube.com/watch?v=A12wj5MGRi8) · [Lyndon’s GDC blocking example and notes](https://media.gdcvault.com/gdc2018/presentations/Lyndon_Michael_ZipThwackPing.pdf) · [Medeiros’s pixel-art production account](https://www.patreon.com/posts/explosions-part-7719254) · [Video transcript and worked timing](https://www.linkedin.com/learning/2d-animation-tips-and-tricks/looney-toons-fx-explosion) · [Explosion course breakdown](https://www.vfxapprentice.com/courses/2d-fx-explosion-masterclass) · [Reeves, sections 2.1–2.2](https://graphics.cs.cmu.edu/courses/15-869-F07/Papers/Reeves-1983-PSA.pdf) · [Production article, sequence diagram and accompanying text](https://media.gdcvault.com/GD_Mag_Archives/GDM_February_2000.pdf) · [Mislav’s pixel-art dust/smoke demonstration](https://www.youtube.com/watch?v=itF0TCa_PpI) · [0, .25), [.25, .55), [.55, .80), [.80, 1); remove at 1. In a 400 ms life this gives changes at 0, 100, 220 and 320 ms. | Test two births at 0 and 160 ms. At 240 ms the first tuft is in cel 3 and the second in cel 1. Stop emitting and let the last particle expire at 560 ms. For a baked sheet, draw those same combined states on a common canvas. |

### Diagnose the export

| Symptom in an exported clip | Smallest discriminating check | Repair |
| --- | --- | --- |
| Chest lifts when the lid opens | Overlay the body in authoring coordinates, then overlay the sliced frames at their restored pivots. | Fix the authored body if it moved in both. If only the slice jumps, restore the original offset or use fixed cells. |
| The burst looks like a balloon or a blinking lamp | Replay a solid silhouette, then the interior alone. Watch the leading edge, openings and timing of peak brightness. | Redraw the first outward displacement or breakup pose if the outline expands uniformly. If the outline works, shorten the hot hold or rework interior values. |
| Dust pops, marches in step or leaves a square halo | Compare one strip on light/dark backgrounds, one particle with travel disabled, then a group with staggered births. | Correct an alpha/blend mismatch or dirty edge in the strip, unintended motion inside the cel, or synchronized spawning in the group, according to the first failing pass. |
| Correct source drawings play out of order or never clear | Re-slice the exported file using the consuming engine’s row order and timing. Inspect the last nonempty cel, expiry, and the next trigger. | Restore duration, row selection, hold or removal explicitly. If empty cels or duplicate holds were packed out, preserve their meaning in the runtime clip. |

## Evidence

Unity’s grid importer for particle texture sheets can select one row per particle and sample by lifetime, speed or FPS. An authored decay that must end at death fits a lifetime curve. A fixed authored beat may call for a fixed clock. In Godot 4.5, the particle node needs a CanvasItemMaterial with particle animation enabled and the correct horizontal and vertical frame counts. Configure progression separately. Aseprite can omit empty frames, merge duplicates or add padding; inspect the sheet the consumer actually samples. These are documentation-backed import paths, not results of importing these three exercises in an engine. [Unity Texture Sheet Animation](https://docs.unity3d.com/6000.0/Documentation/Manual/PartSysTexSheetAnimModule.html) · [Godot 2D particle flipbooks](https://docs.godotengine.org/en/4.5/tutorials/2d/particle_systems_2d.html) · [Aseprite export options](https://www.aseprite.org/docs/cli/)
