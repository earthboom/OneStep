---
id: K-CODE-AGENT-INSTRUCTION-AUDIT
title: 에이전트가 프로젝트 지침을 따랐는지 세션 대화 기록으로 확인하기
summary: 지침을 지켰는지는 에이전트의 보고나 할 일 목록 상태가 아니라, 대화 기록에 남은 지침 로드 항목, 도구 호출 입력, 시각이 찍힌 글로 판단한다. 필요한 출력 없이 단계만 완료로 표시될 수 있다.
kind: method
scope: JSONL 대화 기록을 남기는 Claude Code CLI와 데스크톱 세션. 필수 단계가 도구 호출이나 보이는 글을 남기는 모든 에이전트 설정
keywords: [Claude Code, agent instructions, instruction compliance, session transcript, JSONL, instructions attachment, tool_use, CLAUDE.md, CLAUDE.local.md, subagents, task list, self-report, audit, retest, 지침 적용 확인]
status: active
checked_at: "2026-11-20"
context:
  tool: Claude Code 데스크톱 앱과 CLI, 2026-11 기준 대화 기록 형식
---

## 지침

세션들이 어떤 지침(시작 절차, 필수 읽기, 검색, 보고 항목)을 적용했는지 확인하려면 대화 기록을 직접 읽는다.

1. **기록 찾기.** Claude Code는 대화마다 JSONL 파일 하나를 `~/.claude/projects/<인코딩된 작업 경로>/<session-uuid>.jsonl`에 쓰고, 서브에이전트 기록은 `<session-uuid>/subagents/` 아래에 둔다. 데스크톱 세션 ID(`local_...`)는 파일 이름과 다르므로 `cwd`, 첫 사용자 메시지, 시각으로 짝을 맞춘다. 되감거나 갈라진 대화는 앞부분 메시지를 반복하는 두 번째 파일을 만들 수 있다.
2. **지침이 로드됐는지 확인.** `type: attachment`이고 `attachment.type: instructions`인 항목이 문맥에 들어간 지침 파일을 나열한다. 에이전트에게 묻지 않고도 "자동으로 불러왔는가"를 답할 수 있다.
3. **필수 단계마다 관찰 가능한 근거를 대응.** 필수 읽기는 입력에 그 파일이 들어간 `tool_use`, 필수 검색은 질의가 들어간 명령 입력, 필수 진술은 assistant `text` 블록이다. 주 대화를 판단할 때는 `isSidechain` 항목을 뺀다.
4. **시각으로 순서 확인.** "실행 전에 X를 말한다" 같은 요구는 X가 어딘가에 있는지가 아니라, 그 글이 절차 파일 외의 첫 도구 호출보다 앞서는지로 판단한다.
5. **자기 보고는 주장으로 취급.** 에이전트의 요약, 마무리 글, 할 일 목록 상태는 단계가 실행됐다는 근거가 아니다.

## 적용 범위와 예외

하네스가 대화 기록을 온전히 남길 때 적용된다. 필드 이름과 경로는 한 도구 버전에서 관찰한 동작이라 바뀔 수 있으니, 스크립트를 쓰기 전에 표본 줄을 다시 확인한다. 기록은 에이전트가 무엇을 했는지 보여 줄 뿐 이유는 보여 주지 않는다. 빠진 단계를 진단하려면 요청 문구와 지침 문장이 필요하다. 다른 세션에서 시작한 통제 재시험은 요청 앞에 맥락을 덧붙일 수 있고, 헤드리스 실행은 인증 만료로 실패할 수 있다. 그래서 재시험은 사용자가 직접 입력한 요청과 비슷할 뿐 같지는 않다.

## 확인

- 점검한 세션마다 `instructions` 항목에 기대한 파일이 있다.
- 필수 단계마다 맞는 `tool_use` 입력이나 `text` 블록과 그 시각이 있다.
- 순서 규칙은 조건에 맞는 첫 글이 절차 파일 외의 첫 도구 호출보다 앞선다.
- 단계를 했다고 표시한 할 일 목록 항목은 세기 전에 대화 기록과 대조한다.

## 근거

2026-11-20 한 게임 프로젝트 체크아웃의 대화 6건과, 데스크톱 앱에서 시작한 통제 재시험 2건을 점검했다. 설정 이후 모든 세션에서 `instructions` 항목이 로컬 지침 파일의 자동 로드를 확인해 주었다. 한 재시험에서는 할 일 목록에 "post work brief" 단계가 완료로 표시됐지만, 이어지는 도구 호출 전에 그런 글은 대화 기록에 없었다. 관련 사건: [R-CODE-AGENT-BRIEF-ORDER](../../records/code/R-CODE-AGENT-BRIEF-ORDER.md).
