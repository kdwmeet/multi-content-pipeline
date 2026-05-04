import streamlit as st
from app.graph import app_graph

st.set_page_config(page_title="멀티 플랫폼 파이프라인", layout="wide")

st.title("소스 기반 멀티 플랫폼 콘텐츠 자동 발행기")
st.markdown("하나의 소스 데이터를 입력하면 블로그, 링크드인, 트위터 에이전트가 병렬로 작동하여 각 플랫폼에 최적화된 콘텐츠를 동시다발적으로 생성합니다.")
st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("소스 데이터 입력")
    with st.form("content_form"):
        source_input = st.text_area(
            "콘텐츠의 원본이 될 메모, 인터뷰 스크립트, 또는 기사 내용을 입력하십시오.",
            height=300,
            placeholder="예: 이번 분기 영업이익이 전년 대비 15% 상승했습니다. 주력 서비스인 클라우드 부문의 매출 증대가 주요 원인입니다. 다음 분기에는 글로벌 시장 진출을 가속화할 예정입니다."
        )
        submit_btn = st.form_submit_button("병렬 콘텐츠 생성 시작", use_container_width=True)

with col2:
    st.subheader("플랫폼별 생성 결과")
    
    if submit_btn and source_input.strip():
        initial_state = {
            "source_material": source_input,
            "blog_post": "",
            "linkedin_post": "",
            "twitter_thread": "",
            "final_summary": ""
        }

        # 결과를 출력할 영역 미리 확보
        blog_container = st.expander("블로그 포스트", expanded=True)
        linkedin_container = st.expander("링크드인 포스트", expanded=True)
        twitter_container = st.expander("트위터 스레드", expanded=True)

        with st.spinner("3개의 에이전트가 동시에 콘텐츠를 작성 중입니다..."):
            for output in app_graph.stream(initial_state):
                if not output:
                    continue

                for node_name, state_update in output.items():
                    if not state_update:
                        continue

                    if node_name == "blog":
                        blog_container.markdown(state_update.get("blog_post", ""))
                    elif node_name == "linkedin":
                        linkedin_container.markdown(state_update.get("linkedin_post", ""))
                    elif node_name == "twitter":
                        twitter_container.markdown(state_update.get("twitter_thread", ""))
                    elif node_name == "aggregator":
                        st.success(state_update.get("final_summary", ""))

    elif not submit_btn:
        st.info("좌측에 소스 데이터를 입력하고 파이프라인을 가동하십시오.")