package playground

import (
	"fmt"
	"testing"

	"github.com/google/btree"
)

func TestBtree(t *testing.T) {
	tr := btree.New(2)
	for i := btree.Int(0); i < 10; i++ {
		tr.ReplaceOrInsert(i)
	}
	fmt.Println("len:       ", tr.Len())
	fmt.Println("get3:      ", tr.Get(btree.Int(3)))
	fmt.Println("get100:    ", tr.Get(btree.Int(100)))
	fmt.Println("del4:      ", tr.Delete(btree.Int(4)))
	fmt.Println("del100:    ", tr.Delete(btree.Int(100)))
	fmt.Println("replace5:  ", tr.ReplaceOrInsert(btree.Int(5)))
	fmt.Println("replace100:", tr.ReplaceOrInsert(btree.Int(100)))
	fmt.Println("min:       ", tr.Min())
	fmt.Println("delmin:    ", tr.DeleteMin())
	fmt.Println("max:       ", tr.Max())
	fmt.Println("delmax:    ", tr.DeleteMax())
	fmt.Println("len:       ", tr.Len())
}
