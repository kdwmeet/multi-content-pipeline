from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END

load_dotenv()

# 상태 정의
class ContentState(TypedDict):
    source_material: str
    blog_post: str
    linkedin_post: str
    twitter_thread: str
    fianl_summary: str

# 노드 구형
def blog_node(state: ContentState):
    """소스 자료를 바탕을 ㅗ긴 분량의 블로그 포스트를 작성"""
    llm = ChatOpenAI(model="gpt-5.4-nano", reasoning_effort="high")
    source = state.get("source_material", "")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 전문 블로그 에디터입니다. 제공된 소스 자료를 바탕으로 가독성 높은 블로그 포스트를 작성하십시오. 마크다운 형식으로 제목과 소제목을 반드시 포함해야 합니다."),
        ("user", "소스 자료:\n{source}")
    ])

    response = (prompt | llm).invoke({"source": source})
    return {"blog_post": response.content}

def linkedin_node(state: ContentState):
    """소스 자료를 바탕으로 비즈니스인사이트가 담긴 링크드인 게시물을 작성"""
    llm = ChatOpenAI(model="gpt-5.4-nano", reasoning_effort="high")
    source = state.get("source_material", "")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 링크드인 콘텐츠 크리에이터입니다. 소스 자료를 바탕으로 비즈니스 인사이트가 담긴 링크드인 게시물을 작성하십시오. 문단은 짧게 나누고 비즈니스 커뮤니케이션에 맞는 전문적인 어조를 유지하십시오."),
        ("user", "소스 자료:\n{source}")
    ])

    response = (prompt | llm).invoke({"source": source})
    return {"linkedin_post": response.content}

def twitter_node(state: ContentState):
    """소스 자료를 바탕으로 짧은 트위터 스레드를 작성"""
    llm = ChatOpenAI(model="gpt-5.4-nano", reasoning_effort="high")
    source = state.get("source_material", "")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 소셜 미디어 인플루언서입니다. 소스 자료를 바탕으로 사람들의 이목을 끄는 짧고 강렬한 스레드(연속된 게시물)를 작성하십시오. 각 문단은 번호를 매겨 구분하십시오."),
        ("user", "소스 자료:\n{source}")
    ])

    response = (prompt | llm).invoke({"source": source})
    return {"twitter_thread": response.content}

def aggregator_node(state: ContentState):
    """병렬 노드들의 작업이 모두 끝난 후 실행되어 상태를 취합"""
    return {"final_summary": "모든 플랫폼의 콘텐츠 생성이 완료되었습니다."}

# 그래프 조립 및 컴파일
workflow = StateGraph(ContentState)

workflow.add_node("blog", blog_node)
workflow.add_node("linkedin", linkedin_node)
workflow.add_node("twitter", twitter_node)
workflow.add_node("aggregator", aggregator_node)

# START에서 3개의 노드로 분기 (Fan-Out)
workflow.add_edge(START, "blog")
workflow.add_edge(START, "linkedin")
workflow.add_edge(START, "twitter")

# 3개의 노드가 끝나면 하나의 노드로 수렴 (Fan-In)
workflow.add_edge("blog", "aggregator")
workflow.add_edge("linkedin", "aggregator")
workflow.add_edge("twitter", "aggregator")

workflow.add_edge("aggregator", END)

app_graph = workflow.compile()