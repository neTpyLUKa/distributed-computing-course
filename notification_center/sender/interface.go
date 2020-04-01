package sender

type Sender interface {
	Send(address string, body string)
}
