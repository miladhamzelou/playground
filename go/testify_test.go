package playground

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func Calculate(n int) int {
	return 2 + n
}
func TestCalculate(t *testing.T) {
	assert.Equal(t, Calculate(2), 4)
}

func TestStatusNotDown(t *testing.T) {
	assert := assert.New(t)

	var tests = []struct {
		input    int
		expected int
	}{
		{2, 4},
		{-1, 1},
		{0, 2},
		{-5, -3},
		{99999, 100001},
	}

	for _, test := range tests {
		assert.Equal(Calculate(test.input), test.expected)
	}
}
