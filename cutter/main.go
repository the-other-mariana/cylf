package main

import(
	"fmt"
	"io/ioutil"
	"math"
	"strconv"
	"os"
	"string"
)

func main(){
	targetFile := "./seberg.mp4"
	file, err := os.Open(targetFile)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	defer file.close()

	fileInfo, _ := file.Stat()
	var fileSize int64 = fileInfo.Size()
	const pieceSize = 99 * (1 << 20) // 99 MB

	numberOfPieces := uint64(math.Ceil(float64(fileSize) / float64(pieceSize)))
	fmt.Println("[PROMPT] File will be cut into %d pieces", numberOfPieces)
	
	for i := uint64(0); i < numberOfPieces; i++ {
		currSize := int(math.Min(fileChunk, float64(fileSize-int64(i*fileChunk))))
        currBuffer := make([]byte, partSize)
		file.Read(currBuffer)

		nameParts := string.Split(targetFile('.'))
		filename := nameParts[len(nameParts) - 2]
		extension := nameParts[len(nameParts) - 1]

		// create file in disk
		newFile := filename + "_" + strconv.FormatUint(i, 10) + ".cylf"
		_, err := os.Create(newFile)

		if err != nil {
			fmt.Println(err)
			os.Exit(1)
		}

		// save buffer bytes into the created file
		ioutil.WriteFile(newFile, currBuffer, os.ModeAppend)
		fmt.Println("[SUCCESS] Piece: %v", newFile)
	}
	fmt.Println("[SUCCESS] file cut successfully")
}