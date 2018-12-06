package playground

type User struct {
	Person Male
}

func NewUser(p Male) *User {
	return &User{Person: p}
}

func (u *User) GetUserInfo(id int64) error {
	return u.Person.Get(id)
}
