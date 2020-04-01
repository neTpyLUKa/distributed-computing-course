package main

import (
	log "github.com/sirupsen/logrus"
	"github.com/streadway/amqp"
	"notification/mq"
	"notification/sender"
)

func Connect() (*amqp.Connection, error) {
	return amqp.Dial("amqp://guest:guest@rabbitmq:5672/")
}

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

func main() {
	conn, err := Connect()
	for err != nil { // TODO add retrycount
		log.Warningf("Error connecting, %s, retrying", err)
		conn, err = Connect()
	}
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"hello", // name TODO use config
		false,   // durable
		false,   // delete when unused
		false,   // exclusive
		false,   // no-wait
		nil,     // arguments
	)
	failOnError(err, "Failed to declare a queue")

	email_sender := sender.NewEmailSender(ch, q)
	reader := mq.NewReader(email_sender, ch, q)

	forever := make(chan struct{})

	go reader.Start()

	<-forever
	/*body := "Hello World!"
	err = ch.Publish(
		"",     // exchange
		q.Name, // routing key
		false,  // mandatory
		false,  // immediate
		amqp.Publishing {
			ContentType: "text/plain",
			Body:        []byte(body),
		})
	failOnError(err, "Failed to publish a message")
*/}
