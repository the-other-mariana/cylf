package main

import(
	"fmt"
	"io/ioutil"
	"math"
	"strconv"
	"os"
	"strings"
	"flag"
	"path/filepath"
	"./mem"
)

/* last version: appends b as a whole to file */

func cut(name string, mb *int){
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

	// calculate the number of bytes from MB input
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

	// make i buffers of n bytes and store each piece
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

func merge(name, folder string){
	fmt.Println("[RESOURCES]")
	fmt.Println("Start Memory:")
	mem.PrintMemUsage()
	nameParts := strings.Split(name, ".")
	filename := nameParts[len(nameParts) - 2]
	baseFilename := "./" + folder + "/" + filename
	extension := nameParts[len(nameParts) - 1]
	fmt.Printf("[PROMPT] File: %v-merged.%v\n", baseFilename, extension)

	// get the future merged file name
	mergedFile := "./" + filename + "-merged"+ "." + extension

	// find total of .cylf files in input folder
	pattern := filepath.Join("./" + folder, "*.cylf")
	pieces, _ := filepath.Glob(pattern)
	fmt.Printf("[SUCCESS] Files found: %v\n", len(pieces))
	numberOfPieces := uint64(len(pieces))

	// variable to store the accumulated bytes of every piece processed
	var accSize int64 = 0
	//var curr []byte
	for i := uint64(0); i < numberOfPieces; i++ {
		currFile := baseFilename + "_" + strconv.FormatUint(i, 10) + ".cylf"
		file, err := os.Open(currFile)
		fileInfo, _ := file.Stat()
		accSize += fileInfo.Size()
		if err != nil {
			fmt.Printf("[ERROR] %v\n", err)
			os.Exit(1)
		}
		defer file.Close()
		
	}
	//bArray := make([]byte, accSize, accSize)
	var t int64 = 0
	for i := uint64(0); i < numberOfPieces; i++ {
		currFile := baseFilename + "_" + strconv.FormatUint(i, 10) + ".cylf"
		file, err := os.Open(currFile)
		if err != nil {
			fmt.Printf("[ERROR] %v\n", err)
			os.Exit(1)
		}
		defer file.Close()
		fileInfo, _ := file.Stat()
		var fileSize int64 = fileInfo.Size()
		//b := make([]byte, fileSize)
		// send byte array of current file to b variable
		//file.Read(bArray[t:t+fileSize])
		b := make([]byte, fileSize)
		// send byte array of current file to b variable
		file.Read(b)
		f, err := os.OpenFile(mergedFile, os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0666)
		if err != nil {
			fmt.Println(err)
			return
		}
		defer f.Close()
		_, err1 := f.Write(b)
		if err1 != nil {
			fmt.Println(err1)
			return
		}
		t += fileSize
		mem.PrintMemUsage()
	}
	// store the accumulated bytes into a file
	//err := ioutil.WriteFile(mergedFile, bArray, 0644)
	fmt.Println("End Memory:")
	mem.PrintMemUsage()
	/*
	if err != nil {
		fmt.Printf("[ERROR] %v\n", err)
		os.Exit(1)
	}*/
}

func main(){
	var action string
	var name string
	var folder string
	// numeric vars
	mb := flag.Int("n", 10, "limit file size (MB)")
	// string vars
	flag.StringVar(&action, "a", "cut", "action: 'cut' or 'merge'")
	flag.StringVar(&name, "f", "default", "filenameto to work on")
	flag.StringVar(&folder, "i", "default", "folder where file parts are")
	flag.Parse()

	if action == "cut" {
		cut(name, mb)
	} else if action == "merge" {
		merge(name, folder)
	}
}