package common

import log "github.com/sirupsen/logrus"

type Sender interface {
	Send(message Message)
}

func FailOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

type Message struct {
	Address string `json:"address"`
	Body    string `json:"body"`
	Subject string `json:"subject"`
	RetryCount float64 `json:"retry_count"`
}
