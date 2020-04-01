package config

type config struct {
	QueueEmail string `env:"QUEUE_EMAIL"`
	QueueSms string `env:"QUEUE_SMS"`
	SMTPHost string `env:"SMTP_HOST"`
	SMTPPort string `env:"SMTP_PORT"`
	SMTPUsername string `env:"SMTP_USERNAME""`
}
