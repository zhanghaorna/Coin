import re
from pyquery import PyQuery as pq

pkgPattern = re.compile(r'<li appid=\".*?\" pkg=\"(.*?)\">')


str = '<ul class="list clearfix"><li appid="157674" pkg="com.mt.mtxx.mtxx"><a href="http://zhushou.sogou.com/apps/detail/157674.html" title="&lt;em&gt;美图秀&lt;/em&gt;&lt;em&gt;秀&lt;/em&gt;"></li>'
html = pq(str)

print(html('li').attr('pkg'))

