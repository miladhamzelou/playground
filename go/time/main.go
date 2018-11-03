package main

import "time"
import "fmt"

func main(){
	
	fmt.Println("time.Now().Location()： ", time.Now().Location())

	fmt.Println("time.Now()： ", time.Now())
	fmt.Println("time.Now().In(time.Local)： ", time.Now().In(time.Local))
	fmt.Println("time.Now().In(time.UTC)： ", time.Now().In(time.UTC))

	if newyork, err := time.LoadLocation("America/New_York"); err == nil {
		fmt.Println("time.Now().In(America/New_York)： ", time.Now().In(newyork))
	}


	
}

