# Multi-Platform Content Auto-Publisher (소스 기반 멀티 플랫폼 콘텐츠 자동 발행기)

## 1. 프로젝트 개요

이 프로젝트는 LangGraph의 병렬 처리(Parallel Execution) 기능을 실무에 적용한 콘텐츠 자동화 파이프라인입니다. 

사용자가 단일 소스 데이터(메모, 기사, 인터뷰 스크립트 등)를 입력하면, 시스템이 여러 에이전트를 동시에 가동하여 블로그, 링크드인, 트위터 등 각 플랫폼의 특성에 맞는 콘텐츠를 동시다발적으로 생성합니다. 하나의 입력으로 다수의 결과물을 얻어내는 Fan-out / Fan-in 아키텍처를 구현하여 작업 시간을 획기적으로 단축합니다.

## 2. 시스템 아키텍처 및 워크플로우

본 시스템은 다중 에이전트의 비동기 병렬 실행 구조를 가집니다.

1. State Definition: 원본 소스 데이터와 각 플랫폼별 생성 결과물을 담을 수 있는 상태(State)를 정의합니다.
2. Parallel Nodes (Fan-out): 파이프라인이 시작되면 제어권이 3개의 노드(블로그, 링크드인, 트위터 에이전트)로 동시에 분기됩니다. 각 에이전트는 서로 독립적으로 작동하며 플랫폼의 톤앤매너에 맞게 텍스트를 작성합니다.
3. Aggregator Node (Fan-in): 모든 병렬 작업이 완료되면 하나의 노드로 다시 수렴하여 상태를 최종 취합하고 스트리밍 결과를 사용자에게 반환합니다.

## 3. 기술 스택

* Language: Python 3.10+
* Package Manager: uv
* LLM: OpenAI gpt-5.4-nano (각 플랫폼의 문체와 포맷을 정교하게 모방하기 위해 reasoning_effort="high" 적용)
* Orchestration: LangGraph (StateGraph 병렬 라우팅 제어)
* Web Framework: Streamlit (비동기 스트리밍 결과 실시간 렌더링)

## 4. 프로젝트 구조
```
multi-content-pipeline/
├── .env                  
├── requirements.txt      
├── main.py               
└── app/
    ├── __init__.py
    └── graph.py          
```
## 5. 핵심 준수 사항 (개발 가이드라인)

시스템의 안정성과 논리적 무결성을 위해 다음 규칙을 엄격히 준수합니다.

* 프롬프트 템플릿 보호: ChatPromptTemplate 구성 시 파이썬 f-string을 절대 사용하지 않습니다. 사용자가 입력하는 소스 데이터 내의 특수 기호가 템플릿 변수와 충돌하는 것을 방지하기 위해, 원본 데이터는 .invoke() 실행 단계에서 딕셔너리 형태로 안전하게 주입합니다.
* 안전한 상태 참조: 상태 딕셔너리 접근 시 초기화 지연으로 인한 KeyError를 방지하기 위해 반드시 state.get("키", 기본값) 방식을 사용합니다.
* 스트리밍 예외 처리: 병렬 노드에서 데이터가 반환될 때 간헐적으로 발생할 수 있는 null 값을 방지하기 위해, 출력 결과를 순회할 때 반드시 방어 로직(if not state_update: continue)을 포함합니다.

## 6. 설치 및 실행 가이드

### 6.1 환경 변수 설정
프로젝트 루트 경로에 .env 파일을 생성하고 API 키를 입력하십시오.
OPENAI_API_KEY=sk-your-api-key-here

### 6.2 의존성 설치 및 실행
uv venv
uv pip install -r requirements.txt
uv run streamlit run main.py

## 7. 활용 예시

* 소스 입력: "이번 3분기 매출 20% 증가. 신규 AI 서비스 도입이 주효했음. 내년 상반기 유럽 진출 예정."
* 병렬 출력 결과:
  - [블로그] 서론, 본론(매출 증가 원인, 유럽 진출 계획), 결론으로 나뉜 긴 줄글 포스팅
  - [링크드인] 비즈니스 인사이트에 초점을 맞춘 프로페셔널한 요약 글
  - [트위터] 사람들의 이목을 끄는 해시태그와 짧은 문장으로 이루어진 스레드

## 8. 실행 화면

<img width="1516" height="996" alt="스크린샷 2026-05-04 112722" src="https://github.com/user-attachments/assets/daadaa27-aa66-4cc0-900f-fc0a6664f49a" />
