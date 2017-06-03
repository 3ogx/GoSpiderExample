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
	"fmt"
	"github.com/hunterhug/GoSpider/util"
	"github.com/hunterhug/GoSpiderExample/zhihu"
	"strings"
)

// 抓取一个问题的全部信息

func help() {
	fmt.Println(`
	-----------------
	知乎问题信息小助手
	功能:
	1. 抓取图片
	2. 抓取答案

	您需要登录，并且
	请您按提示操作（Enter）！

	你亲爱的萌萌~
	太阳萌飞了~~~
	-----------------
	`)
}
func main() {
	help()
	u := zhihu.Input("请输入手机/邮箱:", "569929309@qq.com")
	p := zhihu.Input("请输入密码:", "t13112502886")
	body, err := zhihu.Login(u, p)
	if err != nil {
		panic(err.Error())
	}
	if strings.Contains(string(body), "验证") {
		fmt.Println(string(body))
		cookie := zhihu.Input("知乎药丸233,请您手工登录并且输入cookie:", `aliyungf_tc=AQAAAHsIEAws7QEA6VFYcdFnfcDSvkYb; acw_tc=AQAAAPw9qzSJdgIA6VFYceeh8SW9JGq4; l_n_c=1; q_c1=902510c4493740aca0c12964714d21a9|1496466243000|1496466243000; r_cap_id="ODlkYTE2NTRlNTU1NGE2ODk4NzdlMTAzODFjNTYwNGI=|1496466243|c8acb6ce3c484978a58bb35b65786c51dd89c3a1"; cap_id="ZmViMmNjZDc5NDFkNGU3ZWEwYTU5YzJlY2Q3ZTNmOGQ=|1496466243|86f02cc2355f0884db04e99b74be3e1b42e8dc83"; _xsrf=d43b7403d53a4da0482e61d87d74dba2; d_c0="AJACQuYp2wuPTgukFS3cyRKIs-9xlHIj7yo=|1496466385"; _zap=21c848aa-1c3f-4ce4-ac2d-6368660733ef; __utma=51854390.1073516356.1496466378.1496466378.1496466378.1; __utmb=51854390.0.10.1496466378; __utmc=51854390; __utmz=51854390.1496466378.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.000--|2=registration_date=20150209=1^3=entry_date=20170603=1; z_c0=Mi4wQUJEQk9vSjVtd2NBa0FKQzVpbmJDeGNBQUFCaEFsVk5sZEZaV1FDZUYzdVhyanFRSkxnb2Zyc3V4enNMcVVzNXlR|1496466904|8721b94a4dd67e3754d90074c14fc2ba72e26d1a`)
		zhihu.Baba.SetHeaderParm("Cookie", cookie)
	} else {
		fmt.Println(string(body))
	}

	Base()

}

func Base() {
	for {
		page := 1
		id := zhihu.Input("请输入问题ID:", "28467579")
		q := zhihu.Q(id)
		//fmt.Println(q)

		// 第一个答案
		body, err := zhihu.CatchA(q, page)
		fmt.Println("抓取第一个回答！")
		if err != nil {
			fmt.Println(err.Error())
			continue
		}

		temp, err := zhihu.StructA(body)
		if err != nil {
			fmt.Println(err.Error())
			continue
		}
		if len(temp.Data) == 0 {
			fmt.Println("没有答案！")
			continue
		}

		fmt.Println("开始处理答案:" + temp.Data[0].Excerpt)
		qid, aid, who, html := zhihu.OutputHtml(temp.Data[0])
		filename := fmt.Sprintf("data/%d/%s-%d/%s-%d的回答.html", qid, who, aid, who, aid)
		util.MakeDirByFile(filename)

		err = util.SaveToFile(filename, []byte(html))
		if err == nil {
			fmt.Println("保存答案成功:" + filename)
		} else {
			fmt.Println("保存答案失败:" + err.Error())
			continue
		}
		zhihu.SavePicture(fmt.Sprintf("data/%d/%s-%d", qid, who, aid), []byte(html))

		for {
			if temp.Page.IsEnd {
				fmt.Println("回答已经结束！")
				break
			}
			yes := zhihu.Input("抓取下一个答案，默认Y(Y/N)", "Y")
			if strings.Contains(yes, "N") {
				break
			}
			//fmt.Println(temp.Page.NextUrl)
			body, err = zhihu.CatchA(q, page+1)
			if err != nil {
				fmt.Println("抓取答案失败：" + err.Error())
				continue
			} else {
				page = page + 1
			}
			//util.SaveToFile("data/question.json", body)

			temp1, err := zhihu.StructA(body)
			if err != nil {
				fmt.Println(err.Error())
				continue
			}
			if len(temp1.Data) == 0 {
				fmt.Println("没有答案！")
				s, _ := util.JsonBack(body)
				fmt.Println(string(s))
				continue
			}

			// 成功后再来
			temp = temp1

			fmt.Println("开始处理答案:" + temp.Data[0].Excerpt)
			qid, aid, who, html := zhihu.OutputHtml(temp.Data[0])
			filename := fmt.Sprintf("data/%d/%s-%d/%s-%d的回答.html", qid, who, aid, who, aid)
			util.MakeDirByFile(filename)

			err = util.SaveToFile(filename, []byte(html))
			if err == nil {
				fmt.Println("保存答案成功:" + filename)
			} else {
				fmt.Println("保存答案失败:", err.Error())
				continue
			}
			zhihu.SavePicture(fmt.Sprintf("data/%d/%s-%d", qid, who, aid), []byte(html))
		}
	}
}
