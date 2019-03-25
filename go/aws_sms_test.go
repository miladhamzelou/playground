package playground

import (
	"fmt"
	"strconv"
	"testing"
	"time"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/sqs"
)

func TestAwsSqs(t *testing.T) {
	sess := session.Must(session.NewSessionWithOptions(session.Options{
		SharedConfigState: session.SharedConfigEnable,
		Config:            aws.Config{Region: aws.String("ap-northeast-1")},
	}))

	svc := sqs.New(sess)

	// URL to our queue
	qURL := "https://sqs.ap-northeast-1.amazonaws.com/356236652163/simple-queue-service.fifo"
	id := strconv.FormatInt(time.Now().Unix(), 10)
	result, err := svc.SendMessage(&sqs.SendMessageInput{
		DelaySeconds: aws.Int64(0),
		MessageAttributes: map[string]*sqs.MessageAttributeValue{
			"Title": &sqs.MessageAttributeValue{
				DataType:    aws.String("String"),
				StringValue: aws.String("The Whistler"),
			},
			"Author": &sqs.MessageAttributeValue{
				DataType:    aws.String("String"),
				StringValue: aws.String("John Grisham"),
			},
			"WeeksOn": &sqs.MessageAttributeValue{
				DataType:    aws.String("Number"),
				StringValue: aws.String("6"),
			},
		},
		MessageBody:            aws.String("Information about current NY Times fiction bestseller for week of 12/11/2016."),
		QueueUrl:               &qURL,
		MessageGroupId:         aws.String("1"),
		MessageDeduplicationId: &id,
	})

	if err != nil {
		fmt.Println("Error", err)
		return
	}
	fmt.Println("SendMessage Success", *result.MessageId)

	time.Sleep(10 * time.Second)
	{
		result, err := svc.ReceiveMessage(&sqs.ReceiveMessageInput{
			AttributeNames: []*string{
				aws.String(sqs.MessageSystemAttributeNameSentTimestamp),
			},
			MessageAttributeNames: []*string{
				aws.String(sqs.QueueAttributeNameAll),
			},
			QueueUrl:            &qURL,
			MaxNumberOfMessages: aws.Int64(1),
			VisibilityTimeout:   aws.Int64(20), // 20 seconds
			WaitTimeSeconds:     aws.Int64(0),
		})

		if err != nil {
			fmt.Println("Error", err)
			return
		}

		if len(result.Messages) == 0 {
			fmt.Println("Received no messages")
			return
		}

		fmt.Printf("ReceivedMessage: %#v\n", result)

		resultDelete, err := svc.DeleteMessage(&sqs.DeleteMessageInput{
			QueueUrl:      &qURL,
			ReceiptHandle: result.Messages[0].ReceiptHandle,
		})

		if err != nil {
			fmt.Println("Delete Error", err)
			return
		}

		fmt.Println("Message Deleted", resultDelete)
	}
}
