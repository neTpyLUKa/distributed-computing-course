package config

import "github.com/caarlos0/env/v6"

type Config struct {
	QueueCsv       string `env:"QUEUE_CSV"`
	RabbitLogin    string `env:"RABBITMQ_USER"`
	RabbitPassword string `env:"RABBITMQ_PASS"`
	RabbitPort     string `env:"MQ_PORT"`
	RabbitName     string `env:"RABBITMQ_NAME"`
	CsvPort        string `env:"CSV_RECEIVER_PORT"`
}

func EnvConfig() (*Config, error) {
	var config Config
	err := env.Parse(&config)
	if err != nil {
		return nil, err
	}
	return &config, nil
}
