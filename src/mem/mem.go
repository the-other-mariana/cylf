package mem

// taken from https://gist.github.com/j33ty/79e8b736141be19687f565ea4c6f4226

import (
    "runtime"
    "fmt"
)

func PrintMemUsage() {
	var m runtime.MemStats
	runtime.ReadMemStats(&m)
	// For info on each, see: https://golang.org/pkg/runtime/#MemStats
	fmt.Printf("Alloc = %v MiB | %.2f MB", bToMb(m.Alloc), float64(bToMb(m.Alloc))*1.049)
	fmt.Printf("\tTotalAlloc = %v MiB | %.2f MB", bToMb(m.TotalAlloc), float64(bToMb(m.TotalAlloc))*1.049)
	fmt.Printf("\tSys = %v MiB | %.2f MB", bToMb(m.Sys), float64(bToMb(m.Sys))*1.049)
	fmt.Printf("\tNumGC = %v | %.2f MB\n", m.NumGC, float64(m.NumGC)*1.049)
}

func bToMb(b uint64) uint64 {
    return b / 1024 / 1024
}