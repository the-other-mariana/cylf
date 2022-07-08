# cylf

cylf will cut your files into binary chunks that can be re-merged together using only the name of the original file. 

- This comes in handy when a host has file size limit in the files you upload, so with cylf you cut them so that you can upload and download them somewhere else, and then use cylf again to merge back the downloaded files into 1 file on your machine!

# Run The Code

- Go Version: `go1.18.3 linux/amd64`

Open a terminal and type: 

```
export GO111MODULE=off
```


then, go to `cutter/` folder if you want to split a file or to `merger/` folder if you have a bunch of `.cylf` files you want to merge back, and type on the terminal:

```
go run main.go
```