package playground

import (
	"fmt"
	"testing"

	"github.com/garyburd/redigo/redis"
)

func TestRedis(t *testing.T) {
	var (
		conn redis.Conn
		err  error
	)
	if conn, err = redis.DialURL("redis://localhost:6379"); err != nil {
		fmt.Println(err)
		return
	}
	defer conn.Close()

	fmt.Println(conn.Do("GET", "nonexist"))
	fmt.Println(conn.Do("SET", "foo", int64(12)))
	fmt.Println(redis.Int64(conn.Do("GET", "foo")))
}
