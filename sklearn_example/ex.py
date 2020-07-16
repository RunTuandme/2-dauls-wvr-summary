import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# 房屋面积、房间数
x_data = np.array(
    [[100, 4],
     [ 50, 1],
     [100, 4],
     [100, 3],
     [ 50, 2],
     [ 80, 2],
     [ 75, 3],
     [ 65, 4],
     [ 90, 3],
     [ 90, 2]])
# 房屋价格（单位是百万）
y_data = np.array([9.3, 4.8, 8.9, 6.5, 4.2, 6.2, 7.4, 6.0,  7.6, 6.1])

# 建立模型
model = LinearRegression()
# 开始训练
model.fit(x_data, y_data)

# 斜率
print("coefficients: ", model.coef_)
w1 = model.coef_[0]
w2 = model.coef_[1]

# 截距
print("intercept: ", model.intercept_)
b = model.intercept_

# 测试
x_test = [[90, 3]]
predict = model.predict(x_test)
print("predict: ", predict)

# 评估
print('Mean squared error: %.3f' % mean_squared_error(y_data, model.predict(x_data)))
##((y_test-LR.predict(X_test))**2).mean()
print('score: %.3f' % model.score(x_data, y_data))  
##r2 R平方


""" ax = plt.figure().add_subplot(111, projection = "3d")
ax.scatter(x_data[:, 0], x_data[:, 1], y_data, c = "b", marker = 'o', s = 10)
x0 = x_data[:, 0]
x1 = x_data[:, 1]
x0, x1 = np.meshgrid(x0, x1)
z = b + w1 * x0 + w2 * x1
ax.plot_surface(x0, x1, z, color = "r")
ax.set_xlabel("area")
ax.set_ylabel("num_rooms")
ax.set_zlabel("price")
plt.show() """

