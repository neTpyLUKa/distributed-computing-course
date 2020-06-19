package sender

import (
	log "github.com/sirupsen/logrus"
	"net/http"
	"net/url"
	"notification/common"
)

type SMSSender struct {
	apiId string
}

func (s SMSSender) Send(message common.Message) {
	log.Infof("Attempting to send sms to phone = %s, body = %s", message.Address, message.Body)
	u, err := url.Parse("https://sms.ru/sms/send")
	if err != nil {
		log.Errorf("Error parsing url")
		return
	}
	q := u.Query()
	q.Add("api_id", s.apiId)
	q.Add("to", message.Address)
	q.Add("msg", message.Body)
	q.Add("json", "1")
	log.Infof("url string = %s", q)
	u.RawQuery = q.Encode()
	resp, _ := http.Get(u.String())
	log.Info(resp)
	log.Infof("Sent Successfully")

}

func NewSMSSender() common.Sender {
	return &SMSSender{apiId: "BD126304-AC4D-19AA-C9B4-F5C3F2F0E9EC"} // my = "32C794C0-65B9-A229-F742-EA0D97B3B9B0"}
}
