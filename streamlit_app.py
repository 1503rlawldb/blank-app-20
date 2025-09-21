import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="물러서는 땅, 다가오는 바다",
    page_icon="🌊",
    layout="wide"
)

# --- 제목 및 소개 ---
st.title("🌊 해수면 상승 대시보드")
st.markdown("""
해수면 상승은 더 이상 먼 미래의 이야기가 아닙니다. 이 대시보드는 시간의 흐름에 따른 해수면 변화를 시각적으로 보여주고,
주요 피해 국가들의 현실과 대응 노력을 조명합니다. **좌측 사이드바**에서 연도와 지역을 선택하여 변화를 직접 확인해보세요.
""")
st.markdown("---")

# ----------------------------
# 데이터 생성 (시뮬레이션)
# ----------------------------
@st.cache_data
def generate_sea_level_data():
    """1880년부터 2025년까지의 해수면 상승 데이터를 시뮬레이션합니다."""
    years = np.arange(1880, 2026)
    # 시간이 지날수록 상승폭이 커지는 비선형적 증가를 시뮬레이션
    base_rise = 0.008 * (years - 1880)**2 + np.random.normal(0, 5, len(years))
    sea_level_mm = base_rise - base_rise[0]  # 시작점을 0으로 맞춤
    return pd.DataFrame({'Year': years, 'Sea Level Rise (mm)': sea_level_mm})

df_sea_level = generate_sea_level_data()

# ----------------------------
# 1. 좌측 조작 옵션
# ----------------------------
st.sidebar.header("⚙️ 보기 옵션")
selected_year = st.sidebar.slider("① 연도 선택", 1880, 2025, 2025)
selected_region = st.sidebar.selectbox("② 주요 피해 지역 선택", ["전 세계", "대한민국", "투발루", "몰디브", "방글라데시", "네덜란드"])

# ----------------------------
# 2. 전 세계 해수면 상승 현황
# ----------------------------
st.header(f"📈 {selected_year}년, 전 세계 해수면 상승 현황")

# 선택된 연도까지의 데이터 필터링
df_filtered_by_year = df_sea_level[df_sea_level['Year'] <= selected_year]

# 2-1. 주요 수치 표시
latest_data = df_filtered_by_year.iloc[-1]
ten_years_ago_data = df_sea_level[df_sea_level['Year'] == selected_year - 10]

current_level = latest_data['Sea Level Rise (mm)']
delta = None
if not ten_years_ago_data.empty:
    delta = current_level - ten_years_ago_data.iloc[0]['Sea Level Rise (mm)']

col1, col2, col3 = st.columns(3)
col1.metric(
    label=f"{selected_year}년 누적 상승량 (mm)",
    value=f"{current_level:.2f}",
    delta=f"{delta:.2f} (10년 전 대비)" if delta is not None else "데이터 없음",
    delta_color="inverse"
)
col2.metric(label="측정 기준 연도", value="1880년")
col3.metric(label="데이터", value="시뮬레이션")

