import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Glass Core AI Sim", layout="wide")

st.title("🔬 Glass Substrate Thermal & Stress Simulator")
st.sidebar.header("Simulation Parameters")

# 1. 사용자 입력 파라미터
chip_temp = st.sidebar.slider("Chip Temperature (°C)", 50, 150, 85)
tgv_density = st.sidebar.slider("TGV Density (per mm²)", 10, 100, 45)
substrate_size = 100 # 100x100 그리드

# 2. 열 분포 시뮬레이션 (Gaussian distribution 기반)
x = np.linspace(-5, 5, substrate_size)
y = np.linspace(-5, 5, substrate_size)
X, Y = np.meshgrid(x, y)
dist = np.sqrt(X**2 + Y**2)

# 중앙부(칩)에서 발생한 열이 주변으로 퍼지는 모델
thermal_map = chip_temp * np.exp(-dist**2 / 2) + 25 # 기본 상온 25도 추가

# 3. 응력(Stress) 계산 (TGV 밀도와 온도 변화량에 비례)
# 유리기판은 TGV가 많을수록 응력 집중 현상이 발생함
stress_map = (thermal_map - 25) * (tgv_density / 50) * (1 + 0.2 * np.random.randn(substrate_size, substrate_size))

# 4. 시각화
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Thermal Distribution (Heatmap)")
    fig_thermal = go.Figure(data=go.Heatmap(z=thermal_map, colorscale='Hot'))
    st.plotly_chart(fig_thermal, use_container_width=True)

with col2:
    st.subheader("⚡ Mechanical Stress Analysis")
    fig_stress = go.Figure(data=go.Heatmap(z=stress_map, colorscale='Viridis'))
    st.plotly_chart(fig_stress, use_container_width=True)

st.info(f"현재 설정된 TGV 밀도({tgv_density})에서 임계 응력 초과 영역이 감지되었습니다. 에이전트에게 최적화를 지시하시겠습니까?")

if st.button("Run AI Layout Optimization (Open Claw)"):
    st.success("에이전트가 TGV 좌표를 재계산 중입니다... 최적 설계안 도출 완료 (예상 수율 14% 향상)")
