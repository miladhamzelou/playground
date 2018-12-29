package playground

import (
	"fmt"
	"log"
	"strconv"
	"strings"
	"testing"
	"time"

	"net/http"

	"github.com/PuerkitoBio/goquery"
)

type TxPair struct {
	txhash      string
	time        string
	maker       string
	makerAmount float64
	taker       string
	takerAmount float64
	price       string
}

func (p TxPair) String() string {
	return fmt.Sprintf("%s,%s,%s,%f,%s,%f,%s", p.txhash, p.time, p.maker, p.makerAmount, p.taker, p.takerAmount, p.price)
}

func fetchSinglePage(filter, index int) {

	res, err := http.Get(fmt.Sprintf("https://etherscan.io/dextracker?filter=%d&p=%d", filter, index))
	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()
	if res.StatusCode != 200 {
		log.Fatalf("status code error: %d %s", res.StatusCode, res.Status)
	}

	// Load the HTML document
	doc, err := goquery.NewDocumentFromReader(res.Body)
	if err != nil {
		log.Fatal(err)
	}

	// Find the review items

	doc.Find("body div.wrapper div.profile.container div.row div div div.table-responsive table.table.table-hover tbody tr").Each(func(i int, s *goquery.Selection) {
		var pair TxPair
		var err error
		s.Find("td").Each(func(ii int, ss *goquery.Selection) {
			switch ii {
			case 0:
				{
					pair.txhash = strings.TrimSpace(ss.Text())
				}
			case 1:
				{
					pair.time = strings.TrimSpace(ss.Text())
				}
			case 2:
				{
					pair.maker = strings.TrimSpace(ss.Children().Text())
					ss.Children().Remove()
					if pair.makerAmount, err = strconv.ParseFloat(strings.TrimSpace(ss.Text()), 64); err != nil {
						panic(err)
					}
				}
			case 4:
				{
					pair.taker = strings.TrimSpace(ss.Children().Text())
					ss.Children().Remove()
					if pair.takerAmount, err = strconv.ParseFloat(strings.TrimSpace(ss.Text()), 64); err != nil {
						panic(err)
					}
				}
			case 5:
				{
					pair.price = strings.TrimSpace(ss.Text())
				}
			}

		})
		fmt.Printf("%v\n", pair)
	})
}

func TestHtml(t *testing.T) {
	t.SkipNow()
	for i := 1; i <= 100000; i++ {
		fetchSinglePage(11, i)
		time.Sleep(time.Millisecond * 10)
	}
}
