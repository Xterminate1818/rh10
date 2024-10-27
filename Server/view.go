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
	response := SendPacket{
		Track:  s.track,
		Inputs: [7]float64{},
		Kind:   "reset",
	}
	if e := conn.WriteJSON(response); e != nil {
		fmt.Printf("Error in viewer: %s\n", e)
	}

	// Wait for connection
	for {
		if len(s.actors) != 0 {
			break
		}
	}
	last_track := s.track_generation
	for {
		time.Sleep(50 * time.Millisecond)
		var actor = s.actors[0]
		response := SendPacket{}
		if last_track != s.track_generation {
			response = SendPacket{
				Track:  s.track,
				Inputs: [7]float64{actor.Px, actor.Py, actor.Heading, actor.Vx, actor.Vy},
				Kind:   "reset",
			}
		} else {
			response = SendPacket{
				Inputs: [7]float64{actor.Px, actor.Py, actor.Heading, actor.Vx, actor.Vy},
				Kind:   "continue",
			}
		}
		if e := conn.WriteJSON(response); e != nil {
			fmt.Printf("Error in viewer: %s\n", e)
		}
	}

}
