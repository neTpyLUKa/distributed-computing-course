package sender

import (
	log "github.com/sirupsen/logrus"
	"github.com/streadway/amqp"
	"gopkg.in/gomail.v2"
)

type EmailSender struct {
	channel *amqp.Channel
	queue   amqp.Queue
	dialer  *gomail.Dialer
	from    string
}

func (es *EmailSender) Send(email string, body string) {
	log.Infof("email = %s, body = %s", email, body)
	m := gomail.NewMessage()
	m.SetHeader("From", es.from)
	m.SetHeader("To", email)
	m.SetHeader("Subject", "sample notification")
	m.SetBody("text/html", body)

	err := es.dialer.DialAndSend(m)
	if err != nil {
		log.Warningf("Error sending email, err = %s", err)
	}
}

func NewEmailSender(channel *amqp.Channel, queue amqp.Queue) Sender {
	return &EmailSender{
		channel: channel,
		queue:   queue,
		from:    "dc-sender@mail.ru",
		dialer: gomail.NewDialer(
			"smtp.mail.ru",
			465,
			"dc-sender@mail.ru",
			"pytyUXhTO73~",
		),
	}
}
