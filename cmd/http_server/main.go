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
	fmt.Println("Hello! This is a sample application to test serverless")

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

	e.POST("/sleep", func(c echo.Context) error {
		newSleepTime, err := strconv.Atoi(c.FormValue("time"))
		if err != nil {
			return c.JSON(http.StatusOK, struct {
				Status  string
				Success string
			}{Status: "OK", Success: "False"})
		}
		sleepTime = newSleepTime
		return c.JSON(http.StatusOK, struct {
			Status  string
			Success string
		}{Status: "OK", Success: "True"})
	})

	httpPort := os.Getenv("HTTP_PORT")
	if httpPort == "" {
		httpPort = "8080"
	}

	e.Logger.Fatal(e.Start(":" + httpPort))
}
