#coding:utf-8
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['STFangsong']#用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
#有中文出现的情况，需要u'内容'</code></pre></div>
a = sorted([f.name for f in matplotlib.font_manager.fontManager.ttflist])
for i in a:
    print(i)

fangsong  = list(filter(lambda i: i.name=="STFangsong", matplotlib.font_manager.fontManager.ttflist))
print("{}: {}".format(fangsong[0].name, fangsong[0].fname))
plt.plot((1,2,3),(4,3,-1))
plt.xlabel(u'横坐标')
plt.ylabel(u'纵坐标')
plt.show()
