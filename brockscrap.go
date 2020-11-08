package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/PuerkitoBio/goquery"
)

func init() {
	os.Truncate("Brockout.json", 0)

}

func parseName(url string, c chan int) {
	fl, _ := os.OpenFile("Brockout.json", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	resp, err := http.Get(url)
	if err != nil {
		fmt.Println(err)
		<-c
		return
	}
	page, _ := goquery.NewDocumentFromReader(resp.Body)
	name := page.Find("h1[class='entry-title']").Text()
	out := map[string]string{
		"url":  url,
		"name": name,
	}
	info, _ := json.Marshal(out)
	infotxt := string(info)
	infotxt += "\n"
	fl.Write([]byte(infotxt))
	fmt.Println("finished ", url)
	<-c

}

func main() {
	c := make(chan int, 2)
	defer close(c)
	resp, err := http.Get("https://brocku.ca/goodman/faculty-research/faculty-directory/")
	if err != nil {
		log.Fatal(err)
		return
	}
	defer resp.Body.Close()

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		log.Fatal(err)
	}
	doc.Find("strong a").Each(func(i int, tag *goquery.Selection) {
		url := tag.AttrOr("href", "")
		fmt.Println("sending ", url)
		if url != "" {
			go parseName(url, c)
		}
		c <- 1
	})
	fmt.Println("done")
}
