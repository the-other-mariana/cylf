# cylf

**`cylf`** will cut your files into binary chunks that can be re-merged together using only the name of the original file. 

> This comes in handy when a hosting service has file size limit in the files you upload: with cylf you cut them following the size limit so that upload is allowed, and then in any desired machine you dowload those pieces and merge them using cylf again!

# Run The Executables

- Inside `bin/` folder, you will find the folders that hold the two executables (cutter + merger) of the program. Currently **`cylf`** is available for:

    - Linux Ubuntu

    - Windows 10

## Linux

Open a terminal, go to the directory where the two executables and all the input files are located correctly, and type:

```
./cutter -n 95 -f <FILE_NAME.EXT>
```

or 

```
./merger -i <FOLDER_NAME_WITH_PARTS> -f <OUT_FILE_NAME.EXT>
```

depending on the action you want to do.

## Windows 10

Open a terminal, go to the directory where the two executables and all the input files are located correctly, and type:

```
start cutter.exe -n 95 -f <FILE_NAME.EXT>
```

or 

```
start merger -i <FOLDER_NAME_WITH_PARTS> -f <OUT_FILE_NAME.EXT>
```

depending on the action you want to do.

# Run The Source Code

- Go Version: `go1.18.3 linux/amd64`

Open a terminal and type: 

```
export GO111MODULE=off
```

in order to avoid error messages such as *package XXX is not in GOROOT" when building a Go project* or similar.

Then, go to `cutter/` folder if you want to split a file, and type:

```
go run cutter.go -n 95 -f seberg-2019.mp4
```

or to `merger/` folder if you have a bunch of `.cylf` files you want to merge back, and type:

```
go run merger.go -i seberg-2019 -f seberg-2019.mp4
```

![img](res/sc-v1.png)

### To Cross Compile (Linux -> Win10)

Type on the terminal:

```
GOOS=windows GOARCH=amd64 go build cutter.go
```