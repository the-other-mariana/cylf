package main

import(
	"fmt"
	"io/ioutil"
	"math"
	"strconv"
	"os"
	"strings"
)

func main(){
	pwd, _ := os.Getwd()
	targetFile := pwd + "/seberg-2019.mp4"
	fmt.Printf("file: %v", targetFile)

	
	file, err := os.Open(targetFile)
	if err != nil {
		fmt.Printf("[ERROR] %v\n", err)
		os.Exit(1)
	}

	defer file.Close()

	fileInfo, _ := file.Stat()
	var fileSize int64 = fileInfo.Size()
	const pieceSize = 95 * (1 << 20) // 99 MB

	numberOfPieces := uint64(math.Ceil(float64(fileSize) / float64(pieceSize)))
	fmt.Printf("[PROMPT] File will be cut into: %d pieces with size: %d bytes\n", numberOfPieces, pieceSize)
	
	for i := uint64(0); i < numberOfPieces; i++ {
		currSize := int(math.Min(pieceSize, float64(fileSize-int64(i*pieceSize))))
        currBuffer := make([]byte, currSize)
		file.Read(currBuffer)

		nameParts := strings.Split(targetFile, ".")
		filename := nameParts[len(nameParts) - 2]
		//extension := nameParts[len(nameParts) - 1]

		// create file in disk
		newFile := filename + "_" + strconv.FormatUint(i, 10) + ".cylf"
		_, err := os.Create(newFile)

		if err != nil {
			fmt.Printf("[ERROR] %v\n", err)
			os.Exit(1)
		}

		// save buffer bytes into the created file
		ioutil.WriteFile(newFile, currBuffer, os.ModeAppend)
		fmt.Printf("[SUCCESS] Piece: %v\n", newFile)
	}
	fmt.Println("[SUCCESS] file cut successfully")
}