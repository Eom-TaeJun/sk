# Verification cleanup — 2026-10-06

기준 baseline: `8d0112353b27de5a1606c259bdb7219e4e11d1c6`. 사용자의 계속 진행 지시에 따라 [이전 코드 검토](../../reviews/2026-10-06/ai_code_review.md)의 네 가지 재현 오류와 최신 자료 검증의 재현성 공백을 정비한다. 목적은 하이닉스 상품·고객·공급 관계를 조사하기 전에 원문과 관측 계약의 무결성을 지키는 것이다.

## 변경과 완료 기준

| 대상 | 구현한 변경 | 요구사항 기반 확인 |
|---|---|---|
| 수집 시각 | SEC acceptance의 실제 달력·시간, retrieval의 명시 UTC ISO datetime을 검사한다. 저장된 record·receipt·ledger·source의 시각과 획득방식도 대조한다. | 불가능한 날짜·시각·비UTC·누락 offset을 거부한다. SEC 시간대 미확인과 issuer 날짜 정밀도는 유지한다. |
| 중간 저장 실패 | 불변 revision을 만든 뒤 ledger를 먼저 확정하고 최신 `record.json`을 게시한다. 재시도는 확정 이력과 원문을 검증한 뒤 최신뷰를 복구한다. UUID 임시파일은 교체 실패 후 정리한다. | ledger/receipt/view/replace 실패 뒤 재시도 가능; 이전 revision bytes와 최초 획득 시각·방식 보존. `verify-only`는 불일치를 읽기 전용으로 거부하며 손상된 원문을 자동 수정하지 않는다. |
| 캐시 | 현재 scenario 원문과 cached `source_trace`에 포함된 과거 원문의 hash를 반환 전에 확인한다. | 현재·이전 원문 변경을 거부하고 기존 승인 result·Evidence bytes를 보존한다. 정상 원문으로 복구하면 같은 과거 결과를 반환한다. |
| H1 테스트 | corpus/Gate6 builder·읽기·원문 검증·replay를 필요한 입력의 임시 복사본으로 옮긴다. 종료 시 원본 입력 hash를 비교한다. | 전체 검사 전후 repository 원문·데이터·capability ledger 169개 파일 bytes 동일. 실제 corpus/승인 데이터의 재작성 없이 기존 검사를 수행한다. |
| 최신 연구 자료 | stdlib 전용 `scripts/validate_current_research.py`를 추가한다. 고정된 2026-10-05 API/목적 JSON 9개, 앞선 입력 6개와 manifest·40개 검토 객체·22 family/23 접근 pointer·문서 분류·후보 상태를 검사한다. | hash·ID·pointer·후보 승격·UTC·분류 변조를 거부한다. 문서 안내 수정은 허용한다. 요약 수는 실제 배열·응답 분류·성공 family에서 재계산한다. |
| 현재 안내 | 예전 상품/고객 수렴·주문서 후속 추적·한국 수출+독일 생산 파일럿 권고를 당시 기록으로 표시한다. | 현재 경제적 조사 순서는 [지표 수집 목적](../../research/supply_chain/indicator_collection_purpose.md)의 KOSIS 측정 계약 하나로 이어진다. |

생산용 corpus builder·원문·날짜별 연구 JSON/manifest와 H1 승인 상태는 변경하지 않는다. 검증기 PASS는 현재 API 접속·경제적 타당성·선행성·사람 승인 결과가 아니다. 기존 실제 issuer capture 한 건은 읽기 전용 재검사한다.

## 실제 검증과 검토

첫 통합 검증은 전체 140개 테스트 PASS, 두 research validator PASS와 실제 issuer capture의 `--verify-only` PASS를 확인했다. 원본 입력 169개의 실행 전후 SHA-256이 같았다. 처음 저장소 밖의 임시 통합 실행 파일은 repository import 경로를 빠뜨려 테스트 discovery가 실패했으며 경로를 보완한 뒤 위 검사를 수행했다. 그 실패 실행도 원본을 변경하지 않았다.

작성 역할은 수집기, 캐시/테스트 격리, 연구 검증기로 나눴다. 다른 담당자가 캐시/격리와 연구 검증기를 검토했고 root는 수집기 diff와 전체 동작을 확인했다. 독립 검토에서는 새 검증기의 두 요약 문서를 함께 99로 바꾸고 hash chain을 갱신하면 실제 성공 응답 11개와 달라도 PASS였다는 반례를 재현했다. 배열·원 family 참조·receipt 획득방식에서 요약을 재계산하고, 양쪽 요약·hash chain 동시 변조와 실패 분류 변조 회귀 3개를 추가해 보완했다. 관련 최신 검증기 회귀 15개와 실제 자료 검증은 PASS다. 역할을 나눈 동일 모델 검토이며 blind review·다른 모델 교차검증·Claude 플러그인 실행의 효과를 측정한 결과로 부르지 않는다.

최종 root 검증은 구현 커밋 `9570b195dbfe2db6766846f893bccef85f0b526b`의 깨끗한 로컬 Git clone에서 수행했다. Git에 포함된 파일만으로 **143 tests, OK**, 두 research validator PASS, 실제 issuer capture 한 건의 읽기 전용 재검사 PASS였다. Clone 자체의 입력 169개 파일은 실행 전후 bytes가 같고 Git 작업 트리도 깨끗했다. 복제 시 일반 CSV 6개에서만 Git 텍스트 줄바꿈 변환이 있었으며 원문·연구 자료처럼 `-text`로 고정한 바이트 대상은 원 checkout과 같았다. 원 checkout 입력 169개도 계속 보존했다.

캐시/격리의 독립 검토는 PASS다. 연구 검증기의 별도 최종 검토도 15개 회귀와 기존 수동 요약 변조 반례를 재실행해 PASS를 확인했다. purpose reviewer는 실제 변경·완료 기록을 읽고 **CONTINUE**로 판단했으며, 새로운 runtime·상시 수집·H1 승인 확대는 **DEFER**했다. Git 커밋·push·main 통합은 기존 사용자 승인 범위이며 실제 SHA/PR은 Git 이력에서 확인한다.

## 재현 명령

repository root, Python standard library:

```powershell
python -m unittest -q
python scripts/validate_supply_chain_research.py
python scripts/validate_current_research.py
python scripts/collect_customer_commitment.py --verify-only
```

제한된 Windows sandbox에서 기본 Temp가 허용되지 않으면 workspace scratch를 지정한다:

```powershell
python -c "from pathlib import Path; import tempfile, unittest; p=Path('work/test-temp'); p.mkdir(parents=True, exist_ok=True); tempfile.tempdir=str(p.resolve()); r=unittest.TextTestRunner().run(unittest.defaultTestLoader.discover('tests')); raise SystemExit(not r.wasSuccessful())"
```

이 작업은 새로운 원문/API 호출·계정·키 발급·runtime·상시 수집·대시보드를 추가하지 않는다. H1/Gate 6 데이터 동결·실증 결과도 만들지 않는다.

**다음 작업 하나:** 한국 반도체 산업의 KOSIS 생산/출하/재고 exact 표·항목·KSIC·기준년·단위·조정을 무료 metadata/문서에서 먼저 확인하고, 관세청/Comtrade의 HS 교역과 비교 가능한 범위·불가능한 연결을 고정한다. 본 수집은 측정 계약 확정 뒤 진행한다.
