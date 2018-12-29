package playground

import (
	"reflect"
	"testing"
)

type Jedi interface {
	HasForce() bool
}

type Knight struct{}

func (*Knight) HasForce() bool {

	return false
}

var _ Jedi = (*Knight)(nil) // 利用编译器检查接口实现
func TestInterface(t *testing.T) {
	var o *int = nil
	var a interface{} = o
	var b interface{}

	println(a == nil, b == nil) // false, true

	v := reflect.ValueOf(a)
	if v.IsValid() {
		println(v.IsNil()) // true, This is nil interface
	}
}
