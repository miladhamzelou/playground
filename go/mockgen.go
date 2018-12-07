//go:generate mockgen -source=./mockgen.go -destination=./mockgen_mock.go -package=playground
package playground

type Male interface {
	Get(id int64) error
}


type User struct {
	Person Male
}

func NewUser(p Male) *User {
	return &User{Person: p}
}

func (u *User) GetUserInfo(id int64) error {
	return u.Person.Get(id)
}
