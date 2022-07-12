package main

import(
	"fmt"
	"io/ioutil"
	"math"
	"strconv"
	"os"
	"strings"
	"flag"
)

func main(){
	// input flags: file size limit, filename
	mb := flag.Int("n", 10, "limit file size (MB)")
	var name string
	flag.StringVar(&name, "f", "default", "filename to cut")
	flag.Parse()

	pwd, _ := os.Getwd()
	targetFile := pwd + "/" + name
	fmt.Printf("file: %v\n", targetFile)

	
	file, err := os.Open(targetFile)
	if err != nil {
		fmt.Printf("[ERROR] %v\n", err)
		os.Exit(1)
	}

	defer file.Close()

	fileInfo, _ := file.Stat()
	var fileSize int64 = fileInfo.Size()
	var pieceSize = uint64(*mb) * (1 << 20) 

	numberOfPieces := uint64(math.Ceil(float64(fileSize) / float64(pieceSize)))
	fmt.Printf("[PROMPT] File will be cut into: %d pieces with size: %d bytes\n", numberOfPieces, pieceSize)

	// create folder
	folderParts := strings.Split(name, ".")
	folderName := folderParts[len(folderParts) - 2]
	err = os.Mkdir(folderName, 0755)
	if err != nil {
		fmt.Printf("[ERROR] %v\n", err)
		os.Exit(1)
	}
	
	for i := uint64(0); i < numberOfPieces; i++ {
		currSize := int(math.Min(float64(pieceSize), float64(fileSize-int64(i*pieceSize))))
        currBuffer := make([]byte, currSize)
		file.Read(currBuffer)

		// create file in disk
		newFile := pwd + "/" + folderName + "/" + folderName + "_" + strconv.FormatUint(i, 10) + ".cylf"
		_, err := os.Create(newFile)

		if err != nil {
			fmt.Printf("[ERROR] %v\n", err)
			os.Exit(1)
		}

		// save buffer bytes into the created file
		ioutil.WriteFile(newFile, currBuffer, os.ModeAppend)
		fmt.Printf("[SUCCESS] Piece %v/%v: %v\n", i+1, numberOfPieces, newFile)
	}
	fmt.Println("[SUCCESS] File cut successfully")
}