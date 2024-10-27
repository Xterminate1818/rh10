package main

import (
	"fmt"
	"net/http"
	"time"
)

type ViewPacket struct {
	Track  Track     `json:"track"`
	X      []float64 `json:"x"`
	Y      []float64 `json:"y"`
	R      []float64 `json:"r"`
	Id     []int     `json:"id"`
	Length int       `json:"length"`
}

func (s *Server) view(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	first := true
	last_track := s.track_generation
	for {
		x := make([]float64, 0)
		y := make([]float64, 0)
		r := make([]float64, 0)
		i := make([]int, 0)
		for k, v := range s.actors {
			x = append(x, v.Px)
			y = append(y, v.Py)
			r = append(r, v.Heading)
			i = append(i, k)
		}
		length := len(s.actors)
		time.Sleep(50 * time.Millisecond)
		response := ViewPacket{}
		if last_track != s.track_generation || first {
			response = ViewPacket{
				Track:  s.track,
				X:      x,
				Y:      y,
				R:      r,
				Id:     i,
				Length: length,
			}
		} else {
			response = ViewPacket{
				X:      x,
				Y:      y,
				R:      r,
				Id:     i,
				Length: length,
			}
		}
		first = false
		if e := conn.WriteJSON(response); e != nil {
			fmt.Printf("Error in viewer: %s\n", e)
		}
	}

}
