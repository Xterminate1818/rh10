package main

import (
	"fmt"
	"net/http"
	"time"
)

func (s *Server) view(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		fmt.Printf("Failed opening web socket: %s\n", err)
		return
	}
	// Wait for connection
	for {
		if len(s.actors) != 0 {
			break
		}
	}
	last_track := s.track_generation
	for {
		time.Sleep(300 * time.Millisecond)
		var actor = s.actors[0]
		response := SendPacket{}
		if last_track != s.track_generation {
			response = SendPacket{
				Track:  s.track,
				Inputs: [8]float64{actor.Px, actor.Py, actor.Heading, actor.Vx, actor.Vy},
				Kind:   "reset",
			}
		} else {
			response = SendPacket{
				Inputs: [8]float64{actor.Px, actor.Py, actor.Heading, actor.Vx, actor.Vy},
				Kind:   "continue",
			}
		}
		if e := conn.WriteJSON(response); e != nil {
			fmt.Printf("Error in viewer: %s\n", e)
		}
	}

}
