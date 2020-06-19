package sender

import (
	"crypto/tls"
	"encoding/json"
	log "github.com/sirupsen/logrus"
	"github.com/streadway/amqp"
	"gopkg.in/gomail.v2"
	"notification/common"
	"notification/config"
	"strconv"
)

type EmailSender struct {
	channel *amqp.Channel
	queue   amqp.Queue
	dialer  *gomail.Dialer
	from    string
}

func (es *EmailSender) Send(message common.Message) {
	if message.RetryCount <= 0 {
		return
	}
	message.RetryCount = message.RetryCount - 1
	log.Infof("Attempting to send mail to email = %s, body = %s", message.Address, message.Body)
	m := gomail.NewMessage()
	m.SetHeader("From", es.from)
	m.SetHeader("To", message.Address)
	m.SetHeader("Subject", message.Subject)
	m.SetBody("text/html", message.Body)

	err := es.dialer.DialAndSend(m)
	if err != nil { // TODO add more timeout, generate more emails, clear all databases
		log.Errorf("Error sending email, err = %s", err)
		body, err := json.Marshal(message)
		if err != nil {
			return
		}

		err = es.channel.Publish(
			"",            // exchange
			es.queue.Name, // routing key
			false,         // mandatory
			false,         // immediate
			amqp.Publishing{
				ContentType: "application/json",
				Body:        []byte(body),
			})
		if err != nil {
			return
		}
	}
}

func NewEmailSender(channel *amqp.Channel, queue amqp.Queue, conf *config.Config) common.Sender {
	port, err := strconv.Atoi(conf.MailPort)
	common.FailOnError(err, "Wrong port given")
	res := &EmailSender{
		channel: channel,
		queue:   queue,
		from:    conf.Email,
		dialer: gomail.NewDialer(
			conf.MailHost,
			port,
			conf.Email,
			conf.MailPassword,

		),
	}
	res.dialer.TLSConfig = &tls.Config{InsecureSkipVerify: true}
	return res
}
