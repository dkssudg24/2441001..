import streamlit as st

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
mport streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

st.title("합성함수 불연속점 시각화 앱")
st.write("수렴/발산 불연속이 있는 함수 f(x), g(x)를 입력하면 합성함수의 불연속점을 찾아 시각화합니다.")

# 함수 입력
f_expr = st.text_input("f(x) 입력 (예: 1/x, tan(x), abs(x-2))", "1/x")
g_expr = st.text_input("g(x) 입력 (예: x, x+1, sin(x))", "x")

x = sp.symbols('x')
try:
    f = sp.sympify(f_expr)
    g = sp.sympify(g_expr)
    h = f.subs(x, g)
except Exception as e:
    st.error(f"수식 오류: {e}")
    st.stop()

# 수치화 함수
f_lambd = sp.lambdify(x, f, modules=['numpy'])
g_lambd = sp.lambdify(x, g, modules=['numpy'])
h_lambd = sp.lambdify(x, h, modules=['numpy'])

# x 범위 설정
X = np.linspace(-10, 10, 1000)
with np.errstate(divide='ignore', invalid='ignore'):
    Yf = f_lambd(X)
    Yg = g_lambd(X)
    Yh = h_lambd(X)

# 불연속점 탐지 (간단 예시: 값이 급격히 변하거나 nan/inf 발생)
def find_discontinuities(Y, X):
    disc_points = []
    for i in range(1, len(Y)):
        if np.isnan(Y[i]) or np.isinf(Y[i]):
            disc_points.append(X[i])
        elif np.abs(Y[i] - Y[i-1]) > 10:  # 임계값 조정 가능
            disc_points.append(X[i])
    return disc_points

disc_points = find_discontinuities(Yh, X)

# 그래프 그리기
fig, ax = plt.subplots()
ax.plot(X, Yh, label='h(x) = f(g(x))')
ax.plot(X, Yf, '--', label='f(x)')
ax.plot(X, Yg, '--', label='g(x)')
for pt in disc_points:
    ax.axvline(pt, color='red', linestyle=':', alpha=0.5)
ax.legend()
st.pyplot(fig)

# 불연속점 출력
if disc_points:
    st.write("불연속점(근사):", np.round(disc_points, 3))
else:
    st.write("불연속점이 감지되지 않았습니다.")

