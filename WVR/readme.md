# WVR 反演亮温和湿延迟计算函数库

![](https://img.shields.io/badge/project-building-brightgreen) 
![](https://img.shields.io/badge/version-1.1.1-green)

---------------
# Code Structures

```
├── WVR
│  ├── kox                  ：计算氧气吸收系数
│  │  ├── C.py
│  │  ├── gamma.py
│  │  ├── gamma0.py
│  │  ├── P.py
│  │  ├── T.py
│  │  ├── TUS.py
│  │  └── kox.py
│  ├── e0.py                ：计算饱和水汽压
│  ├── kv.py                ：计算水汽吸收系数
├──└── tau.py               ：计算大气不透明度
```

---------------
# 详细公式

## 湿延迟
<center>

$
L_{v}=b_0+b_1\tau_1+b_2\tau_2 \left(km\right)
$
</center>

---------------
## 不透明度$\tau$
<center>

$
\tau=ln\left(\dfrac{T_m-T_c}{T_m-T_{sky}}\right)
$
</center>

---------------
## $T_m$
<center>

$
T_m=0.72\times T_0+70.2
$
</center>

---------------
## 系数$b_0$、$b_1$、$b_2$
<center>

$b_0=-K\tau_d/W_m$

$b_1=K/f_1^2W_m$

$b_2=-K/f_2^2W_m$
</center>

---------------
## $W_m$
<center>

$
W_m=\dfrac{T}{\rho_v}\left(\dfrac{\alpha_{wv1}}{f_1^2}-\dfrac{\alpha_{wv2}}{f_2^2}\right)
$
</center>

---------------
## $\tau_d$
<center>

$
\displaystyle{\tau_d=\int_0^\infty\left(\dfrac{\alpha_{ox1}}{f_1^2}-\dfrac{\alpha_{ox2}}{f_2^2}\right)ds}
$
</center>

---------------
## 吸收系数
<center>

$
\alpha\left(h_0,f\right)=\alpha_{ox}\left(h_0,f\right)+\alpha_{cloud}\left(h_0,f\right)+\alpha_{rain}\left(h_0,f\right)+\alpha_{wv}\left(h_0,f\right)
$
</center>

---------------
## $\alpha_{ox}$
<center>

$
\alpha_{ox}\left(h,f\right)=C(f)\gamma_0(h)f^2\left(\dfrac{P(h)}{1013}\right)^2\left(\dfrac{300}{T_p(h)}\right)^{2.85}\left(\dfrac{1}{(f-60)^2+\gamma(h)^2}+\dfrac{1}{f^2+\gamma(h)^2}\right)dB/km
$
</center>

---------------
## $\alpha_{cloud}$
<center>

$
\alpha_{cloud}(h,f)=\rho_{lwc}(h)f^{1.95}exp\left(1.5735-0.0309T_p(h)\right)
$
</center>

---------------
## $\alpha_{rain}$
<center>

$
\alpha_{rain}(h,f)=a_{rain}(f)r(h)^{b_{rain}(f)}
$
</center>

---------------
## $\gamma(h)$
<center>

$
\gamma(h)=\gamma_0(h)\left(\dfrac{P(h)}{1013}\right)\left(\dfrac{300}{T_p(h)}\right)^{0.85}
$
</center>

---------------
## $\gamma_0(h)$
<center>

$$
\gamma_0(h)=
\begin{cases}
0.59,& P(h)>333\\
0.59\left(1+0.0031\left(333-P(h)\right)\right),& 25<P(h)\leq333\\
1.18,& P(h)\leq25
\end{cases}
$$
</center>

---------------
## $C(f)$
<center>

$
C(f)=0.011\left(7.13\times10^{-7}f^4-9.2051\times10^{-5}f^3+3.280422\times10^{-3}f^2-0.01906468f+1.110303146\right)
$
</center>

---------------
## $P(h)$
<center>

$
P(h)=P_{h_0}exp\left(\dfrac{8.387(h_0-h)}{\left(8.387-0.0887h_0\right)\left(8.387-0.0887h\right)}\right)
$
</center>

---------------
## $T_p(h)$
<center>

$$
T_p(h)=
\begin{cases}
T_{h_0}+\dfrac{h-h_0}{2}\left(T_{US}\left(h_0+2\right)-T_{h_0}\right),& h_0\leq h\leq h_0+2\\
T_{US}(h),& h_0+2<h\leq 20\\
217,& 20<h\leq30
\end{cases}
$$
</center>

---------------
## $T_{US}(h)$
<center>

$$
T_{US}(h)=
\begin{cases}
288.16-6.5h,& 288.16-6.5h>277\\
217,& 288.16-6.5h\leq277,h<20\\
197+h,& otherwise
\end{cases}
$$
