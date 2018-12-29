package playground

import (
	"fmt"
	"math"
	"testing"
)

func alignSize(nums []int) int {
	size := 0
	for _, n := range nums {
		if s := int(math.Log10(float64(n))) + 1; s > size {
			size = s
		}
	}

	return size
}

func TestWidth(t *testing.T) {
	nums := []int{12, 237, 3878, 3}
	size := alignSize(nums)
	for i, n := range nums {
		fmt.Printf("%02d %*d\n", i, size, n)
	}
}

// Point is a 2D point
type Point struct {
	X int
	Y int
}

func TestValueField(t *testing.T) {
	p := &Point{1, 2}
	fmt.Printf("%v %+v %#v \n", p, p, p)
}

func TestReferenceByPosition(t *testing.T) {
	fmt.Printf("The price of %[1]s was $%[2]d. $%[2]d! imagine that.\n", "carrot", 23)
}
