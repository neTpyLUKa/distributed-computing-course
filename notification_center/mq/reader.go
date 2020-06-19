package mq

import (
	"encoding/json"
	log "github.com/sirupsen/logrus"
	"github.com/streadway/amqp"
	"notification/common"
	"time"
)

type Reader struct {
	sender  common.Sender
	channel *amqp.Channel
	queue   amqp.Queue
}

func (r *Reader) Start() {
	log.Info("Creating consumer channel")
	messages, err := r.channel.Consume(
		r.queue.Name, // queue
		"",           // consumer
		true,         // auto-ack
		false,        // exclusive
		false,        // no-local
		false,        // no-wait
		nil,          // args
	)
	common.FailOnError(err, "Failed to register a consumer")
	log.Info("Successfully created")

	for rawMsg := range messages {
		var msg common.Message
		err := json.Unmarshal(rawMsg.Body, &msg)
		if err != nil {
			log.Info("Error unmarshaling message")
			continue
		}
		go r.sender.Send(msg)
		time.Sleep(10 * time.Second)
	}
}

func NewReader(sender common.Sender, channel *amqp.Channel, queue amqp.Queue) *Reader {
	return &Reader{sender: sender, channel: channel, queue: queue}
}
