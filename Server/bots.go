package main

import (
	"fmt"
	"math"
	"net/http"

	"github.com/gorilla/websocket"
)

type SendPacket struct {
	Track    Track      `json:"track"`
	Inputs   [7]float64 `json:"inputs"`
	Kind     string     `json:"kind"`
	Waypoint bool       `json:"waypoint-get"`
	Id       int        `json:"id"`
}

type ReceivePacket struct {
	Throttle float64 `json:"throttle"`
	Steer    float64 `json:"steer"`
	Breaking float64 `json:"breaking"`
	Id       int     `json:"id"`
}

func CheckOrigin(r *http.Request) bool {
	return true
}

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin:     CheckOrigin,
}

func (a *Actor) updatePosition(throttle, steer, breaking float64) {
	// Apply air resistance
	a.Vx = a.Vx * AIR_RESISTANCE
	a.Vy = a.Vy * AIR_RESISTANCE
	// Prevent divide by zero
	if a.Vx != 0 || a.Vy != 0 {
		// Apply breaks
		magnitude := math.Sqrt(a.Vx*a.Vx + a.Vy*a.Vy)
		a.Vx -= (a.Vx / magnitude) * breaking * BREAK_MULT
		a.Vy -= (a.Vy / magnitude) * breaking * BREAK_MULT
	}
	// Adjust heading
	steer = (steer - 0.5) * 2.0
	a.Heading += steer * STEER_MULT
	// Apply throttle
	a.Vx += math.Cos(a.Heading) * throttle * THROTTLE_MULT
	a.Vy += math.Sin(a.Heading) * throttle * THROTTLE_MULT
	a.Px += a.Vx
	a.Py += a.Vy
	a.Time += 1
}

func (a *Actor) reset(x, y float64) {
	a.Px = x
	a.Py = y
	a.Vx = 0
	a.Vy = 0
	a.Heading = 0
	a.Time = 0
}

func (s *Server) handle_bots(w http.ResponseWriter, r *http.Request) {
	// Upgrade connection
	conn, err := upgrader.Upgrade(w, r, nil)
	defer conn.Close()
	if err != nil {
		fmt.Printf("Failed opening web socket: %s\n", err)
		return
	}
	// Wait for user to request id
	var init = ReceivePacket{}
	if err = conn.ReadJSON(&init); err != nil {
		fmt.Printf("Failed to receive first packet: %s\n", err)
	}
	fmt.Printf("Init packet: %v\n", init)
	fmt.Printf("Started connection to %s\n", conn.RemoteAddr())
	id, connection := s.requestActor(Actor{}, init.Id)
	waypoint := 1
	// Start game
	for {
		// Generate track
		track := s.requestTrack(s.generations[id])
		course := SendPacket{
			Track:  track,
			Inputs: [7]float64{track.X[0], track.Y[0]},
			Kind:   "reset",
			Id:     id,
		}
		s.actors[id].reset(course.Track.X[0], course.Track.Y[0])
		// Send match start packet
		if err = conn.WriteJSON(course); err != nil {
			fmt.Printf("Failed to send message: %s\n", err)
			return
		}
		// Start event loop
		for {
			waypoint_get := false
			if connection != s.connection_num[id] {
				fmt.Printf("Two clients requested ID %d, evicted old one\n", id)
				return
			}
			actor := &s.actors[id]
			// Block on model sending update
			var received = ReceivePacket{}
			if err = conn.ReadJSON(&received); err != nil {
				fmt.Printf("Failed to read message: %s\n", err)
				return
			}
			fmt.Printf("Received packet: %v\n", received)
			// Calculate new position
			actor.updatePosition(received.Throttle, received.Steer, received.Breaking)
			// Check for waypoint get
			dx := track.X[waypoint] - actor.Px
			dy := track.Y[waypoint] - actor.Py
			distance := math.Sqrt(dx*dx + dy*dy)
			if distance <= DISTANCE_THRESH {
				waypoint += 1
				waypoint %= track.Length
				fmt.Printf("Got waypoint %d", waypoint)
				waypoint_get = true
			}

			if distance >= MAX_DISTANCE {
				fmt.Println("Exceeded max distance, resetting")
				break
			}

			// Advance to next game if time up
			if actor.Time >= GAME_TIME {
				break
			}
			var response = SendPacket{
				Inputs:   [7]float64{actor.Px, actor.Py, actor.Heading, actor.Vx, actor.Vy, track.X[waypoint], track.Y[waypoint]},
				Kind:     "update",
				Waypoint: waypoint_get,
				Id:       id,
			}
			// Send update packet
			if err = conn.WriteJSON(response); err != nil {
				fmt.Printf("Failed to send message: %s\n", err)
				return
			}
		} // </gameloop>
		// Wait for all actors to catch up
		s.generations[id] += 1
		gen := s.generations[id]
		fmt.Printf("Finished generation %d\n", gen)
		/*
				for {
					for i := 0; i < len(s.generations); i += 1 {
						if gen > s.generations[i] || (i == id && len(s.generations) > 1) {
							continue
						}
						goto escape
					}
				}
				// Start next generation
			escape:
		*/
	}
}
