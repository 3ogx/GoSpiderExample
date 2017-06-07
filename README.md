# Golang 土拨鼠项目爬虫示例

这是一个示例的仓库，以前是用Python写爬虫，积累了一定经验后转成Golang，并发快，开发快，理解舒畅。

## 一.使用

1. 依赖[https://github.com/hunterhug/GoSpider](https://github.com/hunterhug/GoSpider)，请下载它到GOPATH
2. 示例仅供学习，爬虫有风险，如果太暴力，会给别人带来损失，在此申明不承担相应责任。

本文 约定 `助手==爬虫`！

下载：

```bash
go get -u -v github.com/hunterhug/GoSpiderExample
```

如果下载过慢，请手动下载，包依赖有问题，请将https://github.com/hunterhug/GoSpider/tree/master/vendor 下的包移动到GOPATH

## 二.Example

项目结构

```
-- doc 杂
-- jiandan 煎蛋文章爬虫
    --main 入口
-- jiandanmeizi 煎蛋图片爬虫
    --main.go 简单

-- pedaily 投资界爬虫
-- taobao 万能图片助手(天猫淘宝额外处理)
-- zhihu 知乎小助手
    --mian 入口
```

### 1. 万能图片助手

[taobao抓取淘宝天猫商品页图片|任意网址也可以](taobao/README.md)，万能图片助手！

写入taobao.csv：

```
https://detail.tmall.com/item.htm?id=523350171126&skuId=3120562159704,tmall
https://item.taobao.com/item.htm?id=40066362090,taobao
#https://item.taobao.com/item.htm?id=40066362090,taobao
```

链接分为两部分，前面是链接，后面是图片保存的目录名，`#`表示忽略这一个网站

跑起来，`-config`后面是`taobao.csv`的位置,如果在`/data/app`下，那么需`-config=/data/app/taobao.csv`， 相对路径时路径是相对于跑程序的地方

```
go run taobao.go -config=taobao.csv
taobao.exe -config=taobao.csv
```

### 2. 投资界助手

[pedaily.cn投资界爬虫](pedaily/README.md),投资专用!

```
搜索：http://zdb.pedaily.cn/company/w

深圳市创新投资集团有限公司  http://zdb.pedaily.cn/company/show3392/ <br/>
广东中科招商创业投资管理有限责任公司 http://zdb.pedaily.cn/company/show10932/<br/>
上海复星创富投资管理股份有限公司  http://zdb.pedaily.cn/company/show6807/<br/>
江苏毅达股权投资基金管理有限公司 http://zdb.pedaily.cn/company/show787/<br/>
盛世景资产管理集团股份有限公司 http://zdb.pedaily.cn/company/show1944/<br/>
朱雀股权投资管理股份有限公司 http://zdb.pedaily.cn/company/show7135/<br/>
浙商创投股份有限公司 http://zdb.pedaily.cn/company/show5998/<br/>
深圳同创伟业资产管理股份有限公司 http://zdb.pedaily.cn/company/show2723/

1. companysearch.go可通过关键字查找一家机构的简单信息
2. companytouzi.go可通过公司代号查找一家机构的投资情况
```

### 3. 淘宝天猫搜索框商品千里寻踪

[taobaoscrapy淘宝天猫搜索框商品千里寻踪待做](taobaoscrapy/README.md),重构[Python版本](https://github.com/hunterhug/taobaoscrapy)可选抓取图片并保存信息到csv

### 4. 分布式煎蛋文章助手

[jiandan煎蛋项目爬文章](jiandan/README.md)

多浏览器持久化cookie分布式爬虫爬取数据，使用到redis，mysql，将网页数据保存在磁盘中，详情页解析后存入数据库。中级示例！

结果，总共抓取了56,961 篇文章

```
1. cont.go编辑配置，`RootDir = "E:\\jiandan"`为数据目录
2. 进main文件夹运行
3. 数据保存在data和数据库中
4. 重抓要删除Redis数据库和文件夹
```

详细 说明见[http://www.lenggirl.com/spider/jiandan.html](http://www.lenggirl.com/spider/jiandan.html)

### 5. 煎蛋妹纸/无聊图片助手

[jiandan煎蛋项目爬图片](jiandanmeizi/README.md)，啥Redis都不用，准备好网速就行！

### 6. 知乎小助手

[zhihu知乎系列爬虫](zhihu/README.md)啥啥都有。工具在[exe](https://github.com/hunterhug/GoSpiderExample/tree/master/zhihu/main)

示例 [防盗链版本HTML](http://www.lenggirl.com/zhihu/28467579-html/1.html)

cookie.txt请自带！

按问题ID抓答案，按收藏夹批量抓答案

```
	-----------------
	知乎问题信息小助手
	功能:
	1. 抓取图片
	2. 抓取答案

	选项:
	1. 从收藏夹https://www.zhihu.com/collection/78172986批量获取很多问题答案
	2. 从问题https://www.zhihu.com/question/28853910批量获取一个问题很多答案

	请您按提示操作（Enter）！答案保存在data文件夹下！

	如果失效了请往exe同级目录cookie.txt
	增加cookie

	你亲爱的萌萌~
	太阳萌飞了~~~
	-----------------
```

## 三.EXE下载

直接点击exe即可运行，exe工具下载见：[百度云盘](http://pan.baidu.com/s/1gfgi9YN)

```
ooxx.exe为爬取煎蛋妹纸图
wuliao.exe为爬取煎蛋无聊图

taobao.exe为爬取天猫淘宝等网址图片，需编辑taoban.csv

zhihu.exe为抓取知乎问题下的回答，包括图片
```

# Tip

如果你觉得项目帮助到你，欢迎请我喝杯咖啡

微信
![微信](https://raw.githubusercontent.com/hunterhug/hunterhug.github.io/master/static/jpg/wei.png)

支付宝
![支付宝](https://raw.githubusercontent.com/hunterhug/hunterhug.github.io/master/static/jpg/ali.png)

如果你需要定制版爬虫小工具，欢迎写好需求后，联系我！按开发时间收费(按天数/如程序员基本工资为每天300，则收取300)
