package config

import "github.com/caarlos0/env/v6"

type Config struct {
	QueueEmail     string `env:"QUEUE_EMAIL"`
	QueueSms       string `env:"QUEUE_SMS"`
	MailHost       string `env:"MAIL_HOSTNAME"`
	MailPort       string `env:"MAIL_PORT"`
	Email          string `env:"MAIL_EMAIL"`
	MailPassword   string `env:"MAIL_PASSWORD"`
	RabbitLogin    string `env:"RABBITMQ_USER"`
	RabbitPassword string `env:"RABBITMQ_PASS"`
	RabbitPort     string `env:"MQ_PORT"`
	RabbitName     string `env:"RABBITMQ_NAME"`
}

func EnvConfig() (*Config, error) {
	var config Config
	err := env.Parse(&config)
	if err != nil {
		return nil, err
	}
	return &config, nil
}
