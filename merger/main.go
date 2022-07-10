package main

import (
	"fmt"
	"flag"
	"os"
	"strconv"
	"strings"
	"io/ioutil"
)

func main(){
	var name string
	flag.StringVar(&name, "f", "default", "filename to merge")
	flag.Parse()

	nameParts := strings.Split(name, ".")
	filename := nameParts[len(nameParts) - 2]
	baseFilename := "../cutter/" + filename
	extension := nameParts[len(nameParts) - 1]
	fmt.Printf("file: %v\n", baseFilename)

	mergedFile := "./" + filename + "-merged"+ "." + extension

	numberOfPieces := uint64(9)
	var curr []byte
	for i := uint64(0); i < numberOfPieces; i++ {
		currFile := baseFilename + "_" + strconv.FormatUint(i, 10) + ".cylf"
		
		file, err := os.Open(currFile)
		fileInfo, _ := file.Stat()
		var fileSize int64 = fileInfo.Size()
		b := make([]byte, fileSize)
		file.Read(b)
		if err != nil {
			fmt.Printf("[ERROR] %v\n", err)
			os.Exit(1)
		}
		defer file.Close()
		for j:=0; j < len(b); j++ {
			curr = append(curr, b[j])
		}
	}
	err := ioutil.WriteFile(mergedFile, curr, 0644)
	if err != nil {
		fmt.Printf("[ERROR] %v\n", err)
		os.Exit(1)
	}
}