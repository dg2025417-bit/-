import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────
# 페이지 기본 설정
# ─────────────────────────────────────────────
st.set_page_config(page_title="청소년 SNS와 정신건강", layout="wide")
st.title("📱 하루 SNS 사용량과 학생 생활 지표 비교")
st.write("당곡고등학교 데이터 탐구 - 4가지 지표를 각각 따로 비교해 봅니다.")

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

# 그래프 종류 선택
st.write("---")
그래프종류 = st.radio(
    "보고 싶은 그래프 종류를 선택하세요",
    ["막대그래프", "꺾은선 그래프"],
    horizontal=True
)
st.write("---")

# ─────────────────────────────────────────────
# 그래프를 그려주는 함수
# ─────────────────────────────────────────────
def 그래프그리기(지표이름):
    if 그래프종류 == "막대그래프":
        st.bar_chart(평균표[지표이름])
    else:
        st.line_chart(평균표[지표이름])

# ─────────────────────────────────────────────
# 4가지 지표를 각각 따로 그리기 (2칸 x 2줄)
# ─────────────────────────────────────────────
st.header("📊 SNS 사용 구간별 지표 비교 (각각 따로)")

# 첫 번째 줄: 수면시간 / 학업성취도
줄1 = st.columns(2)
with 줄1[0]:
    st.subheader("😴 수면시간")
    그래프그리기("수면시간")
with 줄1[1]:
    st.subheader("📚 학업성취도")
    그래프그리기("학업성취도")

# 두 번째 줄: 신체활동량 / 스트레스수준
줄2 = st.columns(2)
with 줄2[0]:
    st.subheader("🏃 신체활동량")
    그래프그리기("신체활동량")
with 줄2[1]:
    st.subheader("😣 스트레스수준")
    그래프그리기("스트레스수준")

# ─────────────────────────────────────────────
# 평균값 표로 정리
# ─────────────────────────────────────────────
st.header("📑 구간별 평균값 표")
st.dataframe(평균표, use_container_width=True)

# ─────────────────────────────────────────────
# 탐구 도우미
# ─────────────────────────────────────────────
st.info(
    "💡 그래프를 보고 생각해 보세요!\n\n"
    "- SNS 사용이 늘면 '수면시간'은 줄어드나요?\n"
    "- '스트레스수준'은 늘어나는 경향이 있나요?\n"
    "- 네 가지 지표 중 가장 뚜렷하게 변하는 것은 무엇인가요?"
)
