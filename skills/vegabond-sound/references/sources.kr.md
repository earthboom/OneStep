# 오디오 제작 근거 자료

2026-11-24 조사. 논문은 연구 조건 안에서 해석하고 현업 사례에서는 시도해 볼 제작 방법을 뽑는다. 표준과 매뉴얼은 명시된 범위에 적용한다. 이 스킬의 절차는 그런 관찰을 현재 자산의 검증으로 옮긴다. 서비스 기능, 라이선스, 출력 옵션에 의존할 때는 최신 공식 자료를 확인한다.

## 효과음

| 출처 | 적용과 확인 |
| --- | --- |
| [van den Doel·Kry·Pai, FoleyAutomatic, SIGGRAPH 2001](https://persianney.com/kvdoelcsubc/publications/foleyautomatic.pdf) | 충격, 미끄러짐, 구름 등의 접촉 기반 합성 연구. 여기와 공명을 따로 설계해 보고 현재 동작에서 의도한 재질과 운동이 들리는지 확인한다. |
| [Perry Cook, Princeton Sound Lab 물리 모델링](https://soundlab.cs.princeton.edu/research/phymod/) | 물리 기반 타악기, 모달 합성, 확률적 이벤트에 대한 저자 자료와 논문. 타격의 공명과 딸랑거림의 다중 충돌처럼 사건에 맞는 모델을 고른다. |
| [Andy Farnell, Designing Sound, MIT Press](https://mitpress.mit.edu/9780262288835/designing-sound/) | 절차적 사운드 설계에 관한 출판사 소개. 어떤 이벤트 변수가 소리를 바꿔야 하는지부터 생각해 볼 수 있다. 공개 소개는 책의 범위를 설명한다. |
| [Lawlor·Neumann, Overwatch: Play by Sound, GDC 2016](https://www.gdcvault.com/play/1023010/Overwatch-The-Elusive-Goal-Play) | 플레이어의 판단에 연결된 음향 설계 목표를 다룬 개발자 발표. 다른 소리와 경쟁할 때도 현재 큐를 알아듣는지 확인한다. |
| [Blizzard, Overwatch 2 사운드 디자이너 인터뷰](https://overwatch.blizzard.com/en-gb/news/24226699/talent-tree-sound-designer-overwatch-2/) | 캐릭터의 역할과 판타지에서 출발해 폴리 재료를 탐색한 현업 사례. 레이어를 고르기 전에 이벤트의 정체성을 정한다. |
| [Kevin Regamey, The TUNIC Audio Talk, GDC 2023](https://www.youtube.com/watch?v=sCIK78OHrIY) | 발표 소개에서 초기 크리에이티브 방향, 게임에서 출발한 음향 결정, 효과음 설계와 구현을 확인할 수 있다. 세부 제작 결정을 더 조사할 때 출발점으로 쓴다. |

## 배경음악과 적응형 음악

| 출처 | 적용과 확인 |
| --- | --- |
| [Elizabeth Medina-Gray, 비디오 게임 음악의 모듈 이음새 분석, 2019](https://www.mtosmt.org/issues/mto.19.25.3/mto.19.25.3.medina.gray.html) | 순차 모듈과 동시 모듈의 관계를 분석한다. 박절, 음색, 음높이, 크기, 급격한 변화를 비교하고 의도적 단절도 기능에 따라 평가한다. |
| [Austin Wintory, From JOURNEY to ERICA](https://awintory.medium.com/from-journey-to-erica-214355002896) | 인터랙티브 음악에 대한 작곡가의 경험. 어떤 순간에 고정된 진행이 필요한지, 어디서 플레이어 상태에 반응할지를 판단하는 사례다. |
| [Audiokinetic, Wwise Project Adventure](https://www.audiokinetic.com/download/documents/WwiseProjectAdventure_en.pdf) | 음악 세그먼트, 출발·도착 전환 규칙, 선택적 연결 구간에 관한 공식 튜토리얼. 설치한 버전에서 큐와 전환 규칙을 확인한다. |
| [FMOD Studio 2.04, Authoring Events](https://www.fmod.com/docs/2.04/studio/authoring-events.html) | 타임라인 영역, 조건, 퀀타이즈에 관한 공식 설명. 실제 이벤트와 재생 경로의 타이밍을 점검한다. |
| [Epic Quartz 개요](https://dev.epicgames.com/documentation/unreal-engine/overview-of-quartz-in-unreal-engine?lang=en-US) 및 [MetaSounds 개요](https://dev.epicgames.com/documentation/en-us/unreal-engine/metasounds-the-next-generation-sound-sources-in-unreal-engine) | 각각 재생 예약과 샘플 단위 소스 그래프 기능을 설명한다. 필요한 추가·제거·페이드·취소 동작을 직접 시험한다. |
| [Unity, AudioSource.PlayScheduled](https://docs.unity3d.com/ScriptReference/AudioSource.PlayScheduled.html) | DSP 시간을 쓰는 공식 API. 준비 시간을 주고 사용처에 임포트한 뒤 실제 출력을 확인한다. |

## 말소리

| 출처 | 적용과 확인 |
| --- | --- |
| [Shure, 녹음 마이크 기법](https://content-files.shure.com/Pubs/microphone-techniques-for-studio-recording/microphonetechniques-recording-guide.pdf) | 제조사의 녹음 가이드. 테스트 대사에서 거리, 방향, 파열음, 근접 효과를 비교한다. |
| [Audacity, Noise Reduction](https://manual.audacityteam.org/man/noise_reduction.html) | 노이즈 프로파일과 아티팩트에 관한 공식 문서. 지속적인 잡음이라면 잡음만 있는 대표 구간을 고르고 제거되는 소리를 들어본다. |
| [iZotope, 플러그인과 단독 RX 에디터](https://www.izotope.com/community/blog/rx-as-a-plugin-vs-as-a-standalone-audio-editor) | 맥락에 따라 편집 방식을 달리하는 사례. 전체를 처리하기 전에 최종 배경에서 클릭이나 잔여 잡음이 들리는지 판단한다. |
| [Jean-Marc Valin, 실시간 전대역 음성 개선 연구, 2018](https://arxiv.org/abs/1709.08243) | 임계대역 게인 추정과 피치 필터를 조합한 RNNoise 연구. 실제 녹음에서 아티팩트와 명료도를 확인한다. |
| [W3C, SSML 1.1](https://www.w3.org/TR/speech-synthesis11/) | 발음, 쉼, 운율을 위한 마크업 표준. 사용할 수 있는 제어 옵션과 합성 결과는 TTS 제공자에 따라 확인한다. |

## 작곡 그루브 편곡

| 출처 | 적용과 확인 |
| --- | --- |
| [송화숙, 「이 죽일 놈의 사랑」 발라드의 성정치학, 2017](https://journal.kci.go.kr/musicology/archive/articleView?artiId=ART002245331) | 한국 발라드의 역사와 극적 고조를 다룬 연구. 현재 곡에서 가사, 선율 윤곽, 화성, 감정 절정의 위치를 탐색한다. 관찰 범위는 연구된 시대와 곡에 따른다. |
| [김성현, K-pop 발라드의 절정음과 마무리음 연구, 2025](https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART003264097) | 2015~2024년의 지상파 차트 1위 발라드 표본을 분석했다. 보컬의 최고조와 끝맺음 관계를 비교하는 데 쓰며 해석은 표본에 한정한다. |
| [Witek 외, 당김음·움직임·그루브의 즐거움, 2014](https://doi.org/10.1371/journal.pone.0094446) | 펑크 드럼 브레이크 청취 실험에서 중간 정도의 당김음이 높은 평가를 받았다. 알앤비나 랩의 고정 설정으로 삼지 않고 리듬 밀도를 비교하는 출발점으로 쓴다. |
| [Questlove의 강연과 시연, 2013](https://www.redbullmusicacademy.com/lectures/questlove-new-york-2013/) 및 [D’Angelo와의 대화, 2014](https://www.redbullmusicacademy.com/lectures/dangelo/) | 그루브와 세션 협업에 대한 당사자 사례. 감지할 수 있는 박의 기준을 두고 파트 사이의 타이밍 관계를 비교한다. |
| [Ben Duinker, 힙합의 프레이징과 박절, 2021](https://doi.org/10.1093/mts/mtab003) 및 [힙합 플로우의 표현적 타이밍, 2022](https://online.ucpress.edu/jpms/article-abstract/34/1/90/120447/Functions-of-Expressive-Timing-in-Hip-Hop-Flow) | 비트와 랩의 프레이징, 박절, 타이밍에 대한 연구. 보컬의 구절과 강세를 표시한 뒤 일치와 어긋남의 효과를 비교한다. |
| [Dennis DeSantis, Making Music](https://cdn-resources.ableton.com/resources/uploads/makingmusic/MakingMusic_DennisDeSantis.pdf) 및 [Ableton Live 12, Using Grooves](https://www.ableton.com/en/live-manual/12/using-grooves/) | 프로덕션 전략과 도구의 그루브 기능. 편곡에서 요소를 빼서 비교하고 선택한 파트의 타이밍과 벨로시티를 조절한다. |

## 측정과 납품

| 출처 | 적용과 확인 |
| --- | --- |
| [ITU-R BS.1770-5](https://www.itu.int/rec/R-REC-BS.1770-5-202311-I) | 오디오 프로그램 라우드니스와 트루 피크 측정 알고리즘. 납품 목표값은 실제 규격에서 가져온다. |
| [EBU R 128](https://tech.ebu.ch/publications/r128) 및 [EBU Tech 3285](https://tech.ebu.ch/publications/tech3285) | 방송 라우드니스 권고와 BWF 메타데이터 규격. 납품에 해당하는지와 도구가 필요한 필드를 보존하는지 확인한다. |
| [Spotify for Artists, 라우드니스 정규화](https://support.spotify.com/us/artists/article/loudness-normalization/) | 서비스별 정규화 동작과 납품 안내. 스트리밍 미리듣기 조건을 의도한 마스터 및 사용처와 비교한다. |
| [FFmpeg 필터](https://ffmpeg.org/ffmpeg-filters.html#ebur128)와 [ffprobe](https://ffmpeg.org/ffprobe.html) | 측정과 검사에 관한 공식 자료. 실제 납품물을 검사하고 목적에 따라 수치를 해석한다. |

## 도구와 권리

| 출처 | 적용과 확인 |
| --- | --- |
| [Kreuk 외, AudioGen, ICLR 2023](https://arxiv.org/abs/2209.15352) 및 [Copet 외, MusicGen, NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/94b472a1842cd7c56dcb125fb2765fbd-Abstract-Conference.html) | 텍스트 유도 오디오와 제어 가능한 음악 생성 연구. 렌더의 사건 순서, 곡 구조, 타이밍과 내용 충실도를 검사한다. 해당 프로젝트는 [AudioCraft 가중치 라이선스](https://github.com/facebookresearch/audiocraft/blob/main/LICENSE_weights)를 확인하고 실제 체크포인트에 맞는 조건을 살핀다. |
| [ElevenLabs, 효과음 생성](https://elevenlabs.io/docs/api-reference/text-to-sound-effects/convert) | 시간, 포맷, 루프 제어의 공식 예시. 버전별 지원 여부를 확인하고 생성 파일과 루프를 직접 검사한다. |
| [Suno, 유료 구독 권리](https://help.suno.com/en/articles/9601665) | 상업적 사용 조건에 관한 제공자 문서. 납품에 해당하는 플랜, 생성·다운로드 등 관련 날짜, 현재 약관을 확인한다. |
| [Freesound FAQ](https://freesound.org/help/faq/) 및 [미국 저작권청, 녹음물](https://www.copyright.gov/register/sr-definition.html) | 개별 소리 라이선스 안내와 작곡·녹음을 구분하는 미국 공식 자료. 사용할 자산과 용도, 해당 관할에 맞춰 확인한다. |
