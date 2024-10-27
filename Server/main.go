package main

import (
	"fmt"
	"math"
	"math/rand/v2"
	"net/http"
	"sync"
)

// Track params
const TRACK_MEAN_RADIUS = 140.0
const TRACK_STD_DEVIATION = 40.0
const TRACK_SEGMENTS = 10

// Physics params
const AIR_RESISTANCE = 0.95
const STEER_MULT = 1.5
const THROTTLE_MULT = 1.0
const BREAK_MULT = 1.0
const DISTANCE_THRESH = 10.0

// Time steps before reset
const GAME_TIME = 5000
const MAX_DISTANCE = 200.0

// Do not edit
const CANVAS_ORIGIN_X = 400.0 - TRACK_MEAN_RADIUS
const CANVAS_ORIGIN_Y = 400.0 - TRACK_MEAN_RADIUS

type Actor struct {
	Px      float64
	Py      float64
	Vx      float64
	Vy      float64
	Heading float64
	Time    int
	check   int
}
type Server struct {
	actors           map[int]*Actor
	generations      map[int]int
	track            Track
	track_generation int
	connection_num   []int
	append_lock      sync.Mutex
}

func (s *Server) requestActor(a Actor, id int) int {
	s.append_lock.Lock()
	defer s.append_lock.Unlock()
	s.actors[id] = &a
	s.generations[id] = 0
	return id
}

func (s *Server) requestTrack(id int) Track {
	s.append_lock.Lock()
	defer s.append_lock.Unlock()
	if s.track_generation != id {
		s.track_generation = id
		s.track = generate_track()
	}
	return s.track
}

type Track struct {
	X      []float64 `json:"x"`
	Y      []float64 `json:"y"`
	Length int       `json:"length"`
}

func generate_track() Track {
	x_arr := make([]float64, TRACK_SEGMENTS)
	y_arr := make([]float64, TRACK_SEGMENTS)
	for i := 0; i < TRACK_SEGMENTS; i++ {
		theta := (float64(i) / float64(TRACK_SEGMENTS)) * math.Pi * 2
		r := (rand.NormFloat64() * TRACK_STD_DEVIATION) + TRACK_MEAN_RADIUS
		x := r*math.Cos(theta) + CANVAS_ORIGIN_X
		y := r*math.Sin(theta) + CANVAS_ORIGIN_Y
		x_arr[i] = x
		y_arr[i] = y
	}
	return Track{X: x_arr, Y: y_arr, Length: TRACK_SEGMENTS}
}

func index(w http.ResponseWriter, r *http.Request) {
	http.ServeFile(w, r, "./index.html")
}

func main() {
	s := Server{
		track:       generate_track(),
		actors:      make(map[int]*Actor),
		generations: make(map[int]int),
	}
	files := http.FileServer(http.Dir("./"))
	http.Handle("/", files)
	http.HandleFunc("/view", s.view)
	http.HandleFunc("/bots", s.handle_bots)
	fmt.Println("Listening on 192.168.0.20:8080")
	err := http.ListenAndServe("0.0.0.0:8080", nil)
	if err != nil {
		panic(err)
	}
}
