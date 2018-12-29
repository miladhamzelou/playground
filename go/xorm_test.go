package playground

import (
	"math/big"
	"testing"

	_ "github.com/go-sql-driver/mysql"
	"github.com/go-xorm/xorm"
	"github.com/stretchr/testify/assert"
)

var engine *xorm.Engine

type Int256 big.Int
type Account struct {
	Id      int64
	Balance Int256 `xorm:"decimal(38,18)"`
}

func NewInt256(i *big.Int) *Int256 {
	v := Int256(*i)
	return &v
}
func (i *Int256) FromDB(data []byte) error {
	v := (*big.Int)(i)
	v.SetString(string(data), 10)
	return nil
}

func (i *Int256) ToDB() ([]byte, error) {
	v := (*big.Int)(i)
	return []byte(v.String()), nil
}

func (i *Int256) String() string {
	v := (*big.Int)(i)
	return v.String()
}
func TestXorm(t *testing.T) {
	t.SkipNow()
	assert := assert.New(t)
	var engine *xorm.Engine
	var err error
	var has bool

	//	if engine, err = xorm.NewEngine("mysql", "dex:Y,^CD)^<Bi123@tcp(chain-dev-1:3306)/dex?charset=utf8"); err != nil {

	if engine, err = xorm.NewEngine("mysql", "root:6^R2${F+,zE#d(E_?h94@tcp(localhost:3306)/test?charset=utf8"); err != nil {

		panic(err)
	}

	if err = engine.DropTables(&Account{}); err != nil {
		panic(err)
	}

	if err = engine.CreateTables(&Account{}); err != nil {

		panic(err)
	}

	var user = Account{
		Id: 2,
	}

	user.Balance = *NewInt256(big.NewInt(1234))
	if _, err = engine.Insert(&user); err != nil {
		panic(err)
	}

	query := new(Account)
	query.Id = 2
	if has, err = engine.Get(query); err != nil {
		panic(err)
	}
	assert.Equal(true, has)
	assert.Equal(user, *query)

	accounts := make([]Account, 0)
	err = engine.Find(&accounts)
	assert.Equal(user, accounts[0])

}
