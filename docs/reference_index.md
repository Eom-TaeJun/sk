# 과거 구현과 설계 참조

현재 작업은 [지표 수집 목적](research/supply_chain/indicator_collection_purpose.md)을 따른다. 이 안내는 보존된 구현·승인 계약·과거 조사와 미래 설계를 필요할 때 찾기 위한 참조다. 아래 자료의 과거 다음 단계 문구를 현재 실행 지시로 사용하지 않는다.

## 구현과 승인 상태

| 영역 | 보존 상태와 참조 |
| --- | --- |
| Evidence 처리와 시간 갱신 | Vertical Slice·2025→2026 Temporal Update 구현. [당시 구현 계획](implementation_plan.md), [작업 검토](work_review_vertical_slice.md), [출처 해석](source_understanding.md), [한계](research_validation_gaps.md) |
| H1 측정 설계 | Gates 1–5 사람 승인·동결. [승인 계약](exec-plans/active/h1_empirical_validation_design.md), [승인 전 타당성 기록](exec-plans/active/h1_feasibility_manifest.md) |
| H1 자료 준비 | 24-Track·4-Track pilot와 full corpus/Gate 6 검토 패키지 준비. [corpus 수집 기록](exec-plans/completed/h1_full_corpus_collection.md), [Gate 6 readiness](reviews/h1_gate6_corpus_readiness.md), [수집 runbook](runbooks/h1_primary_source_collection.md) |
| H1 대기 경계 | 사람 Gate 6 동결 대기. 지표·lead/lag·실현율·결과 분석·verdict는 미승인·미계산. 제품 상용화와 고객/플랫폼 실현 층은 pooling하지 않음 |
| 중단 실험 | 현재 baseline에서 제거되어 [완료 기록](exec-plans/completed/interrupted_h1_experiment.md)과 Git 이력에만 보존. H1 finding으로 사용하지 않음 |
| 수집·검증 정비 | [고객 약정 단일 실험](exec-plans/completed/customer_commitment_collection_20261003.md), [AI 코드 검토](reviews/2026-10-06/ai_code_review.md), [오류 수정·검증](exec-plans/completed/verification_cleanup_20261006.md), [구조 필요성 검토](reviews/2026-10-07/structure_cleanup.md) |

## 경제적 계약과 미래 설계

| 확인할 내용 | 참조와 실행 경계 |
| --- | --- |
| 프로젝트의 경제적 원칙 | [Master Instruction](../00_MASTER/00_CODEX_MASTER_INSTRUCTION.md) |
| 결정과 설계 변경 이력 | [Architecture Decisions](../00_MASTER/02_ARCHITECTURE_DECISIONS.md) |
| 전체 분석 영역과 모듈 admission | [Decision Architecture](decision_architecture.md). 보존된 설계이며 모든 영역을 동시에 구현·수집하는 목록이 아님 |
| 모델·프로그램·runtime 역할 | [역할 배분](../00_MASTER/03_WHERE_TO_USE_WHAT.md), [Agent Architecture](agent_architecture.md). 특정 runtime·멀티에이전트 수를 목표로 삼지 않음 |
| 미래 확장 | H2는 신뢰할 수 있는 H1 최소 검증 이후, H3는 자료가 충분할 때까지 `KNOWN_UNKNOWN`. Decision Engine·Agent Execution Harness·runtime·dashboard·DB는 현재 구현 범위에서 제외 |

실제 계약·상태 전이와 검증은 `src/`, `02_SCHEMAS/`, `tests/`에 있다. 실제 수행 사실은 `application_evidence/`에 보존한다. 학습·설계·합성 시험을 예측력·사업 성과로 표현하지 않는다. 원본 ZIP baseline과 SHA-256 manifest는 `data/raw/baseline/`에 유지하며 v1/v2 표기 차이는 한계 문서를 참조한다.

## 공급망 조사 이력

상품·산업 문서와 날짜별 연구 후보는 [공급망 자료 안내](research/supply_chain/README.md)에서 찾는다. 2026-10-03의 32개 후보/14개 로드맵, 2026-10-04의 18개 측정 후보, 2026-10-05의 34개 번호 지표/6개 가족 계약은 서로 다른 날짜·목적의 묶음이다. 수를 합치거나 과거 우선순위를 현재 실행 목록으로 사용하지 않는다.

독립 목적 검토와 수정 기록의 소유자는 [research_convergence_review.md](research/supply_chain/research_convergence_review.md)다. 검증 명령·작업자 불변조건은 [AGENTS.md](../AGENTS.md)를 따른다. 현재 단계·세부 진행 이력을 새 안내 문서마다 복제하지 않는다.
