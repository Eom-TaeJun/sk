# AI 코드 검토 방법과 현재 저장소 점검

기준일: **2026-10-06**. 검토 대상: `c3ae9996bd51452cedfb4b7ac3186c61dbb31b39`.

**연구 방향은 유지하고 검증 절차는 보완해야 한다.** 하이닉스의 상품·고객·구매·공급 관계를 먼저 정의하고 공개 자료의 한계를 보존하는 방향은 목적에 맞는다. 그러나 기존 115개 테스트가 통과해도 날짜 오류, 중간 저장 실패, 캐시의 원문 재검사 누락과 테스트의 실제 자료 재작성은 남아 있다. 새로운 수집기나 관리 runtime을 늘리기 전에 이 경계를 정비하는 편이 낫다.

이번 변경은 검토 결과와 [오프라인 재현 파일](reproduce_findings.py)을 보존한다. 운영 코드·기존 연구 데이터·H1 승인 상태는 수정하지 않는다. 원문 해시 검증, 코드 동작 검증, 자료의 경제적 의미, 사람 승인과 예측 성능은 각각 별도 판단이다.

## 참고할 검토 방법

공식 문서·실제 공개 프롬프트가 기술 동작의 근거다. Reddit은 개발자의 경험과 문제 제기이며 효과를 증명하는 비교 실험은 아니다. 아래 적용 열은 이 저장소에 대한 판단이다. 공개 프롬프트와 설치 가능한 플러그인이 있다는 사실은 모델 실행까지 무료라는 뜻이 아니다.

