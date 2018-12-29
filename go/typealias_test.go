package playground

import (
	"fmt"
	"testing"
)

type MyInt1 int
type MyInt2 = int

func (i MyInt1) m1() {
	fmt.Println("MyInt1.m1")
}

// func (i MyInt2) m2() {
// 	fmt.Println("MyInt2.m2")
// }

type user struct {
}
type MyUser1 user
type MyUser2 = user

func (i MyUser1) m1() {
	fmt.Println("MyUser1.m1")
}

func (i MyUser2) m2() {
	fmt.Println("MyUser2.m2")
}

type I interface {
	m2()
}

func (i user) m() {
	fmt.Println("User.m")
}

func TestTypeAlias(t *testing.T) {

	var i1 MyInt1
	//var i2 MyInt2
	i1.m1()
	//i2.m2()

	var u1 MyUser1
	var u2 MyUser2
	u1.m1()
	u2.m2()

}
