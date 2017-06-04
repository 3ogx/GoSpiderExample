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
package zhihu

import (
	"fmt"
	"github.com/hunterhug/GoSpider/util"
	"path/filepath"
	"strings"
	"testing"
)

func TestCatchCoolection(t *testing.T) {
	cookie := `aliyungf_tc=AQAAAHsIEAws7QEA6VFYcdFnfcDSvkYb; acw_tc=AQAAAPw9qzSJdgIA6VFYceeh8SW9JGq4; l_n_c=1; q_c1=902510c4493740aca0c12964714d21a9|1496466243000|1496466243000; r_cap_id="ODlkYTE2NTRlNTU1NGE2ODk4NzdlMTAzODFjNTYwNGI=|1496466243|c8acb6ce3c484978a58bb35b65786c51dd89c3a1"; cap_id="ZmViMmNjZDc5NDFkNGU3ZWEwYTU5YzJlY2Q3ZTNmOGQ=|1496466243|86f02cc2355f0884db04e99b74be3e1b42e8dc83"; _xsrf=d43b7403d53a4da0482e61d87d74dba2; d_c0="AJACQuYp2wuPTgukFS3cyRKIs-9xlHIj7yo=|1496466385"; _zap=21c848aa-1c3f-4ce4-ac2d-6368660733ef; __utma=51854390.1073516356.1496466378.1496466378.1496466378.1; __utmb=51854390.0.10.1496466378; __utmc=51854390; __utmz=51854390.1496466378.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.000--|2=registration_date=20150209=1^3=entry_date=20170603=1; z_c0=Mi4wQUJEQk9vSjVtd2NBa0FKQzVpbmJDeGNBQUFCaEFsVk5sZEZaV1FDZUYzdVhyanFRSkxnb2Zyc3V4enNMcVVzNXlR|1496466904|8721b94a4dd67e3754d90074c14fc2ba72e26d1a`
	Baba.SetHeaderParm("Cookie", strings.TrimSpace(cookie))
	b, e := CatchCoolection(78172986, 500)
	if e != nil {
		fmt.Println(e.Error())
	} else {
		util.SaveToFile(filepath.Join(util.CurDir(), "../data/collection.html"), []byte(b))
	}
}

func TestParseCollection(t *testing.T) {
	body, err := util.ReadfromFile(filepath.Join(util.CurDir(), "../data/collection.html"))
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%#v.", ParseCollection(body))

}

func TestCatchAllCollection(t *testing.T) {
	fmt.Printf("%#v,", CatchAllCollection(78172986))
}