| 자료 | 확인한 방식 | 이 저장소에 적용할 부분 |
|---|---|---|
| [Claude Code best practices](https://code.claude.com/docs/en/best-practices) | 작성과 검토를 다른 컨텍스트에서 수행하고 실행 가능한 검증 결과를 제시한다. 억지로 문제를 찾게 하면 불필요한 복잡성이 늘 수 있다. | 목적·diff·불변조건·완료 기준을 검토자에게 주고, 실제 오류나 유지보수 비용을 만드는 부분만 보고한다. |
| [공식 code-review 플러그인](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-review/commands/code-review.md) | 지침·버그·이력·과거 PR 의견·주석의 다섯 관점으로 검토하고 발견을 다시 확인한다. confidence 80 미만을 제외한다. 빌드·타입 검사는 CI에서 수행된다고 가정한다. | 독립 발견과 재검증을 분리한다. confidence는 모델 평가값이며 정확도 확률로 사용하지 않는다. 실제 테스트는 별도로 실행한다. |
| [공식 code-simplifier](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-simplifier/agents/code-simplifier.md) | 최근 변경에서 동작을 보존하며 중복·중첩·불필요한 추상화를 줄인다. 줄 수보다 명확성을 우선한다. | 원문 바이트·실패 기록·출력 계약을 보존한다. 기본 JS/React 규칙은 Python 코드에 그대로 복사하지 않는다. |
| [PR Review Toolkit](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/pr-review-toolkit/README.md) | 주석·테스트 행동·조용한 실패·타입 불변조건·일반 리뷰·단순화를 나눈다. | 원문 수집 실패를 성공으로 보이는 fallback, 날짜/단위/단계 계약, 문서와 실제 구현의 차이를 우선 검토한다. |
| [공식 Code Review 문서](https://code.claude.com/docs/en/code-review) | 내장 local 명령, 공개 플러그인, hosted 서비스는 범위와 실행 방식이 다르다. 수정·외부 댓글 옵션도 구분된다. | 현재는 패턴만 적용한다. 플러그인 설치·유료 hosted 서비스·외부 AI 실행 없이 기존 Codex와 표준 Python 검증을 사용한다. |
| [Reddit 리뷰 부담 논의](https://www.reddit.com/r/ClaudeCode/comments/1wpovtv/the_slow_collapse_of_code_reviews_how_do_you_deal/) | 서로 다른 지시의 리뷰 에이전트를 사용해도 작성자가 변경을 이해하고 책임져야 한다는 경험을 공유한다. | 에이전트 수나 의견 일치를 품질의 증명으로 삼지 않는다. 반례·실행 결과를 확인한다. |
| [Reddit 장기 AI 개발 경험](https://www.reddit.com/r/ClaudeCode/comments/1qxvobt/ive_used_ai_to_write_100_of_my_code_for_1_year_as/) | 테스트의 중요성과 쓸모없는 AI 생성 테스트가 만드는 거짓 안도감을 함께 논의한다. | 요구사항에서 기대 결과를 정하고 경계값·오류·재실행을 검사한다. 테스트 수만 늘리지 않는다. |
| [SlopCodeBench 논문 v2](https://arxiv.org/abs/2603.24755v2), [저자 GitHub](https://github.com/SprocketLab/slop-code-bench) | 요구사항이 반복해서 바뀔 때 기능 통과와 코드 중복·복잡성의 누적을 따로 평가한다. | 한 번의 PASS와 향후 수정 용이성을 분리한다. 이 benchmark의 결과로 우리 저장소나 현재 모델의 품질을 점수화하지 않는다. |

[Claude 공식 YouTube 소개](https://www.youtube.com/watch?v=RKsADl0ZC3Y)는 2026-03-09 공개된 Code Review의 병렬 탐색·발견 재검증 원리를 설명하는 보조 자료다. 검색 메타데이터·설명과 [공식 발표](https://claude.com/blog/code-review)를 확인했으며 영상 재생·자막 분석은 하지 않았다. 기술 동작은 위 공식 문서와 소스에서 확인했다.

공식 페이지와 GitHub `main`은 바뀔 수 있으므로 이 표는 위 기준일의 확인이다. 새로운 Claude 기능이나 설치 명령을 이 Python 프로젝트의 필수 구성요소로 지정하지 않는다.

## 코드에서 재현한 문제

아래 네 건은 **P2**로 분류했다. 현재 단일 사례·수동 파이프라인의 신뢰성과 복구 가능성에 영향을 주는 수정 대상이다. 합성 자료의 실패 재현을 실제 수집 자료의 오류나 경제적 사건으로 해석하지 않는다.

### 중간 저장 실패 후 자동 재시도가 막힘

위치: [수집기 391행](../../../scripts/collect_customer_commitment.py#L391).

`capture`는 최신 `record.json`을 먼저 바꾸고 `acquisition.json` ledger를 나중에 바꾼다. 두 번째 capture에서 ledger 쓰기만 실패시키면 최신뷰는 새 revision을, ledger는 이전 revision을 가리킨다. 이후 검증과 같은 입력 재시도는 모두 `current record view differs from its immutable capture`로 실패한다.

이 검증은 불일치 상태를 성공으로 승인하지 않는다. 기존 불변 기록도 남아 있다. 문제는 자동 복구 없이 수집 재개가 막히는 것이다. 수정은 authoritative ledger와 재생성 가능한 최신뷰를 분리하고, 두 파일 교체 사이의 실패를 복구하도록 해야 한다. 회귀 사례는 두 번째 저장 실패 뒤 기존 유효 revision을 검증하고 재시도가 가능한지 확인해야 한다.

### 불가능한 시각도 검증에 통과함

위치: [SEC 시각 추출 150행](../../../scripts/collect_customer_commitment.py#L150), [수집 시각 입력 361행](../../../scripts/collect_customer_commitment.py#L361).

SEC acceptance 추출은 문자열의 모양만 확인한다. 합성 자료의 acceptance를 `2025-99-99 99:99:99`, 내부 함수의 `timestamp`를 `not-an-ISO-date`로 바꾸면 저장되고 `verify_capture`가 PASS를 반환한다. 원문 재추출·해시 일치는 달력과 UTC 시각의 유효성을 보장하지 않는다.

달력·시간 범위를 검사하고 retrieval 시각의 UTC 계약을 확인해야 한다. SEC acceptance의 미확인 시간대를 임의 추정할 필요는 없다. CLI 기본 retrieval 시각은 `datetime.now(timezone.utc)`에서 생성되므로 이 재현을 모든 실제 수집 시각이 잘못됐다는 주장으로 넓히지 않는다.

### 캐시 반환 전에 현재 원문 해시를 확인하지 않음

위치: [파이프라인 284행](../../../src/pipeline.py#L284).

기존 `run_result.json`이 있고 scenario fingerprint가 같으면 archive 해시 검사보다 먼저 반환한다. 임시 workspace에서 정상 실행 뒤 원문만 바꾸고 같은 scenario를 재실행하면 이전 결과와 `HUMAN_APPROVED` 상태가 그대로 반환된다.

이는 과거 승인 결과의 반환이며 AI가 새 승인 기록을 만든 것은 아니다. 다만 현재 원문으로 재검증했다고 해석할 수 없는 경로다. 재실행에서 source dependency를 검사하거나 과거 snapshot 읽기와 현재 원문 검증을 명시적으로 분리해야 한다. 회귀 사례는 원문 변경 뒤 같은 scenario 재실행을 포함해야 한다.

### 전체 테스트가 실제 연구 아카이브를 재작성함

위치: [테스트 setup 38행](../../../tests/test_h1_full_corpus.py#L38), [아카이브 쓰기 540행](../../../src/measurement/corpus.py#L540).

`CorpusBuilder(ROOT)`가 실제 repository를 build workspace로 사용한다. 전체 테스트는 115개 모두 통과했지만 Windows에서 아카이브 36개가 LF에서 CRLF로 바뀌었다. `.gitattributes`의 해당 원문은 `-text`이므로 이는 무시할 텍스트 표시 차이가 아닌 실제 바이트 변경이다. 최초 재작성 뒤의 bytes를 비교하는 replay 테스트로는 실행 전 checkout 변화를 잡지 못한다.

입력을 임시 workspace로 복사하고 그 안에서만 build해야 한다. 종료 후 입력 byte hashes와 작업 트리의 무변경도 확인해야 한다. 이번 테스트가 만든 아카이브 변경은 검토 시작 시 깨끗했던 커밋으로 복구했고, 이후 추적된 기존 파일의 변경이 없음을 확인했다.

## 현재 진행 내용의 점검

| 영역 | 현재 실물과 판단 | 보완할 부분 |
|---|---|---|
| 상품·고객 중심 목적 | `AGENTS.md`와 상품/산업/지표 목적 문서에 구현 범위와 금지 해석이 있다. **CONTINUE**. | 공개 링크를 실제 고객 주문·채택·물량으로 승격하지 않는 기준을 유지한다. |
| 단일 고객 약정 수집 | 수집기·issuer 원문/metadata capture 한 건·합성 회귀 25개가 있다. 저장된 capture의 원문 해시·재추출은 PASS였다. | 조건부 최대 약정과 실제 현금·설비 배정·가동을 계속 구분한다. 저장 실패·날짜 회귀가 추가로 필요하다. |
| 최신 연구 검증 재현 | 최신 34개 번호 지표와 6개 가족 계약의 검토는 존재하지만 관련 검증 명령이 저장소 밖에 있다. **REWORK**. | clone만으로 기존 API 자료·목적 등록표·참조·hash·후보 상태를 확인하는 최소 진입점을 보존한다. |
| 과거 다음 작업 안내 | 현재 목적 문서는 KOSIS 측정 계약을 다음으로 정한다. 과거 고객 약정 문서는 주문서 후속 공시 또는 상품·고객 연결을 아직 다음으로 표시한다. **REWORK**. | 과거 판단을 삭제하지 않고 당시 권고라고 표시하며 현재 목적 문서로 연결한다. |
| 새 관리 runtime·대시보드·상시 수집 | 지금 확인한 문제 해결의 필수 요소가 아니다. **DEFER**. | 현재 코드와 검증 계약을 먼저 정비한다. |

최신 자료 검증 공백의 근거는 [목적 검토 완료 계획 33행](../../exec-plans/completed/indicator_purpose_review_20261005.md#L33)과 [기존 검증기 11행](../../../scripts/validate_supply_chain_research.py#L11)이다. 기존 검증기는 2026-10-03 bundle의 `artifacts` 계약용이며 최신 `files/byte_size` manifest를 검증하는 명령이 아니다. 이는 당시 로컬 검증이 거짓이었다는 판단이 아니라 **그 절차가 clone에 포함되지 않은 재현성 공백**이다.

안내 충돌은 [첫 사례 마지막 권고](../../research/supply_chain/first_case_review.md#L43), [당시 수집 완료 계획](../../exec-plans/completed/customer_commitment_collection_20261003.md#L35), [경제적 목적 첫 갱신](../../research/supply_chain/decision_purpose.md#L5)과 [현재 목적](../../research/supply_chain/indicator_collection_purpose.md#L163)을 비교했다. 전체 세계지도·반복 수집·선행성 검증은 여전히 완료되지 않았다.

## 반복해서 사용할 검토 절차

1. 변경 전 목적·범위·기존 동작·source hashes·작업 트리 상태를 기록한다.
2. 작성자와 역할을 나눈 검토자가 정확성·실패 처리·자료 계약·목적 적합성을 확인한다. 구현자의 설명을 정답으로 삼지 않는다.
3. 발견을 `파일과 행 → 발생 입력 → 실제 결과 → 기대 결과 → 영향`으로 기록하고 다른 담당자가 재현한다. 재현되지 않은 의심과 취향은 별도 제안으로 둔다.
4. 수정 작업에서는 먼저 요구사항 기반 회귀 사례를 고정하고 최소 부분만 바꾼다. 오류를 없애려고 테스트 기대값이나 원문 데이터를 낮춰 맞추지 않는다.
5. 수정한 경로와 관련 기존 검증을 실행하고 원문·승인 상태·실패 이력·작업 트리를 확인한다. 기능 보존 단순화는 확인된 필요가 있을 때 수행한다.
6. 확인된 수정 대상이 해결되고 관련 검증과 불변조건이 통과하면 종료한다. 리뷰 횟수·코드 줄 수·모델 점수 때문에 반복하지 않는다.

다음 리뷰에 사용할 짧은 지시:

> 목적과 변경 범위에 영향을 주는 정확성·출처·날짜·단위·단계·실패/재실행 문제만 검토하라. 파일/행, 최소 입력, 실제 결과, 기대 결과와 영향을 제시하라. 발견은 별도 담당자가 재현하게 하고, 취향 리팩터링이나 억지 결함을 만들지 마라. 코드 동작 PASS와 경제적 의미·사람 승인·선행성은 구분하라.

이번에는 역할별 검토 에이전트와 root 재현을 사용했다. 에이전트는 기존 대화 맥락과 같은 모델을 공유하므로 완전히 독립된 blind review나 다른 모델 교차 검토를 수행했다고 주장하지 않는다. Claude 플러그인 자체의 효과도 측정하지 않았다.

## 실제 확인 결과와 재현

- Windows 기본 sandbox Temp에서는 권한 오류로 전체 테스트가 중단됐다. 작업 폴더 안으로 Python `tempfile.tempdir`를 지정한 재실행은 **115 tests, OK**였다. 환경 실패와 코드 발견을 분리했다.
- 위 날짜·저장 실패·캐시 사례는 독립 리뷰 담당자와 root가 합성 fixture 및 임시 workspace에서 각각 재현했다. 날짜 probe의 PASS는 **문제를 재현한 출력**이며 품질 승인 결과가 아니다.
- [observations.json](observations.json)은 root의 오프라인 재현 출력을 보존한다. 실제 원문 수집·현재 사건 관측·경제적 선행성 결과가 아니다.
- 재현 파일은 정식 unittest discovery에 포함되지 않는 날짜별 진단 동반 파일이다. 외부 요청·비밀 읽기·canonical corpus build를 수행하지 않는다. 종료 코드 0은 probe 실행 완료를 뜻한다.

repository root에서:

```powershell
python -B docs/reviews/2026-10-06/reproduce_findings.py
```

재현 파일은 임시 복사만 `work/code_review_20261006/` 아래에 쓰고 제거하며 stdout으로 결과를 낸다. 향후 실제 버그 수정 뒤에는 결과가 달라지거나 기존 재현이 실패할 수 있으므로 이 기록의 검토 커밋과 구분한다.

**다음 작업 하나:** 테스트를 임시 workspace로 격리하고 원문 해시·중간 저장 실패·시각 검증 및 최신 자료 검증을 저장소 내 명령으로 재현하는 검증 정비를 수행한다. 범위가 이어지는 하나의 검증 정비 작업이며 신규 수집·runtime은 포함하지 않는다. 그 뒤 경제적 조사 순서는 기존 한국 KOSIS 생산/출하/재고와 교역의 측정 계약 작업을 유지한다.

정비의 완료 기준은 기존 입력 bytes 무변경, 원문 변경 후 캐시 재검증, 중간 저장 실패 후 유효 revision 복구·재시도, 유효하지 않은 시각 거부, clean clone에서 최신 bundle 검증 명령 재현이다.
