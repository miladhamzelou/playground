package playground

import (
	"fmt"
	"log"
	"strings"
	"testing"

	"github.com/PuerkitoBio/goquery"
)

func TestGoQuery_SelectByElement(t *testing.T) {
	html := `<body>
                       <div>DIV1</div>
                       <div>DIV2</div>
                       <span>SPAN</span>

                   </body>
                   `

	dom, err := goquery.NewDocumentFromReader(strings.NewReader(html))
	if err != nil {
		log.Fatalln(err)
	}

	dom.Find("div").Each(func(i int, selection *goquery.Selection) {
		fmt.Println(selection.Text())
	})
}

func TestGoQuery_SelectByID(t *testing.T) {
	html := `<body>
                       <div id="div1">DIV1</div>
                       <div>DIV2</div>
                       <span>SPAN</span>
                   </body>
                   `

	dom, err := goquery.NewDocumentFromReader(strings.NewReader(html))
	if err != nil {
		log.Fatalln(err)
	}

	dom.Find("#div1").Each(func(i int, selection *goquery.Selection) {
		fmt.Println(selection.Text())
	})
}
func TestGoQuery_SelectByClass(t *testing.T) {

	html := `<body>

                       <div id="div1">DIV1</div>
                       <div class="name">DIV2</div>
                       <span>SPAN</span>

                   </body>
                   `

	dom, err := goquery.NewDocumentFromReader(strings.NewReader(html))
	if err != nil {
		log.Fatalln(err)
	}

	dom.Find(".name").Each(func(i int, selection *goquery.Selection) {
		fmt.Println(selection.Text())
	})
}
func TestGoQuery_SelectByProperty(t *testing.T) {

	html := `<body>
                       <div>DIV1</div>
                       <div class="name">DIV2</div>
                       <span>SPAN</span>
                   </body>
                   `

	dom, err := goquery.NewDocumentFromReader(strings.NewReader(html))
	if err != nil {
		log.Fatalln(err)
	}

	dom.Find("div[class]").Each(func(i int, selection *goquery.Selection) {
		fmt.Println(selection.Text())
	})
}

func TestGoQuery_SelectByParentChild(t *testing.T) {

	html := `<body>

                       <div lang="ZH">DIV1</div>
                       <div lang="zh-cn">DIV2</div>
                       <div lang="en">DIV3</div>
                       <span>
                           <div>DIV4</div>
                       </span>

                   </body>
                   `

	dom, err := goquery.NewDocumentFromReader(strings.NewReader(html))
	if err != nil {
		log.Fatalln(err)
	}

	dom.Find("body>div").Each(func(i int, selection *goquery.Selection) {
		fmt.Println(selection.Text())
	})
}

func TestGoQuery_SelectOnlyData(t *testing.T) {

	html := `<body>
               <div>abc
                 <a target="/a"> def </>
               </div>
             </body>
                   `

	dom, err := goquery.NewDocumentFromReader(strings.NewReader(html))
	if err != nil {
		log.Fatalln(err)
	}
	div := dom.Find("body div")
	div.Children().Remove()
	fmt.Println(div.Text())
	// dom.Find("body div:~a").Each(func(i int, selection *goquery.Selection) {
	// 	fmt.Println(selection.Text())
	// })
}