# 2-2. 시간에 따른 변화 그래프
with st.container(border=True):
    st.subheader("연도별 누적 상승량 변화")
    fig = px.line(df_filtered_by_year, x='Year', y='Sea Level Rise (mm)',
                  labels={'Year': '연도', 'Sea Level Rise (mm)': '상승량 (mm)'})
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='#f0f2f6'
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ----------------------------
# 3. 나라별 피해 사례 / 대처 방안
# ----------------------------
case_study = {
    "투발루": {"피해": "해발고도가 매우 낮아 국토의 40% 이상이 만조 시 침수됩니다. 식수 오염, 농경지 파괴가 심각하며 주민들은 뉴질랜드 등으로 이주하고 있습니다. '디지털 국가'로의 전환을 선언하며 국제 사회에 기후 위기의 심각성을 알리고 있습니다.", "대처": "국제 사회에 기후 난민 보호 요청, 해안 방벽 설치, 국가 정보를 디지털로 보존하는 '미래의 국가' 프로젝트를 진행 중입니다."},
    "몰디브": {"피해": "1200여 개의 산호섬으로 이루어진 몰디브는 80% 이상이 해발 1m 미만입니다. 해수면이 1m 상승하면 국토 대부분이 사라질 위기에 처해 있으며, 관광 산업과 국민의 생존을 직접적으로 위협합니다.", "대처": "해상 부유 도시 '몰디브 플로팅 시티' 건설, 수도 말레 주변에 거대한 방파제 건설, 산호초 복원 사업 등을 통해 대응하고 있습니다."},
    "방글라데시": {"피해": "인구 밀도가 높은 갠지스강 삼각주에 위치하여, 해수면 상승과 강력해진 사이클론으로 인해 매년 대규모 홍수와 침수 피해를 겪고 있습니다. 수백만 명의 '기후 난민'이 발생하여 도시 빈민 문제로 이어지고 있습니다.", "대처": "홍수 예측 및 경보 시스템 고도화, 수천 km에 달하는 제방 건설 및 보강, 염분에 강한 농작물 품종 개발 등으로 적응 노력을 기울이고 있습니다."},
    "네덜란드": {"피해": "국토의 약 26%가 해수면보다 낮은 '포더(polder)' 지형으로, 역사적으로 물과의 싸움을 계속해왔습니다. 기후 변화로 인해 폭풍 해일의 위협이 더욱 커지고 있습니다.", "대처": "세계 최고 수준의 치수 시스템 '델타 프로젝트'와 '룸 포 더 리버(Room for the River)'를 통해 방조제, 댐, 수문을 통합 관리하며 자연과 공존하는 방식을 채택하고 있습니다."},
    "대한민국": {"피해": "서해안과 남해안의 해수면 상승률이 세계 평균보다 높게 나타나고 있습니다. 인천, 부산 등 주요 항구 도시와 해안 저지대의 침수 위험이 증가하고 있으며, 백사장 유실과 갯벌 생태계 파괴가 우려됩니다.", "대처": "연안관리 기본계획 수립, 방재 시설(방파제, 배수펌프장) 확충, 연안 침식 모니터링 강화, 친환경 해안 복원 사업 등을 추진하고 있습니다."}
}

if selected_region != "전 세계":
    st.header(f"📍 {selected_region} 상세 정보")
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.error("피해 사례")
            st.write(case_study[selected_region]['피해'])
        with col2:
            st.success("대처 방안")
            st.write(case_study[selected_region]['대처'])
    st.markdown("---")


# ----------------------------
# 4. 지도 시각화 (위험 지역 시뮬레이션)
# ----------------------------
st.header(f"🌍 {selected_year}년, 지구 온난화 위험 지역")

@st.cache_data
def generate_map_points(year):
    """연도에 따라 위험 지역 포인트 수를 조절하여 시각적 변화를 줍니다."""
    base_points = 50
    # 연도가 높아질수록 포인트 수가 기하급수적으로 늘어나도록 설정
    num_points = int(base_points + ((year - 1880) / (2025 - 1880))**2 * 1500)
    df_map = pd.DataFrame({
        "lat": np.random.normal(20, 30, num_points),
        "lon": np.random.normal(0, 60, num_points),
    })
    return df_map

map_data = generate_map_points(selected_year)
st.map(map_data, zoom=1)
st.caption("이 지도는 실제 데이터가 아닌, 연도에 따른 지구 온난화 심화 경향을 보여주기 위한 시뮬레이션입니다. 점의 밀도가 위험도를 상징합니다.")
st.markdown("---")

# ----------------------------
# 5. 성찰과 행동
# ----------------------------
with st.container(border=True):
    st.subheader("📝 성찰: 나는 얼마나 알고 있을까?")
    st.checkbox("해수면 상승이 나와 내 주변의 삶에 직접적인 영향을 줄 수 있다고 생각한다.", key="q1")
    st.checkbox("해수면 상승 문제 해결은 정부와 국제 사회의 노력만으로는 부족하다고 생각한다.", key="q2")
    st.checkbox("에너지 절약, 쓰레기 줄이기 등 기후 변화를 늦추기 위한 개인적인 행동에 참여할 의향이 있다.", key="q3")

# ----------------------------
# 6. 출처
# ----------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("#### 📚 데이터 및 정보 출처")
st.sidebar.markdown("""
- **해수면 데이터:** NASA, NOAA 등에서 제공하는 데이터를 기반으로 시뮬레이션 생성
- **참고 자료:** [IPCC Reports](https://www.ipcc.ch/), [NASA Climate Change](https://climate.nasa.gov/), [NOAA Sea Level Rise](https://coast.noaa.gov/slr/)
""")

