---
id: K-CODE-UE-LOC-MERGE
title: 충돌한 Unreal 로컬라이즈 manifest/archive 를 의미 단위로 병합하고 parity 증명 후 locres 재컴파일하기
summary: Game.manifest 와 각 Game.archive 를 (네임스페이스 경로, 키) 항목으로 평탄화해 3-way 병합하고, 유지하는 쪽의 포맷 그대로 기록한 뒤, 같은 엔진이 유지하는 쪽의 커밋 locres 를 바이트 단위로 재현한다는 것을 먼저 증명하고 나서 GatherText 커맨드릿으로 Game.locres 를 재컴파일한다.
kind: method
scope: 장수 브랜치 간 git 머지에서 Content/Localization/<target>/ 의 manifest, archive, locres 가 충돌하는 Unreal Engine 프로젝트
keywords: [Unreal Engine, localization, Game.manifest, Game.archive, Game.locres, Game.po, GatherText, GenerateTextLocalizationResource, Game_Compile.ini, UTF-16LE, three-way merge, semantic merge, locres parity]
status: active
checked_at: "2026-11-06"
context:
  engine: UE 5.3 프로젝트 데이터를 5.8 소스 빌드로 컴파일
  platform: Windows desktop
  format: manifest/archive 는 UTF-16LE BOM JSON, 탭 들여쓰기, LF
---

## Guidance

1. 충돌한 manifest/archive 의 3단계를 `git show <base>:<path>`, `git show <ours>:<path>`, `git show <theirs>:<path>` 로 스크래치에 추출한다. 텍스트로 해소하지 않는다. 큰 JSON 트리라 git 의 줄 단위 병합은 네임스페이스를 중복시키거나 깨뜨린다.
2. 2바이트 BOM 뒤를 UTF-16LE JSON 으로 파싱한다. (중첩 `Namespace` 값의 튜플, `Key`) 를 키로 평탄화한다. manifest 는 `Source` 객체와 키의 나머지 필드, archive 는 `Key` 를 뺀 자식 항목이 값이다.
3. 맵을 3-way 병합한다. 양쪽 동일이면 유지, 한쪽만 바뀌었으면 그쪽 채택(추가/수정/삭제), 양쪽이 다르게 바꿨으면 사람 결정 목록에 올리고 임시로 ours 유지.
4. 병합 맵을 유지하는 쪽 트리의 깊은 복사본에 델타로 적용한다. 새 항목은 트리가 이미 쓰는 순서(자식이 소스 텍스트순인지, 키가 키순인지 먼저 감지)로 삽입하고, 빈 `Children`/`Subnamespaces` 배열은 제거한다. 결과를 다시 평탄화해 병합 맵과 같은지 단언한다.
5. 유지하는 쪽 포맷으로 직렬화한다: BOM, `json.dumps(ensure_ascii=False, indent='\t')`, LF, 유지하는 쪽에 끝 개행이 있으면 끝 개행. 직렬화기는 먼저 증명한다: 각 입력을 파싱 후 재직렬화해 바이트 비교. 끝 개행만 없는 쪽은 병합해도 안전하다.
6. 한쪽을 고르지 말고 모든 `Game.locres` 를 재컴파일한다. 더미 프로젝트(최소 `.uproject`, 프로젝트의 `Config/Localization/<target>_Compile.ini`, 병합된 manifest/archive 를 담은 `Content/Localization/<target>/`)를 만들고 `UnrealEditor-Cmd.exe <dummy>.uproject -run=GatherText -config=Config/Localization/<target>_Compile.ini -unattended -nullrhi -nosplash -NoShaderCompile` 를 실행한다.
7. 결과를 믿기 전에 parity 를 증명한다: 유지하는 쪽의 커밋된 manifest/archive 를 먼저 컴파일해 모든 문화권에서 커밋 locres 와 바이트 일치를 요구한다. 그 다음에 병합 입력을 컴파일해 스테이징한다.
8. `Game.po` 는 원본이 아니라 파생 export 다. archive 보다 많이 뒤처질 수 있고 git 은 텍스트로 병합한다. 병합 archive 와 비교하는 목적은 병합 실수 탐지이지 번역 결정이 아니다.

## Applicability and exceptions

양쪽 브랜치가 같은 로컬라이즈 타겟을 건드렸고 archive 가 JSON(UE 기본)일 때 적용한다. 여기서는 더 높은 마이너 버전 엔진이 locres 를 동일하게 컴파일했지만, 엔진 빌드와 프로젝트마다 parity 단계로 다시 증명해야 한다. 더미 프로젝트의 엔진에서 로드 실패하는 플러그인(여기서는 셰이더 모듈이 없는 소스 빌드의 `NNEDenoiser`)은 `.uproject` `Plugins` 배열에서 꺼야 하며, 안 끄면 커맨드릿이 컴파일 전에 종료한다. 프로젝트 커스텀 엔진이 있으면 그걸 우선 쓴다. 양쪽이 같은 키를 다르게 바꾼 항목은 이 방법이 다루지 않으며 사람 결정으로 남긴다.

## Checks

- 라운드트립: 유지하는 쪽에서 `serialize(parse(file)) == file`. 다른 쪽의 차이는 보고하고 끝 개행뿐인지 확인.
- 항목 수: 병합 항목 == 유지 쪽 항목 + 상대 추가 - 삭제, manifest 와 모든 문화권 archive 에서 동일.
- parity: 유지 쪽 커밋 입력의 컴파일 locres == 커밋 locres (모든 문화권), 병합 컴파일 전에.
- 내용: 병합 locres 를 파싱하거나 바이트 검색해 상대가 추가한 모든 키와 유지 쪽이 머지 베이스 이후 추가한 모든 키가 있는지 확인. locres 안의 ASCII 키/번역은 1바이트 ANSI 로 저장되므로 ASCII 바이트로, 비ASCII 는 UTF-16LE 로 검색.
- `.po` 교차 검사: 3단계 모두에서 archive 에 없고 `.po` 에만 있는 항목은 기존 staleness 이지 병합 손실이 아니다.

## Evidence

2026-11-06 UE 5.3 게임 프로젝트의 hotfix -> main 머지에서 관찰: manifest 1개와 문화권 archive 10개 충돌; 평탄화 결과 base 14364 / ours 14557 / theirs 14378 항목; 상대가 14키 추가, manifest 항목 최대 875개(소스 메타데이터)와 문화권당 4~37 번역 수정; 양쪽 충돌 0. 커밋 locres 는 플러그인 하나를 끈 뒤 5.8 소스 빌드 `UnrealEditor-Cmd.exe` 와 더미 프로젝트로 바이트 단위 재현됐고, 병합 locres 에는 추가 14키와 유지 쪽이 추가한 193키가 모두 있었다. `.po` 는 모든 단계에서 archive 보다 1245 항목 뒤처져 있었다. 출처 프로젝트: 스튜디오 UE5 게임(경로와 키 생략).

미검증: 해당 5.8 빌드 외의 엔진, 비JSON 레거시 archive, 양쪽이 같은 키를 바꾼 머지.
