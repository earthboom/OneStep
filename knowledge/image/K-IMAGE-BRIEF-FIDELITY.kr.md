---
id: "K-IMAGE-BRIEF-FIDELITY"
title: "생성·편집한 이미지가 요청의 시각 조건을 충족하는지 확인한다"
summary: "생성에 앞서 구도, 스타일, 문구와 보존 영역을 확인할 기준을 정한다. 관찰된 문제에 맞춰 수정하고 첫 납품본과 최종본을 따로 평가한다."
kind: "method"
scope: "여러 참조 이미지, 정확한 문구, 보호할 영역 등 요청별 조건이 있는 래스터 이미지 생성과 편집"
keywords: ["image generation","brief fidelity","reference roles","image edit","imagegen","Korean type","visual validation","이미지 생성","요구 준수","참조 이미지","부분 수정","한글 타이포"]
status: "active"
checked_at: "2026-11-26"
---

# 생성·편집한 이미지가 요청의 시각 조건을 충족하는지 확인한다

## 지침

하나의 이미지 작업 절차에서 신규 생성, 참조 생성과 편집을 구분하고 같은 imagegen 도구를 사용한다. 브리프에서 눈으로 확인할 필수 조건, 배치·정체성·스타일처럼 각 참조의 역할, 편집 때 보존할 영역을 기록한다. 관찰 가능한 스타일 기준을 더한다. 사진은 시점·조명·재질, 만화는 실루엣과 선·명암의 위계, 초현실적 장면은 의도한 불가능한 관계가 읽히면서 그림자와 공간 단서가 일관적인지 확인한다.

구도나 장면 해석이 어긋나면 다시 생성한다. 국소 문제는 필요한 부분만 수정하고 앞서 통과한 조건을 다시 확인한다. 형식이 허용하면 정확한 문구는 편집 가능한 텍스트로 넣고 철자, 띄어쓰기, 발음 구별 부호와 문장부호를 확인한다. 이미지 크기와 투명도는 파일로 검사한다. 알파 채널이 있어도 배경 픽셀이 실제로 투명한지 확인한다. 크기를 조정했다면 프레이밍과 배치를 다시 확인한다. 확인하지 못한 필수 조건은 미확인으로 기록한다. [Vegabond Image](../../skills/vegabond-image/SKILL.kr.md)

## 적용 범위와 예외

다양한 콘셉트가 필요하면 [창의적 탐색](K-IMAGE-CREATIVE-EXPLORATION.kr.md)을 사용한다. 주관적인 완성도는 조건을 맞춘 결과를 나란히 보여 주고 평가한다. 소규모 조건 충족 비교로 일반적인 미적 선호를 판단하기는 어렵다.

## 확인

제안한 비교는 12개 사례를 고정했다. 한 달 기지 브리프의 스타일 세 종류, 자유 생성, 개수·색상 연결, “달 기지에 오신 것을 환영합니다!” 같은 정확한 한글 포스터, 512 × 512 투명 PNG, 스케치, 두 장면의 동일 인물, 여러 참조 역할, 배경만 수정, 옷 색만 수정이다. 두 절차를 각각 두 번 실행해 48건을 비교한다. 입력·실행 조건·호출 예산을 맞추고 평가자에게 절차를 가린다. 첫 납품본, 최종본과 수정 호출을 따로 센다. 최종 필수 조건의 통과가 늘고 중요 문구나 보존 조건이 퇴행하지 않으며 수정 호출 중앙값이 늘지 않는지 확인한다.

## 근거

OneStep 비교는 네 실행 컨텍스트에서 48건을 기록했다. AI 평가자 한 명이 절차를 가린 후보 54개를 평가했다. 기본·스킬 절차의 첫 납품 통과는 각각 20/24와 22/24, 최종 통과는 23/24와 24/24였다. 수정 호출은 6회와 2회였으며 중앙값은 모두 0이었다. 두 절차 모두 한글 문구와 보존 사례를 통과했다. 스킬 절차는 이미지를 생성한 뒤 포스터 문구를 배치했다. 최종까지 가장 어려웠던 조건은 제품을 정확히 수직으로 내려다보는 구도였다. 모델 빌드와 동일 씨드는 확인할 수 없었다. 케이스마다 새 채팅에서 실행하거나 사람의 선호도를 측정하지 않았다. [케이스](../../output/vegabond-image-comparison/cases.md) · [실행과 결과](../../output/vegabond-image-comparison/results.md) · [집계](../../output/vegabond-image-comparison/metrics.json) · [블라인드 점수](../../output/vegabond-image-comparison/review-scores.json)

GenEval과 T2I-CompBench++는 개수, 속성, 공간 관계를 따로 평가하는 근거다. TIFA는 보이는 조건을 질문으로 검사한다. GIE-Bench는 편집 성공과 보존을 평가한다. PromptCharm과 ControlNet은 단계적 수정과 공간 조건을 준 제작 사례다. 이 자료의 범위는 평가 기준과 참조 역할의 근거까지다.

- 평가 방법 · [GenEval](https://arxiv.org/abs/2310.11513) · [T2I-CompBench++](https://arxiv.org/abs/2307.06350) · [TIFA](https://arxiv.org/abs/2303.11897) · [GIE-Bench](https://arxiv.org/abs/2505.11493)
- 참조와 수정 · [PromptCharm](https://arxiv.org/abs/2403.04014) · [ControlNet](https://arxiv.org/abs/2302.05543) · [GPT Image 프롬프트](https://developers.openai.com/api/docs/guides/image-prompting) · [이미지 생성 한계](https://developers.openai.com/api/docs/guides/image-generation#limitations) · [구도 스케치](https://www.adobe.com/learn/firefly/web/sketch-to-ai-generated-image) · [구도와 스타일 참조 분리](https://www.adobe.com/learn/firefly/web/firefly-boards-to-photoshop-workflow) · [Porto 제작 인터뷰](https://www.creativebloq.com/3d/ai-has-amplified-my-20-years-of-experience-believes-concept-artist-daniel-porto) · [편집 가능한 텍스트 레이어](https://helpx.adobe.com/photoshop/desktop/text-typography/type-layers-creation/type-layers-in-photoshop.html)
- 스타일별 참고 자료 · [Nikon 화각](https://www.nikon.co.uk/en_GB/learn-and-explore/magazine/tips-and-tricks/what-is-focal-length-in-photography-a-guide-for-beginners) · [Animation Mentor 화면 연출](https://www.animationmentor.com/blog/tutorial-use-character-staging-to-guide-viewer-focus/) · [MoMA 초현실주의](https://www.moma.org/collection/terms/surrealism/surrealist-objects-and-assemblage)
