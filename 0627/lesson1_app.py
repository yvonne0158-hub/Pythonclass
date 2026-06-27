import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ========== 中文字型設定 ==========
# Windows 使用 'Microsoft JhengHei'（微軟正黑體）
# macOS 可使用 'Arial Unicode MS' 或 'Heiti TC'
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False   # 避免負號顯示為方塊

# ========== 建立圖表 ==========
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.30)  # 預留下方空間給滑桿

# X 軸：0 到 4π，共 1000 個點
x = np.linspace(0, 4 * np.pi, 1000)

# 初始參數
A_init = 1.0       # 振幅
omega_init = 1.0   # 頻率
phi_init = 0.0     # 相位偏移

# 繪製兩條曲線
sin_curve, = ax.plot(x, A_init * np.sin(omega_init * x + phi_init),
                     label='y = A·sin(ωx + φ)', color='#1f77b4')
cos_curve, = ax.plot(x, A_init * np.cos(omega_init * x + phi_init),
                     label='y = A·cos(ωx + φ)', color='#ff7f0e')

# 圖表外觀設定
ax.set_xlim(0, 4 * np.pi)
ax.set_ylim(-5.5, 5.5)
ax.set_title('正弦（sin）與餘弦（cos）波形', fontsize=14)
ax.set_xlabel('x（弧度）', fontsize=12)
ax.set_ylabel('y', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(loc='upper right')

# ========== 建立三個滑桿 ==========

# 1. 振幅滑桿
ax_slider_amp = plt.axes([0.20, 0.20, 0.60, 0.03])
slider_amp = Slider(
    ax_slider_amp, '振幅 A', 0.1, 5.0,
    valinit=A_init, valfmt='%.1f'
)

# 2. 頻率滑桿
ax_slider_omega = plt.axes([0.20, 0.13, 0.60, 0.03])
slider_omega = Slider(
    ax_slider_omega, '頻率 ω', 0.1, 10.0,
    valinit=omega_init, valfmt='%.1f'
)

# 3. 相位偏移滑桿
ax_slider_phi = plt.axes([0.20, 0.06, 0.60, 0.03])
slider_phi = Slider(
    ax_slider_phi, '相位偏移 φ', 0.0, 2 * np.pi,
    valinit=phi_init, valfmt='%.2f'
)


def update(val):
    """滑桿值變更時更新波形"""
    A = slider_amp.val
    omega = slider_omega.val
    phi = slider_phi.val

    # 重新計算 y 值
    sin_curve.set_ydata(A * np.sin(omega * x + phi))
    cos_curve.set_ydata(A * np.cos(omega * x + phi))

    # Y 軸範圍隨振幅自動調整
    ax.set_ylim(-A * 1.2, A * 1.2)

    fig.canvas.draw_idle()


# 將每個滑桿的變動事件綁定到更新函式
slider_amp.on_changed(update)
slider_omega.on_changed(update)
slider_phi.on_changed(update)

plt.show()
