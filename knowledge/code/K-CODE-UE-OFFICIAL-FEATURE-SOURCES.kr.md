---
id: K-CODE-UE-OFFICIAL-FEATURE-SOURCES
title: 에이전트가 실제로 읽을 수 있는 출처로 언리얼 엔진 공식 기술 목록 만들기
summary: 마케팅용 기능 페이지, 문서 섹션 페이지, 포럼 출시 공지를 함께 쓴다. www.unrealengine.com은 일반 수집을 거부하고 일부 문서 페이지는 빈 껍데기를 돌려주므로, 렌더링되는 브라우저나 읽히는 페이지를 쓴다.
kind: reference
scope: Epic의 공식 언리얼 엔진 기술이나 그 출시 상태를 나열하거나 분류하는 조사
keywords: [Unreal Engine, official features, feature list, release notes, documentation index, unrealengine.com/features, dev.epicgames.com, forums.unrealengine.com, Experimental, Beta, Production-Ready, WebFetch, HTTP 403, JavaScript-rendered page, 언리얼 공식 기술]
status: active
checked_at: "2026-11-20"
context:
  engine: "Unreal Engine 5.8 안정판, 5.9 Preview 문서"
---

## 지침

서로 보완하는 출처 두 가지를 쓰고, 상태는 따로 확인한다.

1. **기능 페이지**(`https://www.unrealengine.com/features`): Epic의 제품 단위 분류(파이프라인 통합, 월드 제작, 캐릭터와 애니메이션, 렌더링, 시뮬레이션 등). 마케팅 표현이지 모듈 목록이 아니다.
2. **문서 섹션 페이지**(`https://dev.epicgames.com/documentation/unreal-engine`과 게임플레이 시스템, 렌더링과 그래픽, 네트워킹, AI, 애니메이션, 오디오, 테스트 같은 최상위 섹션): 시스템 단위 이름과 각 섹션이 연결하는 하위 주제.
3. **출시 상태**: 안정판 버전과 성숙도 표시(Experimental, Beta, Production-Ready)는 검색 결과 요약이 아니라 릴리스 노트나 공식 포럼 출시 공지에서 가져온다. 소스 빌드 엔진이라면 `Engine/Plugins/Experimental` 아래 플러그인 폴더 위치로 한 번 더 확인한다.

에이전트 도구로 관찰한 접근 결과:

- `www.unrealengine.com` 페이지(기능, 뉴스, 제품 페이지)는 일반 수집 도구에 HTTP 403을 돌려줬지만, 렌더링되는 브라우저 창에서는 열렸다. 브라우저에서는 기능 페이지의 분야별 내용을 분야 제목 기준으로 페이지 글에서 뽑을 수 있었다.
- 일부 `dev.epicgames.com` 페이지(5.8 릴리스 노트, 기능 문서 페이지)는 일반 수집에 29자짜리 "Table of Contents" 껍데기만 돌려줬다. 반면 문서 첫 화면, 섹션 페이지, 5.9 릴리스 노트는 본문 전체를 돌려줬다.
- 포럼 출시 공지(`forums.unrealengine.com`)는 본문 전체를 돌려줬다.
- 예전 버전 이름이 들어간 문서 URL이 최신 문서(5.9 제목)를 보여 줬다. 버전은 URL이 아니라 페이지 제목으로 확인한다.

## 적용 범위와 예외

접근 결과는 사이트, 클라이언트, 날짜에 따라 달라지므로 기대기 전에 다시 확인한다. 기능 페이지는 엔진 시스템과 플러그인을 많이 빠뜨리고, 문서 목차는 마케팅 분류를 빠뜨린다. 그래서 어느 하나만으로는 완전한 목록이 아니다. Preview 문서에는 안정판에 없는 기능이 나올 수 있다.

## 확인

- 목록의 항목마다 그 이름이 나오는 Epic 페이지나 공지가 있다.
- 페이지 제목의 버전이 주장하는 버전과 맞다.
- 성숙도 표시는 릴리스 노트, 포럼 공지, 엔진 플러그인 폴더에서 가져왔다.
- 403이나 빈 껍데기가 오면 읽을 수 없다고 보고하기 전에 렌더링되는 브라우저로 다시 시도한다.

## 근거

2026-11-20의 조사 세션 두 건. 한 세션은 기능 페이지와 문서 섹션을 브라우저 창으로 읽었다. 다른 세션은 서브에이전트를 통해 일반 수집을 썼고, `www.unrealengine.com` URL 3개에서 HTTP 403, 5.8 릴리스 노트와 기능 문서 페이지에서 29자 응답, 문서 섹션 페이지 8개와 5.9 릴리스 노트, 포럼 5.8 공지에서 본문 전체를 기록했다. 수집 세션에서는 검색 요약에 나온 성숙도 주장 두 개(Iris, MCP)를 공지 원문에서 찾지 못했다.
