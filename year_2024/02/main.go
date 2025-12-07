package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

const inputFile = "input.txt"
const minDiff = 1
const maxDiff = 3

func getReports() [][]int {
	file, err := os.Open(inputFile)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	var reports [][]int

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		lineStrings := strings.Split(line, " ")
		var lineInts []int
		for _, s := range lineStrings {
			parsedInt, err := strconv.Atoi(s)
			if err != nil {
				log.Fatal(err)
			}
			lineInts = append(lineInts, parsedInt)
		}
		reports = append(reports, lineInts)
	}

	return reports
}

func removeIndex(s []int, index int) []int {
	ret := make([]int, 0)
	ret = append(ret, s[:index]...)
	return append(ret, s[index+1:]...)
}

func isReportSafe(report []int, mistakeTolerance bool) bool {
	var multiplier int
	if report[0] > report[1] {
		multiplier = -1
	} else if report[0] < report[1] {
		multiplier = 1
	} else {
		multiplier = 0
	}

	for i := 0; i < len(report)-1; i++ {
		diff := report[i+1] - report[i]
		if !numbersSafe(diff, multiplier) {
			if mistakeTolerance {
				for toRemove := range len(report) {
					withRemoved := removeIndex(report, toRemove)
					if isReportSafe(withRemoved, false) {
						return true
					}
				}
				return false
			} else {
				return false
			}
		}
	}
	return true
}

func numbersSafe(diff int, mutliplier int) bool {
	if mutliplier == 0 {
		return false
	}

	if math.Abs(float64(diff)) < minDiff || math.Abs(float64(diff)) > maxDiff || diff*mutliplier <= 0 {
		return false
	}
	return true
}

func calculateSafeReportCount(reports [][]int, mistakeTolerance bool) int {
	safeReports := 0
	for _, report := range reports {
		if isReportSafe(report, mistakeTolerance) {
			safeReports += 1
		}
	}
	return safeReports
}

func main() {
	reports := getReports()
	safeReportsCounts := calculateSafeReportCount(reports, false)
	fmt.Printf("Part 1 solution: %d\n", safeReportsCounts)

	safeReportsCountsPart2 := calculateSafeReportCount(reports, true)
	fmt.Printf("Part 2 solution: %d\n", safeReportsCountsPart2)
}
