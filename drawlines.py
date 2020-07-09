from WVR.Kox.kox import kox
from WVR.kv import kv

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

v = np.linspace(10, 100, 800)
p = 1013
p_v = 7.5*293/217
T = 300
h0 = 0
k_v = []
k_o = []

for i in v:
    k_v.append(kv(T,i,p,p_v))
    k_o.append(kox(i,h0,h0,T,p))

k_v = np.array(k_v)
k_o = np.array(k_o)
    
#plt.plot(v, k_v , label="水汽吸收系数曲线")
plt.plot(v, k_o , label="氧气吸收系数曲线")
plt.xlabel('频率（GHz）',fontsize=13)
#plt.ylabel(r'水汽吸收系数（km$^{-1}\times10^{-2}$）',fontsize=13)
plt.title('van Vleck-Weisskopf模型水汽吸收系数曲线',fontsize=17)
#plt.text(27.3,1.0,s=r'气温：$277.05K$')
#plt.text(27.3,0.93,r'压强：1037.6hPa')
#plt.text(27.3,0.86,r'水汽压：3.228hPa')
#plt.ylim(0,1.3)
#plt.vlines(22.23510,0,1.3,linestyles=':')
#plt.vlines(22.6097,0,1.3,linestyles='--',colors='#DDA0DD')
plt.legend(fontsize=13)
#plt.annotate(r'$v_0$',xy=(22.23510,1),xytext=(20.16,1.1),arrowprops=dict(arrowstyle="->",connectionstyle="arc3"))
#plt.annotate(r'$\'{v_0}$',xy=(22.6097,0.48),xytext=(23.78,0.6),arrowprops=dict(arrowstyle="->",connectionstyle="arc3"))

#plt.savefig('image/kv.png',dpi=1500)
plt.show()