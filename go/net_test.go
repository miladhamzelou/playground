package playground

import (
	"bufio"
	"compress/gzip"
	"fmt"
	"log"
	"net/http"
	"os"
	"regexp"
	"testing"
)

func TestNet(t *testing.T) {
	urls := []string{
		"http://www.toutiao.com/i6614608697882575367/?tt_from=weixin&utm_campaign=client_share&wxshare_count=2&from=singlemessage&timestamp=1541278985&app=news_article_lite&utm_source=weixin&iid=47956109968&utm_medium=toutiao_android&group_id=6614608697882575367&pbid=6615894279619495427",
		"https://www.toutiao.com/i6588744716605456899/?tt_from=weixin&utm_campaign=client_share&wxshare_count=1&timestamp=1541984097&app=news_article_lite&utm_source=weixin&iid=50377168296&utm_medium=toutiao_android&group_id=6588744716605456899",
		"https://www.toutiao.com/i6599951947556454915/?tt_from=weixin&utm_campaign=client_share&wxshare_count=1&timestamp=1541984241&app=news_article_lite&utm_source=weixin&iid=50377168296&utm_medium=toutiao_android&group_id=6599951947556454915",
		"https://www.toutiao.com/i6602380745975529987/?tt_from=weixin&utm_campaign=client_share&wxshare_count=1&timestamp=1541984318&app=news_article_lite&utm_source=weixin&iid=50377168296&utm_medium=toutiao_android&group_id=6602380745975529987",
		"https://www.toutiao.com/i6617954633316827655/?tt_from=weixin&utm_campaign=client_share&wxshare_count=1&timestamp=1541984175&app=news_article_lite&utm_source=weixin&iid=50377168296&utm_medium=toutiao_android&group_id=6617954633316827655",
		"https://www.toutiao.com/i6617954633316827655/?tt_from=weixin&utm_campaign=client_share&wxshare_count=1&timestamp=1541984175&app=news_article_lite&utm_source=weixin&iid=50377168296&utm_medium=toutiao_android&group_id=6617954633316827655",
		"https://www.toutiao.com/i6621357196997296643/?tt_from=weixin&utm_campaign=client_share&wxshare_count=1&timestamp=1541732945&app=news_article_lite&utm_source=weixin&iid=50478756673&utm_medium=toutiao_android&group_id=6621357196997296643",
		"https://www.toutiao.com/i6621372238220231171/?tt_from=weixin&utm_campaign=client_share&wxshare_count=1&timestamp=1541984439&app=news_article_lite&utm_source=weixin&iid=50377168296&utm_medium=toutiao_android&group_id=6621372238220231171",
	}

	client := &http.Client{}

	for index, urlPath := range urls {
		req, err := http.NewRequest("GET", urlPath, nil)

		if err != nil {
			log.Fatalln(err)
		}

		req.Header.Set("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0")
		req.Header.Set("Accept", "*/*")
		req.Header.Set("Host", "www.toutiao.com")
		req.Header.Set("accept-encoding", "gzip, deflate")
		req.Header.Set("Accept-Language", "zh-CN")

		resp, err := client.Do(req)
		if err != nil {
			log.Fatalln(err)
		}

		defer resp.Body.Close()
		reader, err := gzip.NewReader(resp.Body)

		bufReader := bufio.NewReader(reader)

		var validURL = regexp.MustCompile(`http://p[0-9]*.pstatp.com/large/pgc-image/[a-z0-9]*`)
		for {
			if str, err := bufReader.ReadString('\n'); err == nil {
				result := validURL.FindAllStringSubmatch(str, -1)
				for index1, v1 := range result {
					for index2, v2 := range v1 {
						fmt.Println(index, index1, index2, v2)
						req, err := http.NewRequest("GET", v2, nil)

						if err != nil {
							log.Fatalln(err)
						}

						req.Header.Set("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0")
						req.Header.Set("Accept", "*/*")
						req.Header.Set("Host", "www.toutiao.com")
						req.Header.Set("accept-encoding", "gzip, deflate")
						req.Header.Set("Accept-Language", "zh-CN")

						resp, err := client.Do(req)
						if err != nil {
							fmt.Println("failed", err)
							continue
						}
						defer resp.Body.Close()
						file, err := os.Create(fmt.Sprintf("/tmp/%d-%d-%d.jpeg", index, index1, index2))
						bufWriter := bufio.NewWriter(file)
						bufWriter.ReadFrom(resp.Body)
						defer file.Close()
					}
				}
			} else {
				break
			}
		}
	}
}
