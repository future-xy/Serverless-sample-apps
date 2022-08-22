package main

import "fmt"
import "os"
import "net/http"
import "github.com/labstack/echo/v4"
import "github.com/labstack/echo/v4/middleware"

func main() {
	fmt.Println("Hello! This is a sample application to test serverless")

	e := echo.New()
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.GET("/", func(c echo.Context) error {
		return c.HTML(http.StatusOK, "Hello Serverless!")
	})

	e.GET("/ping", func(c echo.Context) error {
		return c.JSON(http.StatusOK, struct {
			Status string
		}{Status: "OK"})
	})

	httpPort := os.Getenv("HTTP_PORT")
	if httpPort == "" {
		httpPort = "8080"
	}

	e.Logger.Fatal(e.Start(":" + httpPort))
}
