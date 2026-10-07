# AI 코드 정리 방법과 구조 필요성 검토

기준일 2026-10-07, 변경 전 저장소 `83f2e1ce819f0966bde45575ca1455f140cb181b`.

**불필요한 설정·구조가 0개라고 판단할 근거는 없었고, 실제로 사용하지 않는 adapter 계층이 남아 있었다.** 앞선 문서 정리와 143개 테스트 통과는 전체 구조의 필요성을 증명하지 않는다. 이번에는 영어 개발자 자료를 먼저 비교하고, 요청한 결과에 필요한 소비처를 추적해 확인된 구조를 제거했다.

현재 A는 하이닉스를 중심으로 제품·구매자·공급자·정부·산업의 관계와 목적별 무료 지표 수집 가능성을 설명하는 것이다. 코드 정리를 먼저 하라는 사용자 지시에 따라 이번 작업에서는 KOSIS 수집을 진행하지 않았다. 이미 승인된 H1 연구 계약과 그 재현 경로는 별도로 보존한다.

## 영어 자료에서 확인한 방법

검색은 `AI generated code overengineering cleanup`, `code simplifier code review plugin`, `AI reviewing AI refactoring`, `unnecessary abstractions dead code` 등의 영어 질의로 진행했다. GitHub 작성자 원문은 도구의 범위·동작 근거이고, Reddit과 개인 영상은 경험·실연이다. 효과의 보편적 보장으로 해석하지 않는다.

