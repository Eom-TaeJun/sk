# SK하이닉스 반도체 전파경로 Codex Final Handoff v1

Codex에 이 폴더 전체를 전달하되,
가장 먼저 `00_MASTER/00_CODEX_MASTER_INSTRUCTION.md`를 읽도록 합니다.

## 핵심 변경

이번 버전에서 필수:
- Hermes Agent 분배/Orchestration
- RAG
- Graph Engineering
- Graph-aware Retrieval
- Harness / State Machine
- Auditor / Human Review

이번 버전에서 제외:
- 전용 LLM 구축
- Fine-tuning
- 전용 Vector DB
- Graph DB
- 대규모 DB 구축

파일/JSON/CSV 기반의 경량 Prototype으로 구현합니다.

## Codex 첫 작업

1. Canonical Sources 읽기
2. source_understanding.md 작성
3. research_validation_gaps.md 작성
4. Repository Tree 제안
5. H1/H2/H3 최소 Dataset 정의
6. New Evidence → Decision Memo 1개 End-to-End 경로부터 구현


## 실행 시작
- Codex에 폴더 전체를 전달
- 첫 입력은 `00_MASTER/04_CODEX_START_PROMPT.txt`
- 구현 전 `docs/implementation_plan.md` 승인
- ChatGPT/Work에서는 `00_MASTER/05_WORK_REVIEW_PROMPT.txt`를 기준으로 결과 리뷰
- 환경/우선순위는 `00_MASTER/06_PROJECT_SETTINGS.md` 참고
