package main

import (
	"fmt"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {
	httpPort := os.Getenv("HTTP_PORT")
	if httpPort == "" {
		httpPort = "8080"
	}

	filePath := os.Getenv("FILE_PATH")

	fmt.Println("Hello! This is a sample application to test serverless")
	fmt.Println("Working on", httpPort)
	fmt.Println("File path is", filePath)

	var sleepTime int = 0

	e := echo.New()
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.GET("/", func(c echo.Context) error {
		return c.HTML(http.StatusOK, "Hello Serverless Test!")
	})

	e.GET("/ping", func(c echo.Context) error {
		time.Sleep(time.Duration(sleepTime) * time.Millisecond)
		return c.JSON(http.StatusOK, struct {
			Status    string
			SleepTime int
		}{Status: "OK", SleepTime: sleepTime})
	})

	e.GET("/read", func(c echo.Context) error {
		dat, err := os.ReadFile(filePath)
		if err != nil {
			return c.JSON(http.StatusOK, struct {
				Status  string
				Content string
			}{Status: err.Error(), Content: ""})
		} else {
			return c.JSON(http.StatusOK, struct {
				Status  string
				Content string
			}{Status: "OK", Content: string(dat)})
		}
	})

	e.POST("/sleep", func(c echo.Context) error {
		newSleepTime, err := strconv.Atoi(c.FormValue("time"))
		if err != nil {
			return c.JSON(http.StatusOK, struct {
				Status string
			}{Status: err.Error()})
		}
		sleepTime = newSleepTime
		return c.JSON(http.StatusOK, struct {
			Status string
		}{Status: "OK"})
	})

	e.Logger.Fatal(e.Start(":" + httpPort))
}