| 원문과 날짜 | 가져올 방법 | 적용 한계 |
| --- | --- | --- |
| [Anthropic code-simplifier](https://github.com/anthropics/claude-plugins-official/blob/ceb9b72b4c4c20ad39efce780edd0aabe80ebce3/plugins/code-simplifier/agents/code-simplifier.md), 확인 파일 commit 2026-01-09 | 동작·출력을 유지하며 중복·중첩·불필요한 추상화를 제거한다. 가독성을 우선한다. | 기본 범위는 최근 변경. Python에 JS·TS·React 규칙을 복사하지 않는다. |
| [Anthropic code-review](https://github.com/anthropics/claude-code/blob/db8834ba1d72e9a26fba30ac85f3bc4316bb0689/plugins/code-review/commands/code-review.md), 확인 파일 commit 2026-03-12 | 후보 발견과 실제 문제인지 재검증하는 역할을 나눈다. 위치·영향·근거를 제시한다. | 변경 diff의 새 버그 중심이며 기존 문제·일반 품질 문제를 제외한다. 기존 과잉 구조 감사와 별개다. 자기 confidence는 정확도 확률이 아니다. |
| [PR Review Toolkit](https://github.com/anthropics/claude-code/blob/f7ab5c799caf2ec8c7cd1b99d2bc2f158459ef5e/plugins/pr-review-toolkit/README.md), 열람 2026-10-07 | 주석·행동 테스트·조용한 실패·타입·일반 리뷰·단순화 중 관련 검토만 선택한다. | 모든 역할을 항상 실행하면 검토 절차 자체가 비대해질 수 있다. |
| [Vulture](https://github.com/jendrikseipp/vulture/blob/01b9ff53d25e17633241a7d0b202d9df02745a99/README.md), 확인 파일 commit 2025-11-25 | 소스와 테스트에서 unused·unreachable 후보를 찾고 소비처를 확인한다. | 동적 호출·암묵적 사용에 오탐·누락이 있다. 자동 삭제 근거가 아니다. |
| [Ruff](https://github.com/astral-sh/ruff/blob/c97af1e712cb3a61764e104065abaaef1001c59c/docs/linter.md), 확인 파일 commit 2026-09-30 | 수정 없는 결과부터 확인하고 필요한 규칙만 적용한다. | safe·unsafe fix와 공개 re-export·부수효과를 검토해야 한다. 전체 포맷 변경부터 시작하지 않는다. |
| [deptry](https://github.com/osprey-oss/deptry/blob/5cee3f280b2e8df85c28147d51079875c2d0a67d/docs/usage.md), 확인 파일 commit 2026-04-08 | 선언 의존성과 실제 import를 비교한다. | 변수 기반 동적 import는 놓칠 수 있다. 현재 저장소에는 외부 의존성 선언이 없어 도입할 이유가 없다. |
| [Radon](https://github.com/rubik/radon/blob/54b88e5878b2724bf4d77f97349588b811abdff2/README.rst), 확인 파일 commit 2024-10-20 | 복잡도·SLOC로 읽을 우선순위를 고른다. | 복잡도는 업무상 필요성·정확성의 판정값이 아니다. 현재 Python 지원은 따로 확인해야 한다. |
| [Fowler YAGNI](https://martinfowler.com/bliki/Yagni.html), 게시 2015-05-26 | 예상 미래 기능·확장성을 위해 현재 복잡성을 추가하지 않는다. | 실제 유지보수와 동작 검증까지 불필요하다는 뜻은 아니다. [작은 동작 보존 리팩토링](https://refactoring.com/)으로 변경한다. |

이 저장소에서는 설치보다 적용 원칙이 먼저다. AST import 조사에서 `src/scripts/tests`의 외부 패키지 import는 없었고, dependency manifest도 없었다. Ruff·Vulture·deptry·Radon·coverage는 확인한 Python 환경에 설치되어 있지 않았다. 이 정리를 위해 새 plugin·skill·hook·설정·의존성 manifest를 만들지 않았다.

## YouTube 실연과 환경 변화

세 영상의 업로드 메타데이터와 실제 영어 자막을 확인했다. 자동 자막은 표현·고유명사 오류가 있을 수 있어 방법을 공식 원문과 대조했다.

| 영상과 업로드일 | 확인 구간 | 적용할 내용 |
| --- | --- | --- |
| [AI Coding Daily Code Simplifier](https://www.youtube.com/watch?v=puynahM0Wew), 2026-01-09, 자동 영어 자막 | 00:15–00:18, 01:27–02:50 | 최근 commit으로 범위를 제한하고 TSX를 정리하되 PHP는 변경 불필요로 판정한다. React/Laravel의 작은 예제다. |
| [Dory Zidon Reviewing AI PRs at Scale](https://www.youtube.com/watch?v=tTl1gF31rp8), 2026-07-06, 자동 영어 자막 | 02:56–03:49, 04:48–05:02, 05:34–05:54 | 결정적인 검사 결과를 검토에 제공하고 작성 대화와 분리된 context를 쓴다. 관계없는 commit을 제외하고 수정 반복을 제한한다. |
| [Claude How the Claude Code team uses Claude Code](https://www.youtube.com/watch?v=S-sYlFiGFv8), 2026-09-02, 수동 영어 자막 | 03:25–04:46, 09:58–10:25, 11:23–11:44 | 과거 모델의 한계를 보완하던 구조도 더 이상 필요하지 않으면 제거한다. 큰 설계와 발견의 타당성을 별도로 검토한다. |

Dory의 [저자 동반 글](https://doryzidon.com/blog/reviewing-ai-prs-at-scale)은 2026-07-03 게시로 영상 업로드일과 다르다. 개인 자료의 free·zero-cost 표현은 모든 환경의 실행 비용 보장이 아니다. 공개 프롬프트를 읽는 것과 외부 모델·hosted 리뷰를 실행하는 것도 구분한다.

## Reddit 경험담과 반론

| 게시일과 논의 | 문제와 실무 팁 | 반론 |
| --- | --- | --- |
| [작은 작업의 과잉 구현](https://www.reddit.com/r/codex/comments/1vf5elq/how_do_you_stop_codexclaude_from_overengineering/), 2026-08-04 | endpoint 변경이 타입·추상화·mock·상태 확장으로 번졌다는 경험. 후속 단순화에서 같은 동작과 테스트 통과를 유지했다고 보고한다. 요청 결과·변경 범위를 먼저 고정한다. | 적은 코드 자체가 좋은 코드의 증거는 아니다. |
| [Claude keeps adding code](https://www.reddit.com/r/ClaudeAI/comments/1qz6cax/claude_keeps_adding_code/), 2026-02-08 | unused 함수 등 구체적 정리 대상을 지정하고 확인된 지적만 수정한다. | OP는 규칙이 무시되고 simplifier가 동작을 깨뜨린다고 응답한다. |
| [프롬프트와 절차의 과잉](https://www.reddit.com/r/ClaudeAI/comments/1us0h97/are_yall_overengineering_or_am_i_not_unlocking/), 2026-07-09 | 사소한 수정에도 AI가 절차·게이트·문서를 늘린다는 경험. 반복되는 실제 문제가 있을 때만 skill을 만든다. | 복잡한 환경에서는 문맥·검증 도구가 필요할 수 있다. |
| [비대한 AI 테스트](https://www.reddit.com/r/ExperiencedDevs/comments/1po8uud/my_teammates_are_generating_enormous_test_suites/), 2025-12-16 | 대량 boilerplate보다 요구·실패를 검출하는 공개 동작 사례를 확인한다. | coverage 목표에 대한 의견이 엇갈린다. 테스트 수·coverage만으로 충분함을 판단하지 않는다. |

이 논의들은 후보와 검토 질문을 제공한다. 참여자의 경험·댓글 동의는 도구 효과나 이 저장소의 삭제 안전성을 입증하지 않는다.

## 실제 구조와 소비처 판정

변경 전 Python 파일은 `src` 25개, `scripts` 3개, `tests` 10개였다. 파일별 import·정의와 관련 CLI·테스트·문서의 사용처를 조사했다. 단순 검색의 미검출은 삭제 판정이 아니므로 별도 검토자가 소비처와 반례를 확인했다.

| 대상 | 실제 소비처와 목적 | 판정 |
| --- | --- | --- |
| Sensor와 하위 Protocol 4개 | 정의 외 실행 소비처 없음. 미래 논리 역할을 빈 타입으로만 표현 | 구현에서 제거. 역할 개념은 과거 설계에 보존 |
| AgentAdapter와 ManualScenarioAdapter | pipeline 한 곳. payload 변환·복사 없이 전역 승인 키만 거절하고 같은 객체 반환 | guard를 동일 호출 위치에 합치고 두 adapter 파일 제거 |
| pipeline·core·retrieval·graph·audit·memo | 지원되는 scenario CLI가 출처→상태 전이→Graph/Audit→Memo를 재현 | 지원되는 이전 기능의 실제 경로. 이번 제거 대상 아님 |
| H1 measurement·corpus·Gate 6 | 승인 계약의 자료 준비·검토 패키지와 CLI·공개 export·테스트 | 보존. 현재 지표 연구에 재사용을 강제하지 않음 |
| research 검증기 두 개 | 고정된 자료·hash·pointer·분류·false 승인 상태 검증 | 유지. 원격 현재 접근성·경제적 진실을 검증한다고 표현하지 않음 |
| 단일 고객 약정 수집기 | 해당 case capture·검증·중간 저장 복구 | 유지. 범용 플랫폼이나 일괄 수집기로 확장하지 않음 |
| JSON schema 13개 | 코드가 파일을 자동 로드하지 않으나 명시적 데이터 계약·승인/문서 참조 | runtime 미사용만으로 삭제하지 않음. 모든 필드와 구현의 일치 검증은 별도 과제 |
| 초기 시작 prompt·project settings | 실제 소프트웨어 설정이 아닌 작업 지침. 전체 문맥 로드·재생성·기술 의무화가 현재 AGENTS와 충돌 | 현재 소유 문서에 연결하는 짧은 안내로 교체. 초기 내용은 Git 이력 보존 |
| .gitattributes·.gitignore | 원문 bytes/line endings 보존, cache·scratch의 추적 제외 | 원자료 재현에 직접 필요하므로 유지 |

제거된 패키지의 `__init__.py`는 빈 파일이 아니라 docstring만 가진 파일이었다. 발견한 7개 클래스와 그 패키지 2개 파일을 제거했으며 pipeline·기존 승인 계약의 의미는 보존한다. 이 저장소 밖에서 해당 내부 클래스를 import하는 소비처까지 조사한 것은 아니다.

## 적용과 검증

검토 순서는 요청 결과 고정 → 실제 진입점과 소비처 조사 → 필요성/정확성 별도 검토 → 작은 제거 → 출력·거절 경계 비교다. 검토자를 늘린다는 이유로 새 실행 framework를 추가하지 않는다. 이 작업의 검토 역할은 같은 모델의 역할 분담이며 모델 간 성능 비교가 아니다.

`run_vertical_slice`의 JSON 로드·파일 없음 검사 직후에 기존 `human_approved` 키 존재 검사를 유지했다. 값이 False라도 키가 있으면 거절하고, 캐시 반환·자료 쓰기보다 먼저 실행한다. 같은 오류 메시지를 보존한다. 기존 run/cache 경계에 대한 최소 회귀 사례 하나를 추가했다.

두 scenario의 변경 전후 cold replay workspace 31개 파일의 구성과 bytes가 같았다. 원자료·연구 후보·지원 수행 기록·schema 182개 파일의 구성과 bytes도 같았다. Python 파일은 38개에서 36개로 줄었고 외부 의존성은 추가되지 않았다.

Root가 PR #13의 어댑터 제거 변경본에서 임시 workspace를 사용해 전체 **144개 테스트 PASS**와 두 research validator PASS를 확인했다. 기존 143개에 승인 거절 경계 사례 하나를 추가한 결과다. 자료 검증기는 고정된 날짜 묶음에 대한 검사다. 별도 기술·목적 검토자는 실제 변경을 읽고 **CONTINUE**로 판정했고, 영상 담당자는 날짜·자막·구간과 해석을 재확인했다. 리뷰어들이 root의 실행 명령을 모두 재실행한 것은 아니다.

이번 완료 범위는 영어 방법 비교, 파일/소비처 수준 구조 조사, 확인된 adapter 제거와 충돌 지침 수정이다. 모든 schema 필드의 중복·계약 일치나 모든 함수의 의미까지 검증해 불필요한 구조가 0개라고 보증하는 감사는 아니다. H1 Gate 6·정식 Evidence·선행성·사람 승인 상태는 그대로다.

## 다시 확인할 조건

자료의 게시/commit 날짜와 열람일은 별개다. 모델·coding 도구·플러그인·Python·의존성·API 또는 사용자 목적이 바뀌면 관련 원문과 현재 소비처를 다시 확인한다. 특히 구형 모델 보완 구조, tool 지원 버전, 최근 diff에만 적용되는 리뷰 범위와 자동 수정의 실패 사례를 다시 본다. 최신이라는 이유만으로 새 설정이나 플러그인을 추가하지 않는다.

정기 감시나 자동 업데이트는 이번 요청의 산출물이 아니다. 다음 경제적 작업은 기존 KOSIS 측정 계약이며, 그때도 실행 framework보다 정확한 표·필드·단위·시점을 먼저 정한다.

## 개발자가 유지하는 최신 방법 확인

2026-10-07 추가 확인. 사용자가 제시한 [노마드 코더 영상](https://www.youtube.com/watch?v=3JCgiVYlLFo&t=97s)은 2026-10-04 게시됐다. 공개 메타데이터·실제 영어 자동 자막과 설명란의 네 저장소 링크를 확인했다. 01:37은 작은 요구에도 파일·추상화를 늘리는 문제, 02:00·03:05·04:05·08:42는 아래 네 도구다. 개발자의 소개·시연이며 독립 효과 검증은 아니다. 협찬 구간의 생산성 수치는 채택 근거로 사용하지 않는다.

단순 추천 목록보다 실제 규칙 파일·commit·release·최근 실패 보고를 조사 단위로 삼는다. 아래 commit 날짜는 UTC이며 저장소 활동일·조회일과 구분한다. 새로운 PR·개발 브랜치가 있다는 사실은 현재 안정 배포에 반영됐다는 뜻이 아니다.

| 자료와 확인한 코드 | 역할과 최신성 | 이 저장소에 가져올 부분 |
| --- | --- | --- |
| [Attention Span](https://github.com/alexgreensh/attention-span/blob/2714c965e6be1fa2597510e66651e63bc67cb448/output-styles/attention-kind.md) | main 2026-09-06, release 0.8도 09-06. 응답 가독성을 위한 output style이며 코드 정리 검출기가 아니다. | 답변은 짧게 하되 조사·검증을 축소하지 않는다. 자체 벤치마크는 우리 설계 품질의 검증이 아니다. |
| [Karpathy Skills](https://github.com/multica-ai/andrej-karpathy-skills/blob/2c606141936f1eeef17fa3043a72095b4765b9c2/skills/karpathy-guidelines/SKILL.md) | main 2026-04-20, SKILL 마지막 수정 01-28. Karpathy의 관찰에서 만든 Multica/forrestchang의 제3자 지침이며 공식 배포물이 아니다. releases 목록 없음. | 가정을 밝히고 현재 요구에 필요한 최소 구현과 직접 연결되는 변경·완료 조건을 정한다. |
| [Anti Slop](https://github.com/dmmulroy/anti-slop/blob/c44ef22ca116d0ba62a3ff663a0bd13a3f3fa40b/README.md) | main/README 2026-09-10, releases 목록 없음. JS·TS용 Oxlint 규칙이며 저자의 팀 취향을 담는다. | 실제 증거 없는 패턴을 구체적으로 검사하는 접근을 참고한다. Python에 TS 규칙·Node 설정을 설치하지 않는다. |
| [Verification Before Completion](https://github.com/obra/superpowers/blob/3be5aad3dd2400ef23b15680969f4bcd3b6d7b8b/skills/verification-before-completion/SKILL.md) | SKILL 마지막 main 수정 2026-07-24. Superpowers 안정 main/release v6.4.2는 09-25이며 파일 내용은 동일하다. | 주장에 맞는 명령을 현재 변경에서 실행하고 출력·종료코드·실패 수를 확인한다. 테스트 통과·버그 수정·요구 충족은 서로 다른 주장이다. |

실제 사용 중 나온 변경·실패가 적용 조건을 알려 준다. 아래 경험·수치는 작성자 보고이며 우리 환경에서 재현한 결과가 아니다.

- **간결함 때문에 일을 일찍 끝냄:** Attention Span [PR #7](https://github.com/alexgreensh/attention-span/pull/7)은 데이터 파이프라인 조사에서 실측·프로파일링 전에 그럴듯한 설명으로 종료하던 사례를 다뤘다. 2026-09-06 병합됐고, 보고의 간결함과 작업 완료를 구분하도록 수정했다. [Issue #10](https://github.com/alexgreensh/attention-span/issues/10)의 단답용 형식 축소는 열린 제안이다.
- **환경 변경으로 설정이 중복됨:** Karpathy Skills [PR #136](https://github.com/multica-ai/andrej-karpathy-skills/pull/136)은 Claude Code의 skill 발견 방식 변경 뒤 plugin 설정이 중복 등록을 만든다는 보고다. 09-13 갱신됐지만 open·unmerged다. 작성자의 token 감소 수치를 검증 결과로 가져오지 않는다. 10-04의 [PR #206](https://github.com/multica-ai/andrej-karpathy-skills/pull/206)도 열린 설명 형식 제안이며 새 release가 아니다.
- **이름만 보고 오탐:** Anti Slop [Issue #50](https://github.com/dmmulroy/anti-slop/issues/50)은 배열이라는 증거 없이 custom `reduce`를 경고한 사례다. 10-06 [PR #51](https://github.com/dmmulroy/anti-slop/pull/51)은 아직 미병합이다. 기존 테스트 통과 상태의 edge case 보고 [#47](https://github.com/dmmulroy/anti-slop/issues/47)와 대응 [#52](https://github.com/dmmulroy/anti-slop/pull/52)·[#53](https://github.com/dmmulroy/anti-slop/pull/53)도 구분해 읽었다.
- **계획과 승인 절차가 목적을 밀어냄:** 안정 v6.4.2에 포함된 [Superpowers PR #2333](https://github.com/obra/superpowers/pull/2333)은 계획의 코드 중복과 불필요한 reviewer prompt를 줄였다. 더 최신인 [PR #2463](https://github.com/obra/superpowers/pull/2463)은 목적을 파악한 뒤 작업 규모에 맞춰 절차를 정하도록 재작성했으며, 10-06 23:57:53 UTC에 [dev](https://github.com/obra/superpowers/blob/9e639188a1a8029926bda6e5d7edbf66ef3ac333/skills/brainstorming/SKILL.md)에 병합됐다. 안정 v6.4.2에는 미포함이다. 전체 승인 흐름을 우리 작업에 수입하지 않는다.
- **검증 실패 원인을 잘못 인정함:** Superpowers [Issue #2452](https://github.com/obra/superpowers/issues/2452)는 모듈 누락·명령 오류로 빨간 테스트를 유효한 회귀 증거로 착각한 사례다. [#2451](https://github.com/obra/superpowers/issues/2451)은 실제 diff 대신 계획을 따라 완료 보고가 작성된 사례다. 두 보고는 10-03 게시됐다. 우리에게는 요청별 실제 변경을 확인하고, 거절 시험이 예상 위반 진단 때문에 실패했는지 확인하는 기준으로 적용한다.

Attention Span이 연결한 [Token Optimizer](https://github.com/alexgreensh/token-optimizer/blob/247edced8f8baca0dab996eb8228816b821a8e11/README.md)는 별도의 context/config 감사 도구다. main과 v5.13.35 release는 2026-10-05다. [CHANGELOG](https://github.com/alexgreensh/token-optimizer/blob/247edced8f8baca0dab996eb8228816b821a8e11/CHANGELOG.md)의 누적 사용량·현재 context 점유 혼동과 Windows launcher 교정은 환경별 점검의 실제 사례다. 중복 지침·참조 파일·도구 구성 감사 아이디어를 참고하되, [SKILL](https://github.com/alexgreensh/token-optimizer/blob/247edced8f8baca0dab996eb8228816b821a8e11/skills/token-optimizer/SKILL.md)의 자기 도구 정리 면제는 채택하지 않는다. 모든 도구의 현재 사용처를 같은 기준으로 확인한다.

Python을 지원하는 [Desloppify](https://github.com/peteromallet/desloppify/blob/3a7735d531a96b6a226bfbdc9fd662b14195f857/README.md)도 보조 비교했다. 확인한 최신 main과 release v1.0은 2026-05-13이다. 기계적 검출과 의미 검토를 나누는 방식은 유용하지만, 점수·지속 상태·실행 harness 전체를 현재 목적에 추가할 근거는 부족하다. 최근 10월 개선과 같은 최신성으로 소개하지 않는다.

이번 추가 작업은 최신 방법의 확인과 기존 작업 규칙 보완이다. 새로운 구조 제거·전체 코드 재감사·외부 도구 효과 검증은 수행한 것으로 보고하지 않는다. 기존 AGENTS에 보고 간결화와 작업 완료의 구분, 작업에 맞는 현재 검증·예상 진단 확인을 보완한다. plugin·skill·hook·lint 설정·상시 감시를 추가하지 않는다.

이번 문서 보완에서는 root가 두 research validator, 로컬 링크 35개와 변경 문서 3개 범위 검사를 다시 실행해 PASS를 확인했다. 원자료·코드·테스트·schema 등 219개 파일의 구성과 bytes를 보존했다. 위 144개 전체 테스트는 PR #13 당시 결과이며 이번 문서 변경에서 재실행한 것으로 표현하지 않는다.
