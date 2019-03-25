import cv2
import os

# 在当前目录下新建文件夹
folder_path = "img_bear/"
os.makedirs(folder_path)
# 进行视频的载入
vc = cv2.VideoCapture('/Users/urugang/Downloads/Telegram Desktop/地狱厨房片头.mp4')
c = 0
# 判断载入的视频是否可以打开
ret = vc.isOpened()
# 循环读取视频帧
while ret:
    c = c + 1
    # 进行单张图片的读取,ret的值为True或者Flase,frame表示读入的图片
    ret, frame = vc.read()
    if ret:
        # 存储为图像
        cv2.imwrite('img_bear/' + str(c) + '.jpg', frame)
        # 输出图像名称
        print('img_bear/' + str(c) + '.jpg')
        # 在一个给定的时间内(单位ms)等待用户按键触发,1ms
        cv2.waitKey(1)
    else:
        break
# 视频释放
vc.release()

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

# 创建字符图片文件夹
folder_path = "bear/"
os.makedirs(folder_path)
for i in range(1, 1000):
    filename = 'img_bear/' + str(i) + '.jpg'
    # 字符列表
    ascii_char = list(
        "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~ <>i!lI;:,\"^`'. "
    )
    # 判断图片是否存在
    if os.path.exists(filename):
        # 将图片转化为灰度图像,并重设大小
        img_array = np.array(
            Image.open(filename).resize((70, 70),
                                        Image.ANTIALIAS).convert('L'))
        # 创建新的图片对象
        img = Image.new('L', (560, 560), 255)
        draw_object = ImageDraw.Draw(img)
        # 设置字体
        font = ImageFont.truetype('Courier New Bold', 10, encoding='unic')
        # 根据灰度值添加对应的字符
        for j in range(70):
            for k in range(70):
                x, y = k * 8, j * 8
                index = int(img_array[j][k] / 4)
                draw_object.text((x, y), ascii_char[index], font=font, fill=0)
        name = 'bear/' + str(i) + '.jpg'
        print(name)
        # 保存字符图片
        img.save(name, 'JPEG')

import cv2
import os

# 设置视频编码器,这里使用使用MJPG编码器
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
# 输出视频参数设置,包含视频文件名、编码器、帧率、视频宽高(此处参数需和字符图片大小一致)
videoWriter = cv2.VideoWriter('bear_character.avi', fourcc, 20.0, (560, 560))

for i in range(1, 1000):
    filename = 'bear/' + str(i) + '.jpg'
    # 判断图片是否存在
    if os.path.exists(filename):
        img = cv2.imread(filename=filename)
        # 在一个给定的时间内(单位ms)等待用户按键触发,100ms
        cv2.waitKey(100)
        # 将图片写入视频中
        videoWriter.write(img)
        print(str(i) + '.jpg' + ' done!')
# 视频释放
videoWriter.release()
