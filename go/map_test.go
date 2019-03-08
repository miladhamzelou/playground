package playground

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestNilMap(t *testing.T) {

	var m map[string]string
	// m = make(map[string]string)
	m = map[string]string{
		"a": "aa",
		"b": "bb"}

	fmt.Println(m)
}

func TestSlice(t *testing.T) {
	var s []int
	s = append(s, 1)
	fmt.Println(s)
}

type Student struct {
	name string
	age  int
}

func TestRange(t *testing.T) {
	assert := assert.New(t)
	students := []Student{
		{"a", 10},
	}
	for _, s := range students {
		s.age += 1
	}
	assert.Equal(students[0].age, 10)

	for i := 0; i < len(students); i++ {
		students[i].age += 1
	}
	assert.Equal(students[0].age, 11)

	students_ref := []*Student{
		&Student{"a", 10},
	}
	for _, s := range students_ref {
		s.age += 1
	}
	assert.Equal(students_ref[0].age, 11)

}
