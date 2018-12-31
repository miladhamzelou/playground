package playground

import (
	"fmt"
	"testing"
)

func TestPanic(t *testing.T) {

	defer func() {
		if r := recover(); r != nil {
			fmt.Println("parent recover: ", r)
		}
	}()
	go func() {
		defer func() {
			if r := recover(); r != nil {
				fmt.Println("child recover: ", r)
			}
		}()
		panic("panic")
	}()

}
