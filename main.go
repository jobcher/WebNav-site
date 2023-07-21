package main

import (
	"database/sql"
	"fmt"
	"io/ioutil"
	"log"

	_ "github.com/mattn/go-sqlite3"
	"gopkg.in/yaml.v2"
)

// 定义查询结果对应的结构体
type Link struct {
	Title       string
	Logo        string
	Url         string
	Description string
}

type List struct {
	Term  string
	Links []Link
}

type Result struct {
	Taxonomy string
	Icon     string
	List     []List
}

// 嵌套一个外层列表
type Results []Result

func main() {
	db, _ := sql.Open("sqlite3", "./nav.db")
	rows, _ := db.Query("SELECT DISTINCT taxonomy,icon FROM nav_list")

	var data Results

	// 遍历查询结果
	for rows.Next() {
		var result Result
		rows.Scan(&result.Taxonomy, &result.Icon)

		// 查询子项
		rows2, _ := db.Query("SELECT DISTINCT term FROM nav_list WHERE taxonomy=?", result.Taxonomy)
		for rows2.Next() {
			var list List
			rows2.Scan(&list.Term)

			// 查询子项的链接
			rows3, _ := db.Query("SELECT title,logo,url,description FROM nav_list WHERE taxonomy=? AND term=?", result.Taxonomy, list.Term)
			for rows3.Next() {
				var link Link
				rows3.Scan(&link.Title, &link.Logo, &link.Url, &link.Description)
				list.Links = append(list.Links, link)
			}
			rows3.Close()

			result.List = append(result.List, list)
		}
		rows2.Close()

		data = append(data, result)
	}

	fmt.Println(data)

	// 将数据转换成yaml格式
	yamlData, err := yaml.Marshal(&data)
	if err != nil {
		log.Fatalf("error: %v", err)
	}
	ioutil.WriteFile("./data/webstack.yml", yamlData, 0644)

	fmt.Println("生成成功!")
}
