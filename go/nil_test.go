package playground

import (
	"fmt"
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
)

type Bar struct{}

func (Bar) Error() string {
	return "bar"
}

func TestNil_1(t *testing.T) {
	assert.True(t, (*string)(nil) == nil, "(*string)(nil) == nil: failed")
	assert.True(t, (interface{})(nil) == nil, "(interface{})(nil) == nil: failed")
}

func TestNil_2(t *testing.T) {
	assert.True(t, (*Bar)(nil) == nil)           // true
	assert.True(t, (error)(nil) == nil)          // true
	assert.False(t, (error)((*Bar)(nil)) == nil) // False
}

func Hello(e error) (err error) {
	defer func() {
		if r := recover(); r != nil {
			if e == nil || reflect.ValueOf(e).IsNil() {
				err = fmt.Errorf("hello: <nil>")
				return
			}
			panic(r)
		}
	}()
	err = fmt.Errorf("hello: %s", e.Error())
	return
}

func TestRecover(t *testing.T) {
	Hello(fmt.Errorf("me"))
}
