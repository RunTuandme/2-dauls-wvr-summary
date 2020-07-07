<center>

# 双通道水汽辐射计评估

</center>

------

摘要：？？


<center>

## 原理部分

</center>

大气微波辐射方程，
<center>

$
\displaystyle{T_B = T_Se^{-\tau_{\infty}}+\int_0^{\infty}T\alpha e^{-\tau}ds}
$
</center>

大气吸收系数$\alpha$,
<center>

$
\alpha = \alpha_v + \alpha_o + \alpha_l
$
</center>

$\alpha_w$为水汽吸收系数，$\alpha_o$为氧气吸收系数，$\alpha_l$为液态水吸收系数。
<center>

$
\displaystyle\tau_{\infty}=\int_0^{\infty}\alpha ds
$

$
\displaystyle\tau=\int_0^s\alpha ds
$
</center>

由大气微波辐射方程可得到，
<center>

$
\tau = ln\left(\dfrac{T_m-T_s}{T_m-T_B}\right)
$
</center>

对于双通道水汽辐射计，假定通道频率为$f_1$、$f_2$，对应大气吸收系数分别为$\alpha_1$、$\alpha_2$，则对应的大气不透明度$\tau_1$、$\tau_2$可写为：
<center>

$
\displaystyle\tau_1=\int_0^{\infty}\alpha_1ds
$

$
\displaystyle\tau_2=\int_0^{\infty}\alpha_2ds
$
</center>

在40GHz频率以下，大多数云中液态水的吸收系数与频率的平方成近似正比的关系。根据这一关系可写出下列方程：

$$
\begin{aligned}
\displaystyle\dfrac{\tau_1}{f_1^2}-\dfrac{\tau_2}{f_2^2} & = \int_0^{\infty}\dfrac{\alpha_1}{f_1^2}ds-\int_0^{\infty}\dfrac{\alpha_2}{f_2^2}ds \\
& = \int_0^{\infty}w(s)\dfrac{\rho_v}{T}ds+\tau_d
\end{aligned}
$$
<center>

$
w(s)=\dfrac{T}{\rho_v}\left(\dfrac{\alpha_{v1}}{f_1^2}-\dfrac{\alpha_{v2}}{f_2^2}\right)
$

$
\displaystyle\tau_d=\int_0^{\infty}\left(\dfrac{\alpha_{o1}}{f_1^2}-\dfrac{\alpha_{o2}}{f_2^2}\right)ds+\int_0^{\infty}\left(\dfrac{\alpha_{l1}}{f_1^2}-\dfrac{\alpha_{l2}}{f_2^2}\right)ds
$
</center>

方程中，权函数$w(s)$在某些特定的频率对上可看作近似与高度无关的常数$W(s)$。则上述方程可改写成
<center>

$
\displaystyle\dfrac{\tau_1}{f_1^2}-\dfrac{\tau_2}{f_2^2}=W(s)\int_0^{\infty}\dfrac{\rho_v}{T}ds+\tau_d
$
</center>

已知由水汽引起的湿延迟$\Delta L_v$可由下式计算，
<center>

$
\displaystyle\Delta L_v = k\int_0^{\infty}\dfrac{\rho_v}{T}ds
$
</center>

其中，$k=1.763\times10^{-6}(K\cdot g^{-1}\cdot m^{-3})$。
则由以上两式可以得到，

<center>

$
\displaystyle\Delta L_v = k\int_0^{\infty}\dfrac{\rho_v}{T}ds=b_0+b_1\tau_1+b_2\tau_2
$
</center>

其中，
<center>

$b_0=-k\tau_d/W_m$

$b_1=k/f_1^2W_m$

$b_2=-k/f_2^2W_m$

$
W(s)=\dfrac{T}{\rho_v}\left(\dfrac{\alpha_{v1}}{f_1^2}-\dfrac{\alpha_{v2}}{f_2^2}\right)
$

$
\tau_1 = ln \left(\dfrac{T_m-T_s}{T_m-T_{B_1}}\right)
$

$
\tau_2 = ln \left(\dfrac{T_m-T_s}{T_m-T_{B_2}}\right)
$
</center>