# 생성 이미지와 부분 편집 결과가 요청에 맞는지 어떻게 확인할까?

식별자 `K-IMAGE-BRIEF-ACCEPTANCE` · 방법 · 사용 중 · 근거 확인일 2026-11-25

**요약** 필수 수량·속성·위치·문구·편집 범위를 그림에서 답할 수 있는 질문으로 바꾼다. 실제 납품 파일을 확인하고 실패한 조건에 맞게 수정한다.

**적용 범위** 래스터 이미지 생성, 부분 편집, 작업 방식 비교

**검색어** image generation, image editing, attribute binding, composition, preservation, exact text, alpha transparency, 이미지 생성, 부분 편집, 원본 보존, 정확한 한글 문구, 구도, 개체 수

## 활용 방법

필수로 보여야 할 요소와 선호 사항을 가른다. “두 등이 모두 입구에 붙었는가?”, “화면 어느 쪽에 차량이 있는가?”, “배경에도 로봇이 하나 더 있는가?”처럼 묻는다. 왼쪽이 피사체 기준인지 화면 기준인지 명시한다. 장면 속 사건과 표현 매체는 따로 판단한다. 공중에 뜬 건물도 그림자와 원근이 일관되면 사진처럼 보일 수 있다. 사진은 원근·그림자·재질을, 만화는 실제 컷 크기의 실루엣과 시선 순서를, 초현실 장면은 의도한 예외를 알아보게 해 주는 단서를 살핀다. [GenEval](https://arxiv.org/abs/2310.11513) · [T2I-CompBench++](https://arxiv.org/abs/2307.06350) · [TIFA](https://arxiv.org/abs/2303.11897) · [Nikon on field of view and focal length](https://www.nikon.co.uk/en_GB/learn-and-explore/magazine/tips-and-tricks/what-is-focal-length-in-photography-a-guide-for-beginners) · [Animation Mentor staging demonstration](https://www.animationmentor.com/blog/tutorial-use-character-staging-to-guide-viewer-focus/) · [MoMA on Surrealism](https://www.moma.org/collection/terms/surrealism/surrealist-objects-and-assemblage)

참조마다 정체성, 시점·배치, 자세, 화풍 등 맡을 역할을 정한다. 위치가 중요하면 간단한 구도 스케치를 준다. 편집할 때는 바꿀 부위와 보존할 특징을 먼저 정하고 원본과 납품본을 나란히 본다. 표현 방향을 맡긴 요청이라면 의미 있게 다른 후보를 비교할 수 있다. [GIE-Bench](https://arxiv.org/abs/2505.11493) · [PromptCharm](https://arxiv.org/abs/2403.04014) · [ControlNet](https://arxiv.org/abs/2302.05543) · [Composition sketch video and transcript](https://www.adobe.com/learn/firefly/web/sketch-to-ai-generated-image) · [Porto interview](https://www.creativebloq.com/3d/ai-has-amplified-my-20-years-of-experience-believes-concept-artist-daniel-porto) · [Skateboard production video and transcript](https://www.adobe.com/learn/firefly/web/firefly-boards-to-photoshop-workflow)

## 적용 조건과 예외

요청의 복잡도에 맞춰 점검량을 정한다. 마스크, 자세 제어 강도, 시드 고정의 지원 여부는 도구마다 다르다. 논문이 제시하는 것은 평가 항목과 특정 시스템의 사례다. 미적 선호는 별도로 판단한다. [Prompt guide](https://developers.openai.com/api/docs/guides/image-prompting) · [Generation documentation](https://developers.openai.com/api/docs/guides/image-generation#limitations)

## 검증 방법

1. 필수 조건별로 충족·실패·미확인을 기록한다. 글자를 확대해 띄어쓰기, 문장부호와 줄바꿈을 대조하고 파일을 디코딩해 크기·형식·알파를 확인한다. 크기나 구도를 보정한 뒤 대비되는 배경 위에서 투명 영역과 경계를 본다.
2. 시점이나 구도가 어긋나면 카메라 단서나 스케치를 고쳐 다시 생성한다. 부분 결함은 직전 합격 이미지에서 수정하고 주변 특징을 재점검한다. 조판이 가능한 납품물에는 글자 공간을 남겨 정확한 원문을 올린 뒤 결과를 확인한다. 간판처럼 그림 속 표면이라면 원근과 질감도 본다. [Photoshop type layers](https://helpx.adobe.com/photoshop/desktop/text-typography/type-layers-creation/type-layers-in-photoshop.html)
3. 작업 방식 비교에서는 요청·참조·예산·판정 기준을 먼저 고정한다. 검수자에게 방식을 가리고 첫 납품본과 채택한 수정본을 따로 채점한다. 반려한 수정도 횟수에 포함하고 어떤 조건이 실패했는지 남긴다.

## 근거

같은 도구에서 요청 12종을 두 번씩 비교했다. 기존 방식과 검수 지침을 적용한 방식의 첫 납품 합격은 각각 20/24건과 22/24건, 최종 합격은 23/24건과 24/24건이었다. 이후 집중 보완한 방식은 같은 사례의 첫 납품에서 24/24건이 합격했고 수정 호출은 2회에서 5회로 늘었다. 첫 납품에는 계획한 크기 보정과 조판이 포함됐다. 사례 수, AI 검수자, 시드·모델 빌드 미확인 때문에 일반화에는 한계가 있다. [고정 사례](../../output/vegabond-image-comparison/cases.md) · [최초 비교](../../output/vegabond-image-comparison/results.md) · [회귀 시험](../../output/vegabond-image-comparison/full-regression/results.md) · [이미지 제작 지침](../../skills/vegabond-image/SKILL.md)
