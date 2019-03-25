import matplotlib.pyplot as plt
import pylab
import numpy as np
import cv2

x = np.array([1, 2, 3])
h = np.array([4, 5, 6])
import scipy.signal
scipy.signal.convolve(x, h)  #卷积运算 array([ 4, 13, 28, 27, 18])

################################################################################
from scipy import signal
sig = np.random.randn(1000)  #生成随机数
autocorr = signal.fftconvolve(sig, sig[::-1], mode='full')  #fft算法实现卷积
fig, (ax_orig, ax_mag) = plt.subplots(2, 1)  #建立两行一列图形
ax_orig.plot(
    sig
)  #在第一行把原始的随机数序列sig画出来 [<matplotlib.lines.Line2D object at 0x0000000006E1DC88>]
ax_orig.set_title(
    'White noise'
)  #设置标题'白噪声' <matplotlib.text.Text object at 0x0000000006931860>
ax_mag.plot(
    np.arange(-len(sig) + 1, len(sig)),
    autocorr)  #卷积后的图像 [<matplotlib.lines.Line2D object at 0x0000000006E1DB00>]
ax_mag.set_title('Autocorrelation'
                 )  #设置标题 <matplotlib.text.Text object at 0x0000000006DFE8D0>
fig.tight_layout()  #此句可以防止图像重叠
fig.show()  #显示图像

################################################################################
import numpy as np
from scipy import signal
from scipy import misc
import matplotlib.pyplot as plt
face=misc.face(gray=True) #创建一个灰度图像
scharr=np.array([[-3-3j,0-10j,+3-3j],
        [-10+0j,0+0j,+10+0j],
         [-3+3j,0+10j,+3+3j]]) #设置一个特殊的卷积和
grad=signal.convolve2d(face,scharr,boundary='symm',mode='same') #把图像的face数组和设计好的卷积和作二维卷积运算,设计边界处理方式为symm
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10,6)) #建立1行2列的图fig
ax1.imshow(face,cmap='gray') #显示原始的图
ax1.set_axis_off() #不显示坐标轴
ax2.imshow(np.absolute(grad),cmap='gray') #显示卷积后的图
ax2.set_axis_off() #不显示坐标轴
fig.show() #显示绘制好的画布
################################################################################
img = plt.imread("3.jpg")  #在这里读取图片
plt.imshow(img)  #显示读取的图片
pylab.show()

fil = np.array([
    [-1, -1, 0],  #这个是设置的滤波，也就是卷积核
    [-1, 0, 1],
    [0, 1, 1]
])

res = cv2.filter2D(img, -1, fil)  #使用opencv的卷积函数

plt.imshow(res)  #显示卷积后的图片
pylab.show()


def convolve(img, fil, mode='same'):  #分别提取三个通道
    if mode == 'fill':
        h = fil.shape[0] // 2
        w = fil.shape[1] // 2
        img = np.pad(img, ((h, h), (w, w), (0, 0)), 'constant')
    conv_b = _convolve(img[:, :, 0], fil)  #然后去进行卷积操作
    conv_g = _convolve(img[:, :, 1], fil)
    conv_r = _convolve(img[:, :, 2], fil)

    dstack = np.dstack([conv_b, conv_g, conv_r])  #将卷积后的三个通道合并
    return dstack  #返回卷积后的结果


def _convolve(img, fil):
    fil_heigh = fil.shape[0]  #获取卷积核(滤波)的高度
    fil_width = fil.shape[1]  #获取卷积核(滤波)的宽度
    conv_heigh = img.shape[0] - fil.shape[0] + 1  #确定卷积结果的大小
    conv_width = img.shape[1] - fil.shape[1] + 1

    conv = np.zeros((conv_heigh, conv_width), dtype='uint8')

    for i in range(conv_heigh):
        for j in range(conv_width):  #逐点相乘并求和得到每一个点
            conv[i][j] = wise_element_sum(
                img[i:i + fil_heigh, j:j + fil_width], fil)
    return conv


def wise_element_sum(img, fil):
    res = (img * fil).sum()
    if (res < 0):
        res = 0
    elif res > 255:
        res = 255
    return res


img = plt.imread("3.jpg")  #在这里读取图片

# plt.imshow(img)  #显示读取的图片
# pylab.show()

#卷积核应该是奇数行，奇数列的
fil = np.zeros((5, 5))
fil[2][0] = -1
fil[2][1] = -1
fil[2][2] = 2.2

res = convolve(img, fil, 'fill')
print("img shape :" + str(img.shape))
plt.imshow(res)  #显示卷积后的图片
print("res shape :" + str(res.shape))
plt.imsave("res.jpg", res)
pylab.show()
