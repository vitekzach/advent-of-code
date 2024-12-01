package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"regexp"
	"slices"
	"strconv"
)

const fileName = "input.txt"

func loadData() ([]int, []int) {
	var arr1 []int
	var arr2 []int

	whitespace := regexp.MustCompile(" +")

	file, err := os.Open(fileName)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		split := whitespace.Split(line, -1)
		val1, err := strconv.Atoi(split[0])
		if err != nil {
			log.Fatal(err)
		}
		val2, err := strconv.Atoi(split[1])
		if err != nil {
			log.Fatal(err)
		}
		arr1 = append(arr1, val1)
		arr2 = append(arr2, val2)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return arr1, arr2
}

func calculateDifferences(arr1, arr2 []int) int {
	var dist int

	slices.Sort(arr1)
	slices.Sort(arr2)

	if len(arr1) != len(arr2) {
		panic("Arrays are not the same length")
	}
	for idx, val := range arr1 {
		dist += int(math.Abs(float64(val - arr2[idx])))
	}
	return dist
}

func filterNumber(arr []int, num int) []int {
	var filtered []int

	for _, i := range arr {
		if i == num {
			filtered = append(filtered, i)
		}
	}
	return filtered
}

func calculateSimilarity(arr1, arr2 []int) int {
	var similarity int

	for _, num := range arr1 {
		similarity += num * len(filterNumber(arr2, num))
	}

	return similarity
}

func main() {
	arr1, arr2 := loadData()
	dist := calculateDifferences(arr1, arr2)
	fmt.Printf("Solution to part 1: %d\n", dist)

	similarity := calculateSimilarity(arr1, arr2)
	fmt.Printf("Solution to part 1: %d\n", similarity)

}
