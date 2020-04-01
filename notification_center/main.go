package main

import (
	"fmt"
	log "github.com/sirupsen/logrus"
	"github.com/streadway/amqp"
	"notification/common"
	"notification/config"
	"notification/mq"
	"notification/sender"
)

func getConnectionString(conf *config.Config) string {
	return fmt.Sprintf("amqp://%s:%s@%s:%s",
		conf.RabbitLogin, conf.RabbitPassword, conf.RabbitName, conf.RabbitPort)
}

func Connect(connectionString string) (*amqp.Connection, error) {
	return amqp.Dial(connectionString)
}

func main() {
	log.SetFormatter(&log.TextFormatter{ForceColors:true, FullTimestamp:true, TimestampFormat:"2006-01-02 15:04:05"})
	log.Info("Attempting to connect")
	conf, err := config.EnvConfig()
	common.FailOnError(err, "Error reading config")
	connectionString := getConnectionString(conf)
	conn, err := Connect(connectionString)
	retryCount := 0
	for err != nil && retryCount > 0 {
		log.Warningf("Error connecting, %s, retrying", err)
		conn, err = Connect(connectionString)
		retryCount--
	}
	common.FailOnError(err, "Error connecting")
	log.Info("Successfully connected")
	defer conn.Close()

	log.Info("Creating channel")
	ch, err := conn.Channel()
	common.FailOnError(err, "Failed to open a channel")
	log.Info("Channel created")
	defer ch.Close()

	log.Info("Declaring email queue if not")
	qEmail, err := ch.QueueDeclare(
		conf.QueueEmail, // name
		false,           // durable
		false,           // delete when unused
		false,           // exclusive
		false,           // no-wait
		nil,             // arguments
	)
	common.FailOnError(err, "Failed to declare a queue")
	log.Info("Successfully declared")

	log.Info("Declaring sms queue if not")
	qSMS, err := ch.QueueDeclare(
		conf.QueueSms, // name
		false,           // durable
		false,           // delete when unused
		false,           // exclusive
		false,           // no-wait
		nil,             // arguments
	)
	common.FailOnError(err, "Failed to declare a queue")
	log.Info("Successfully declared")

	emailSender := sender.NewEmailSender(ch, qEmail, conf)
	readerEmail := mq.NewReader(emailSender, ch, qEmail)

	smsSender := sender.NewSMSSender()
	readerSms := mq.NewReader(smsSender, ch, qSMS)
	forever := make(chan struct{})

	go readerEmail.Start()
	go readerSms.Start()

	<-forever
}
