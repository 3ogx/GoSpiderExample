# 使用
结果，总共抓取了56,961 篇文章

1. cont.go编辑配置，`RootDir = "E:\\jiandan"`为数据目录
2. 进main文件夹运行
3. 数据保存在data和数据库中
4. 重抓要删除Redis数据库和文件夹

详细 说明见[http://www.lenggirl.com/spider/jiandan.html](http://www.lenggirl.com/spider/jiandan.html)

已经封装了exe，小心开车。

![](/doc/jiandan/redis.png)
![](/doc/jiandan/file.png)
![](/doc/jiandan/mysql.png)

```
/*
Copyright 2017 by GoSpider author.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License
*/
package main

import (
	//"fmt"
	"github.com/hunterhug/GoSpiderExample/jiandan"
	"os"
	"os/signal"
)

var Clear = false

func main() {
	if Clear {
		// Reids中Doing的迁移到Todo，需手动，var Clear = true
		go jiandan.Clear()
	} else {
		// 首页爬虫爬取
		go jiandan.IndexSpiderRun()

		// 详情页抓取
		go jiandan.DetailSpidersRun()
	}

	c := make(chan os.Signal)
	//监听指定信号
	signal.Notify(c, os.Interrupt)

	//阻塞直至有信号传入
	<-c
}

```