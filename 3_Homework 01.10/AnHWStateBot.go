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
	"encoding/base64"
	"regexp"
	s "strings"

	tgbotapi "github.com/Syfaro/telegram-bot-api"
)

type ReadmeContent struct {
	Content string
	Text string 	`json:"-"`
	state string 	`json:"-"`
}

type Task struct {
	TaskNum int			  `json:"-"`
	Name    string
	Path    string
	Url 	string
	Html_url string		
	Dirtype string        `json:"type"`
	content ReadmeContent `json:"-"`
}

var (
	telegramBotToken string
	repo_url		 string
	Tasks     		 []Task
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

func findTaskbyId(TaskList []Task, num int) *Task {
	for _, tsk := range TaskList{
		if tsk.TaskNum == num{
			return &tsk
		}			
	}
	return nil
}

func DecodeB64(message string) (retour string) {
    base64Text := make([]byte, base64.StdEncoding.DecodedLen(len(message)))
    base64.StdEncoding.Decode(base64Text, []byte(message))
    fmt.Printf("base64: %s\n", base64Text)
    return string(base64Text)
}

func parceREADMEContent(cnt ReadmeContent)  {

}


func getTaskStatus(task *Task) {	
	ReadMeUrl := s.Replace(task.Url,"?ref=main", "" ,1) + "/README.md"
	fmt.Println(ReadMeUrl)
	res, err := http.Get(ReadMeUrl)
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
	data := ReadmeContent{}
	err = json.Unmarshal(body, &data)
	if err != nil {
		log.Fatal(err)
	}
	if data.Content != "" {
		data.Text = DecodeB64(data.Content)
		var re = regexp.MustCompile(`<!--STATUS=([^-])`)
		matches := re.FindStringSubmatch(data.Text)
		if matches != nil && len(matches) > 1{
			data.state = matches[1]
		}
	}
	task.content = data
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

	for idx, tsk := range data {
		if tsk.Dirtype != "dir" {
			remidxesList = append(remidxesList, idx)
			continue
		}
		splitedName := s.Split(tsk.Name, "_")
		if len(splitedName) > 1 && s.Contains(splitedName[1], "Homework") {
			i2, err := strconv.Atoi(splitedName[0])
			if err != nil {
				remidxesList = append(remidxesList, idx)
				log.Print(err)
				continue
			}
			data[idx].TaskNum = i2
			fmt.Println(tsk.TaskNum)
		} else {
			remidxesList = append(remidxesList, idx)
		}
	}
	sort.Sort(sort.Reverse(sort.IntSlice(remidxesList)))

	for _, ixd := range remidxesList {
		data = remove(data, ixd)
	}
	sort.SliceStable(data, func(i, j int) bool {
		return data[i].TaskNum < data[j].TaskNum
	})

	return data
}


func main() {

	repo_url = "https://api.github.com/repos/Kromelky/AndersenCourses"

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
		cmd := update.Message.Command()
		switch cmd {
		case "start":
			reply = "Привет " + update.Message.From.UserName + ". Я телеграм-бот c домашними заданиями"
		case "git":			
			reply = repo_url
		case "tasks":
			Tasks = readRepo(repo_url + "/contents")
			reply = ""
			for _, tsk := range Tasks {
				reply+=fmt.Sprintf("/task%v\t-\t%v\n", tsk.TaskNum, tsk.Name)
			}
		default:
			if Tasks == nil{
				Tasks = readRepo(repo_url + "/contents")
			}
			if s.Contains(cmd, "task"){
				task_num, err := strconv.Atoi(s.Replace(cmd,"task","",1))
				if err != nil {
					reply = "Не понимаю номер задания"
					break
				} 
				var TaskByNum *Task
				TaskByNum = findTaskbyId(Tasks, task_num)
				if TaskByNum == nil {
					reply = "Не могу найти задание с номером " + strconv.Itoa(task_num)
					break 
				}		
				msg := tgbotapi.NewMessage(update.Message.Chat.ID, TaskByNum.Html_url)
				bot.Send(msg)

				getTaskStatus(TaskByNum)
				fmt.Println(TaskByNum.content.state)
			}			
		}	
		msg := tgbotapi.NewMessage(update.Message.Chat.ID, reply)
		bot.Send(msg)
	}
}