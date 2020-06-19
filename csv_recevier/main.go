package main

import (
	"csv_receiver/common"
	"csv_receiver/config"
	"fmt"
	"github.com/nu7hatch/gouuid"
	log "github.com/sirupsen/logrus"
	"github.com/streadway/amqp"
	"io"
	"net/http"
	"os"
	"path/filepath"
)

func getConnectionString(conf *config.Config) string {
	return fmt.Sprintf("amqp://%s:%s@%s:%s",
		conf.RabbitLogin, conf.RabbitPassword, conf.RabbitName, conf.RabbitPort)
}

func Connect(connectionString string) (*amqp.Connection, error) {
	return amqp.Dial(connectionString)
}

func main() {
	conf, err := config.EnvConfig()
	common.FailOnError(err, "Error getting config")

	connString := getConnectionString(conf)

	log.Info("Connecting to rmq...")
	conn, err := Connect(connString)
	common.FailOnError(err, "Error connecting to rmq")
	log.Info("Successfully connected")

	ch, err := conn.Channel()
	common.FailOnError(err, "Error getting channel")

	qCsv, err := ch.QueueDeclare(
		conf.QueueCsv, // name
		false,         // durable
		false,         // delete when unused
		false,         // exclusive
		false,         // no-wait
		nil,           // arguments
	)
	common.FailOnError(err, "Error declaring queue")

	http.HandleFunc("/upload", func(writer http.ResponseWriter, request *http.Request) {
		id, err := uuid.NewV4()
		if err != nil {
			writer.WriteHeader(http.StatusInternalServerError)
			return
		}

		filename := id.String() + ".csv"
		out, err := os.Create(filepath.Join("/csv_data/", filename))
		if err != nil {
			writer.WriteHeader(http.StatusInternalServerError)
			return
		}
		defer out.Close()

		log.Println(request.Header)

		_, err = io.Copy(out, request.Body)
		if err != nil {
			writer.WriteHeader(http.StatusInternalServerError)
			return
		}

		writer.WriteHeader(http.StatusOK)

		log.Info("Publishing message")
		err = ch.Publish("", // exchange
			qCsv.Name, // routing key
			false,     // mandatory
			false,     // immediate
			amqp.Publishing{
				Body: []byte(filename),
			},
		)
		common.FailOnError(err, "Error publishing message")
		log.Info("Message pubished")
	})
	log.Info(conf)
	log.Fatal(http.ListenAndServe("csv_receiver:"+conf.CsvPort, nil))
}
