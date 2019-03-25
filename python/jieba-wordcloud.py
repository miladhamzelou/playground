#coding:utf-8
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['STFangsong']  #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  #用来正常显示负号
#有中文出现的情况，需要u'内容'</code></pre></div>

# pip3 install WordCloud
# pip3 install jieba

fangsong  = list(filter(lambda i: i.name=="STFangsong", matplotlib.font_manager.fontManager.ttflist))
from wordcloud import WordCloud

f = open(
    u'/Users/urugang/Downloads/Telegram Desktop/司徒雷登在华五十年（全译本）.txt',
    'r',
    encoding='gbk').read()

wordcloud = WordCloud(
    background_color="white", width=1000, height=860, margin=2,
    font_path=fangsong[0].fname
).generate(f)

# width,height,margin可以设置图片属性

# generate 可以对全部文本进行自动分词,但是他对中文支持不好,对中文的分词处理请看我的下一篇文章
#wordcloud = WordCloud(font_path = r'D:\Fonts\simkai.ttf').generate(f)
# 你可以通过font_path参数来设置字体集

#background_color参数为设置背景颜色,默认颜色为黑色

plt.imshow(wordcloud)
plt.axis("off")
plt.show()

wordcloud.to_file('test.png')
