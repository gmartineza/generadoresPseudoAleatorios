package main

import (
	"fmt"
	"math"
	"strconv"
	"time"
)

func destripador(xCuadrado int, d int) int64 {
	x := strconv.Itoa(xCuadrado)
	indiceIzq := ((len(x) - d) / 2)
	resultado, _ := strconv.Atoi(x[indiceIzq : indiceIzq+d])
	return int64(resultado)
}

func loopDeNoSeQuePonerle(x1 int64) int64 {
	xCuadrado := int(math.Pow(float64(x1), 2))

	return destripador(xCuadrado, 4)
}

func main() {
	x1 := time.Now().UnixMilli() % 1000
	xNuevo := loopDeNoSeQuePonerle(x1)
	var relustado string
	for i := 0; i < 5; i++ {
		xNuevo = loopDeNoSeQuePonerle(xNuevo)
		relustado += strconv.Itoa(int(xNuevo))
	}

	fmt.Printf("%s", relustado)
}
