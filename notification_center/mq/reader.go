package mq

import (
	"encoding/json"
	log "github.com/sirupsen/logrus"
	"github.com/streadway/amqp"
	"notification/sender"
)

type Reader struct {
	sender  sender.Sender
	channel *amqp.Channel
	queue   amqp.Queue
}

type message struct {
	Address string `json:"address"`
	Body    string `json:"body"`
}

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

func (r *Reader) Start() {
	msgs, err := r.channel.Consume(
		r.queue.Name, // queue
		"",           // consumer
		true,         // auto-ack
		false,        // exclusive
		false,        // no-local
		false,        // no-wait
		nil,          // args
	)
	failOnError(err, "Failed to register a consumer")

	for raw_msg := range msgs {
		var msg message
		err := json.Unmarshal(raw_msg.Body, &msg)
		if err != nil {
			continue // TODO handle error ?
		}
		go r.sender.Send(msg.Address, msg.Body)
	}
}

func NewReader(sender sender.Sender, channel *amqp.Channel, queue amqp.Queue) *Reader {
	return &Reader{sender: sender, channel: channel, queue: queue}
}
