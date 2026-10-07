# 작업 설정 안내

이 파일은 소프트웨어가 읽는 설정 파일이 아니라 작업 안내다. 실제 작업 규칙은 [AGENTS.md](../AGENTS.md), 지표 수집 범위는 [지표 목적](../docs/research/supply_chain/indicator_collection_purpose.md)을 따른다.

작업마다 필요한 파일을 선택한다. 원자료·승인 계약·출처 검증은 유지하고, 특정 runtime이나 논리 역할의 수를 구현 목표로 삼지 않는다. 새 폴더·설정·의존성은 실제 소비처가 있을 때 추가한다.

보존된 구조와 설계는 [참조 안내](../docs/reference_index.md)에서 찾는다. 코드 정리 방법과 실제 사용처 점검은 [구조 필요성 검토](../docs/reviews/2026-10-07/structure_cleanup.md)를 참조한다.

2026-10-07에 전체 Master/schema를 고우선순위로 로드하던 목록과 제거된 adapter·미구현 eval 디렉터리를 노출하던 구조 목록을 없앴다. 초기 eval 안내에는 승인 후 생성 조건이 있었다. 초기 안내는 Git 이력에 보존한다.
