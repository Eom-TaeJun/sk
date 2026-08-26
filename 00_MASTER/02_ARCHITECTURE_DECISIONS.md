# Architecture Decisions

## 유지
- Hermes agent orchestration
- RAG
- Graph engineering
- Graph-aware retrieval
- deterministic harness
- auditor/human review

## 제외
- dedicated LLM
- fine-tuning
- dedicated vector DB
- graph DB
- enterprise DB build

## 이유

RAG:
최신성과 Source Trace가 핵심이므로 필요.

Graph:
Customer → Platform → Product → Bottleneck → Decision 경로가 핵심이므로 필요.

Hermes:
여러 섹터의 변화를 별도 Sensor로 분배하고, 결과를 하나의 Harness로 통합하기 위해 필요.
단 현재 버전의 실제 API/Tool capability는 구현 시 공식 문서로 검증.

Harness:
LLM이 매번 다른 기준으로 분석하지 않게 하는 핵심 통제장치.

Auditor:
FACT / CLAIM / ESTIMATE / INFERENCE 혼동과 과잉추론 방지.

DB 제외:
이번 프로젝트는 운영형 서비스가 아니라 채용 경험 증명용 Prototype.
파일 기반 구조로도 문제정의·구조화·검증 역량을 충분히 보여줄 수 있음.
