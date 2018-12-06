//go:generate mockgen -source=./male.go -destination=./male_mock.go -package=playground
package playground

type Male interface {
	Get(id int64) error
}
