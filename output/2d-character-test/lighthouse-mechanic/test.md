# 등대 정비사 테스트 샘플

OneStep `ca13c55`의 공개된 `vegabond-image` 지침과 내장 imagegen으로 준비한 비교용 샘플이다. 새 전용 기능을 실행한 결과는 아직 없다.

| 산출물 | 확인한 내용 |
| --- | --- |
| 대화 일러스트 (`portrait.png`) | 1254×1254. 실제 생성된 디자인을 스프라이트의 인물 참조로 사용했다. |
| 생성된 스프라이트 원본 (`sprite-source.png`) | 1254×1254 RGBA. 배경에 투명도가 있다. |
| 대기 스프라이트 (`idle-64.png`) | 64×64 RGBA. 알파 경계로 자른 뒤 인물 높이 60px로 축소하고 고정 팔레트로 변환했다. 가시색 15개. 알파값 0 또는 255. |
| 표시 크기 비교 (`size-check.png`) | 밝고 어두운 바탕에서 1배, 최근접 보간으로 4배 확대. 밝은 앞머리와 주황 스카프는 남고 열쇠의 세부 모양은 사라진다. |

## 일러스트 프롬프트

An original character illustration for the dialogue screen of a hand-painted 2D side-scrolling adventure, one adult lighthouse mechanic, square composition, hips-up three-quarter portrait looking screen-right. Short ink-black bob, one large ivory forelock over the near eyebrow, warm medium-brown skin, cropped petrol-blue work jacket with an oversized triangular orange neckerchief, ochre tool belt and one small brass tide-key hanging from it. Alert, amused face, caught listening as she adjusts the orange knot with one hand. Strong grouped silhouettes and economical clean ink shapes, gouache midtones, restrained paper grain, deep blue shadows, warm ivory edge light. Sea-green background with a distant off-white lighthouse and a narrow wedge of golden morning sea. Face and jacket read against the background. Original indie game art, no interface, no text or logo, no frame.

## 스프라이트 프롬프트

Use the supplied character illustration for the person's identity, outfit and palette. Deliver ONE isolated full-body idle player sprite of this same adult lighthouse mechanic, facing right in a side-scrolling 2D adventure. Readable at 64x64 pixels. Bold low-resolution pixel art, deliberately chunky pixel clusters, sparse internal outlines, about 16 colors. The large ivory streak in her dark bob, warm brown skin, triangular orange neckerchief, petrol-blue cropped jacket, mustard utility belt and small brass key remain distinctive. Dark trousers and sturdy brown boots planted in a relaxed staggered stance, hands relaxed. Single idle pose, head to both soles surrounded by empty padding, clean alpha transparency across all the surrounding canvas and between limbs; no shadow, ground, scene or checkerboard. Square canvas.
