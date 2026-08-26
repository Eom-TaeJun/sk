# Before / After

| 항목 | Before | After | 실제 측정 근거 |
|---|---|---|---|
| Source traceability | Canonical 문서의 출처명·날짜 중심 | Memo fact별 Evidence ID→Source ID→excerpt→locator→URL/hash | `RUN-HBM4-VS-001/decision_memo.json`; fact 4건 모두 trace 검증 |
| 반복분석 시간 | 측정하지 않음 | 측정하지 않음 | 시간 절감 수치 미기록 |
| Evidence classification | 문서 단위 FACT/CLAIM 표시 | 문서 1건을 A_DIRECT_FACT 2건, B_COMPANY_CLAIM 2건으로 분리 | `atomic_evidence.jsonl` 4 records |
| Contradiction preservation | 대표 충돌을 설계문서에 서술 | semantic boundary 3건을 OPEN·auto_resolved=false로 보존 | `contradictions.jsonl` 3 records |
| 재분석 일관성 | 실행 경로 없음 | 동일 scenario 재실행 결과의 state, graph diff, source trace, trace hash 일치 | deterministic replay test 통과 |
| 판단 업데이트 가능성 | 변경 전후 log 없음 | 자동 PROMOTED→HUMAN_REVIEW 보류, path→subgraph 표현 수정 | `decision_change_log.md`; transition log |

실제로 측정하지 않은 성능, 정확도, 시간 절감 수치는 기록하지 않았다.
