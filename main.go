package main

import (
	"fmt"
	"io/ioutil"
	"log"

	_ "github.com/mattn/go-sqlite3"
	"gopkg.in/yaml.v2"
)

// 定义查询结果对应的结构体
type Link struct {
	Title       string `yaml:"title"`
	Logo        string `yaml:"logo"`
	Url         string `yaml:"url"`
	Description string `yaml:"description"`
}

type List struct {
	Term  string `yaml:"term"`
	Links []Link `yaml:"links"`
}

type Result struct {
	Taxonomy string `yaml:"taxonomy"`
	Icon     string `yaml:"icon"`

	Links []Link `yaml:"links"`
	List  []List `yaml:"list"`
}

// 嵌套一个外层列表
type Results []Result

func main() {

	// 假设从数据库查到的数据如下
	data := Results{
		{
			Taxonomy: "个人网站",
			Icon:     "far fa-star",
			Links: []Link{
				{
					Title:       "网址导航",
					Logo:        "bear2.png",
					Url:         "https://nav.jobcher.com/",
					Description: "个人网址导航,随缘更新",
				},
				{
					Title:       "网址导航",
					Logo:        "bear2.png",
					Url:         "https://nav.jobcher.com/",
					Description: "个人网址导航,随缘更新",
				},
			},
		},
	}

	// 将数据转换成yaml格式
	yamlData, err := yaml.Marshal(&data)
	if err != nil {
		log.Fatalf("error: %v", err)
	}
	ioutil.WriteFile("data.yml", yamlData, 0644)

	fmt.Println("生成成功!")
}
