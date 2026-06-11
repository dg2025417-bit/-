import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────
# 페이지 기본 설정
# ─────────────────────────────────────────────
st.set_page_config(page_title="청소년 SNS와 정신건강", layout="wide")
st.title("📱 하루 SNS 사용량과 학생 생활 지표 비교")
st.write("당곡고등학교 데이터 탐구 - SNS 사용 시간에 따른 수면, 학업, 신체활동, 스트레스 변화")

# ─────────────────────────────────────────────
# 데이터 불러오기 (영어 → 한글 번역)
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Teen_Mental_Health_Dataset.csv")

    # 값 번역
    df["gender"] = df["gender"].map({"male": "남성", "female": "여성"})
    df["platform_usage"] = df["platform_usage"].map({
        "Instagram": "인스타그램", "TikTok": "틱톡", "Both": "둘 다"
    })
    df["social_interaction_level"] = df["social_interaction_level"].map({
        "low": "낮음", "medium": "보통", "high": "높음"
    })

    # 열 이름 번역
    df = df.rename(columns={
        "age": "나이", "gender": "성별",
        "daily_social_media_hours": "하루SNS사용시간",
        "platform_usage": "사용플랫폼", "sleep_hours": "수면시간",
        "screen_time_before_sleep": "취침전스크린시간",
        "academic_performance": "학업성취도", "physical_activity": "신체활동량",
        "social_interaction_level": "사회적상호작용",
        "stress_level": "스트레스수준", "anxiety_level": "불안수준",
        "addiction_level": "중독수준", "depression_label": "우울증여부"
    })
    return df

df = load_data()

# ─────────────────────────────────────────────
# 데이터 미리보기
# ─────────────────────────────────────────────
with st.expander("📋 데이터 미리보기 (클릭하여 펼치기)"):
    st.dataframe(df.head(20))
    st.write(f"전체 학생 수: {len(df)} 명")

# ─────────────────────────────────────────────
# 하루 SNS 사용시간을 구간으로 나누기
# ─────────────────────────────────────────────
구간경계 = [0, 2, 4, 6, 8.1]
구간이름 = ["0~2시간", "2~4시간", "4~6시간", "6~8시간"]
df["SNS사용구간"] = pd.cut(df["하루SNS사용시간"], bins=구간경계,
                          labels=구간이름, right=False)

# 구간별 평균 계산
평균표 = df.groupby("SNS사용구간")[
    ["수면시간", "학업성취도", "신체활동량", "스트레스수준"]
].mean().round(2)

# ─────────────────────────────────────────────
# 1. 막대그래프 - 지표 하나씩 비교
# ─────────────────────────────────────────────
st.header("📊 막대그래프로 비교하기")

지표선택 = st.selectbox(
    "비교할 지표를 선택하세요",
    ["수면시간", "학업성취도", "신체활동량", "스트레스수준"]
)

st.subheader(f"SNS 사용 구간별 평균 {지표선택}")
st.bar_chart(평균표[지표선택])

# ─────────────────────────────────────────────
# 2. 꺾은선 그래프 - 4가지 지표 한눈에 비교
# ─────────────────────────────────────────────
st.header("📈 꺾은선 그래프로 한눈에 비교하기")
st.write("SNS 사용 시간이 늘어날수록 각 지표가 어떻게 변하는지 살펴보세요.")
st.line_chart(평균표)

# ─────────────────────────────────────────────
# 3. 평균값 표로 정리
# ─────────────────────────────────────────────
st.header("📑 구간별 평균값 표")
st.dataframe(평균표, use_container_width=True)

# ─────────────────────────────────────────────
# 탐구 도우미
# ─────────────────────────────────────────────
st.info(
    "💡 그래프를 보고 생각해 보세요!\n\n"
    "- SNS 사용이 늘면 '수면시간'은 어떻게 변하나요?\n"
    "- '스트레스수준'은 어떤 경향을 보이나요?\n"
    "- 예상과 다른 결과가 있다면 그 이유는 무엇일까요?"
)
