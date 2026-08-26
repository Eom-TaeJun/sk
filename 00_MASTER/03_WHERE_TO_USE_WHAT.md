# 어디에서 무엇을 사용할지

## 1. ChatGPT/Work 계열: 설계·판단·리뷰
역할:
- 회사/직무 맥락 이해
- Deep Research 결과 해석
- 가설과 경제학적 구조 검토
- Codex가 만든 결과 리뷰
- 직무기술서용 메시지 추출

업로드 권장:
- 01_CANONICAL_SOURCES 전체
- 00_MASTER/01_RECRUITER_AND_JOB_SIGNAL.md
- 00_MASTER/02_ARCHITECTURE_DECISIONS.md
- 필요 시 Codex가 만든 project_fact_sheet.md / decision_change_log.md

여기서는 코드 구현을 지시하기보다
"이 결과가 SK하이닉스 현업/인사에게 어떤 신호로 읽히는가"를 검토한다.

## 2. Codex: 구현
역할:
- Repository 설계
- Evidence parser
- RAG
- Graph engineering
- Graph-aware retrieval
- Hermes orchestration
- Harness/state machine
- Auditor
- Backtest
- Decision memo generation
- 로그/테스트

Codex에 전달:
- 이 v2 폴더 전체

Codex가 가장 먼저 읽을 파일:
1. 00_MASTER/00_CODEX_MASTER_INSTRUCTION.md
2. 00_MASTER/02_ARCHITECTURE_DECISIONS.md
3. 01_CANONICAL_SOURCES/*
4. 02_SCHEMAS/*
5. 03_TEMPLATES/*

## 3. Deep Research: 자료 수집
역할:
- 원출처 검색
- Historical backtest용 Source 확보
- Signal/병목/계약/전력 정보 보강

Codex에게 직접 웹 조사를 대량으로 시키기보다,
Deep Research 결과를 Canonical Source로 편입한 뒤 구현한다.

## 4. Hermes: Codex가 구현 안에서 사용
Hermes를 별도 연구 환경으로 운영하는 것이 아니라,
Codex가 Agent orchestration layer로 연결한다.

Hermes 역할:
- Demand/Platform sensor
- Memory product sensor
- Supply/Infra sensor
- Commercial/Policy sensor
- Auditor
- Orchestration

주의:
Hermes의 실제 기능/API는 설치 시점 공식 문서에 맞춰 검증한다.
가상의 API를 만들지 않는다.
