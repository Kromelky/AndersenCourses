package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"sort"
	"strconv"
	s "string"

	tgbotapi "github.com/Syfaro/telegram-bot-api"
)

type UserData struct {
	UserName string
	TaskList []Task
}

type ReadmeContent struct {
	content string
}

type Task struct {
	TaskNum int64 `json:"-"`
	Name    string
	Path    string
	Dirtype string        `json:"type"`
	content ReadmeContent `json:"-"`
}

var (
	telegramBotToken string
	UserDataList     []UserData
)

func init() {
	flag.StringVar(&telegramBotToken, "tkn", "", "Telegram Bot Token")
	flag.Parse()
	fmt.Print(telegramBotToken)
	if telegramBotToken == "" {
		log.Print("-telegrambottoken is required")
		os.Exit(1)
	}
}

func remove(s []Task, i int) []Task {
	s[i] = s[len(s)-1]
	return s[:len(s)-1]
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
	UserDataList := []UserData{}

	for update := range updates {
		reply := "Не знаю что сказать"
		if update.Message == nil {
			continue
		}

		log.Printf("[%s] %s", update.Message.From.UserName, update.Message.Text)

		var userData *UserData
		exists := false
		for _, i := range UserDataList {
			if i.UserName == update.Message.From.UserName {
				exists = true
				userData = &i
				break
			}
		}
		if !exists {
			userData := UserData{}
			userData.UserName = update.Message.From.UserName
		}

		switch update.Message.Command() {
		case "start":
			reply = "Привет " + userData.UserName + ". Я телеграм-ботоздания новой /restart"
		case "git":
			userData.TaskList = readRepo("https://api.github.com/repos/Kromelky/AndersenCourses/contents")
			reply = "world"

		case "tasks":
			reply = "world"

			msg := tgbotapi.NewMessage(update.Message.Chat.ID, reply)

			bot.Send(msg)
		}
	}
}

func readRepo(url string) []Task {
	res, err := http.Get(url)
	if err != nil {
		log.Fatal(err)
	}
	body, err := ioutil.ReadAll(res.Body)
	res.Body.Close()
	if err != nil {
		log.Fatal(err)
	}
	if res.StatusCode != http.StatusOK {
		log.Fatal("Unexpected status code", res.StatusCode)
	}
	data := []Task{}
	err = json.Unmarshal(body, &data)
	if err != nil {
		log.Fatal(err)
	}

	remidxesList := []int{}

	for idx, Task := range data {
		if Task.Dirtype != "dir" {
			remidxesList = append(remidxesList, idx)
			continue
		}
		splitedName := s.split(Task.Name, '_')
		if len(splitedName) > 1 && s.Contains(splitedName[1], "Homework") {
			i2, err := strconv.ParseInt(splitedName[0], 10, 64)
			if err != nil {
				remidxesList = append(remidxesList, idx)
				log.Print(err)
				continue
			}
			Task.TaskNum = i2
		} else {
			remidxesList = append(remidxesList, idx)
		}
	}
	sort.Sort(sort.Reverse(sort.IntSlice(remidxesList)))

	for _, ixd := range remidxesList {
		data = remove(data, ixd)
	}

	return data
}
