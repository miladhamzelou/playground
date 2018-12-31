package playground

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/mock"
)

// MessageService handles notifying clients they have
// been charged
type MessageService interface {
	SendChargeNotification(int) error
}

// SMSService is our implementation of MessageService
type SMSService struct{}

// MyService uses the MessageService to notify clients
type MyService struct {
	messageService MessageService
}

// SendChargeNotification notifies clients they have been
// charged via SMS
// This is the method we are going to mock
func (sms SMSService) SendChargeNotification(value int) error {
	fmt.Println("Sending Production Charge Notification")
	return nil
}

// ChargeCustomer performs the charge to the customer
// In a real system we would maybe mock this as well
// but here, I want to make some money every time I run my tests
func (a MyService) ChargeCustomer(value int) error {
	a.messageService.SendChargeNotification(value)
	fmt.Printf("Charging Customer For the value of %d\n", value)
	return nil
}

// smsServiceMock
type smsServiceMock struct {
	mock.Mock
}

// Our mocked smsService method
func (m *smsServiceMock) SendChargeNotification(value int) error {
	fmt.Println("Mocked charge notification function")
	fmt.Printf("Value passed in: %d\n", value)
	// this records that the method was called and passes in the value
	// it was called with
	args := m.Called(value)
	fmt.Printf("args: %#v\n", args)
	// it then returns whatever we tell it to return
	// in this case true to simulate an SMS Service Notification
	// sent out
	return args.Error(0)
}

// we need to satisfy our MessageService interface
// which sadly means we have to stub out every method
// defined in that interface
func (m *smsServiceMock) DummyFunc() {
	fmt.Println("Dummy")
}

// TestChargeCustomer is where the magic happens
// here we create our SMSService mock
func TestChargeCustomer(t *testing.T) {
	smsService := new(smsServiceMock)

	// we then define what should be returned from SendChargeNotification
	// when we pass in the value 100 to it. In this case, we want to return
	// true as it was successful in sending a notification
	smsService.On("SendChargeNotification", 100).Return(nil)

	// next we want to define the service we wish to test
	myService := MyService{smsService}
	// and call said method
	myService.ChargeCustomer(100)

	// at the end, we verify that our myService.ChargeCustomer
	// method called our mocked SendChargeNotification method
	smsService.AssertExpectations(t)
}

// A "Production" Example
// func main () {
// 	fmt.Println("Hello World")

// 	smsService := SMSService{}
// 	myService := MyService{smsService}
// 	myService.ChargeCustomer(100)
// }
