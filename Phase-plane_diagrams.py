import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# 定义动力系统
def system(y, t):
    eta, nu = y  # 状态变量
    d_eta = nu  # \dot{\eta} = \nu
    d_nu = - 0.02 * (1 + nu**2) * nu - (0.95 + 0.018 * eta**2) * eta  # 修正后的方程
    return [d_eta, d_nu]

# 时间范围
t = np.linspace(0, 100, 2000)  # 时间范围从 0 到 100，增加时间点的数量

# 创建网格边缘的初始条件
eta_vals = np.linspace(-10, 10, 15)  # eta 网格
nu_vals = np.linspace(-10, 10, 15)  # nu 网格
initial_conditions = []

# 取网格边缘点（上下边界和左右边界）
for eta0 in eta_vals:
    initial_conditions.append([eta0, -10])  # 下边界
    initial_conditions.append([eta0, 10])   # 上边界
for nu0 in nu_vals:
    initial_conditions.append([-10, nu0])  # 左边界
    initial_conditions.append([10, nu0])   # 右边界

# 绘制相空间轨迹
plt.figure(figsize=(8, 6))

for eta0, nu0 in initial_conditions:
    sol = odeint(system, [eta0, nu0], t)
    plt.plot(sol[:, 0], sol[:, 1], 'r-', alpha=0.6)

# 设置图像参数
plt.xlabel(r'$\eta$')
plt.ylabel(r'$\nu$')
plt.title('Phase Plane with Initial Conditions on Grid Edges')
plt.xlim([-10, 10])  # 横坐标范围调整为 -10 到 10
plt.ylim([-10, 10])  # 纵坐标范围调整为 -10 到 10
plt.grid()
plt.show()
