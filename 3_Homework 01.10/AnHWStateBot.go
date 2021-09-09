package main

import (
	"flag"
	"github.com/Syfaro/telegram-bot-api"
	"log"
	"os"
)

var (
	telegramBotToken string
)

func init() {
	flag.StringVar(&telegramBotToken, "telegrambottoken", "", "Telegram Bot Token")
	flag.Parse()

	if telegramBotToken == "" {
		log.Print("-telegrambottoken is required")
		os.Exit(1)
	}
}

func main() {
	bot, err := tgbotapi.NewBotAPI(telegramBotToken)
	if err != nil {
		log.Panic(err)
	}

	log.Printf("Authorized on account %s", bot.Self.UserName)

	u := tgbotapi.NewUpdate(0)
	u.Timeout = 60


	updates, err := bot.GetUpdatesChan(u)


	for update := range updates {
		reply := "Не знаю что сказать"
		if update.Message == nil {
			continue
		}

		log.Printf("[%s] %s", update.Message.From.UserName, update.Message.Text)

		switch update.Message.Command() {
		case "start":
			reply = "Привет. Я телеграм-бот"
		case "hello":
			reply = "world"
		}

		msg := tgbotapi.NewMessage(update.Message.Chat.ID, reply)

		bot.Send(msg)
	}
}