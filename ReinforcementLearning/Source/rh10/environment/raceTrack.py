import gymnasium as gym
from gymnasium import spaces
import random
import numpy as np
import pygame
from typing import Optional
from collections import deque
from pathlib import Path
import asyncio
import websockets
import json
import math

class RaceTrack(gym.Env):
    metadata = {
        "render_modes": [
            "human",
            "rgb_array",
            "state_pixels",
        ],
        "render_fps": 50,
    }

    def __init__(self, dbg_report_dir: Optional[str] = None, render_run_str: Optional[str] = "Evaluation", render_mode: Optional[str] = "human"):
        super(RaceTrack, self).__init__()
        self.render_mode = render_mode
        self.run_name = render_run_str
        self.screen: Optional[pygame.Surface] = None
        self.clock = None
        
        print("init")
        self.dontREAD = 0
        self.resetFLAG = 0
        self.x_pos = 0
        self.y_pos = 0
        self.heading = 0
        self.vel_x = 0
        self.vel_y = 0
        self.targ_x = 0
        self.targ_y = 0
        self.previous_distance = 0
        self.previous_target_x = 0
        self.previous_target_y = 0
        self.id = -1
        self.websocket = None                   #Buffer for the websocket obj
        self.loop = asyncio.get_event_loop()    #Establish async loop for websocket operations

        # Connect to WebSocket Server Asynchronously
        print("CONECTING TO SERVER")
        self.loop.run_until_complete(self.connect_to_server('ws://localhost:8080/bots'))
        
        # Send Init Packet
        print("SENDING INIT PACKET")
        self.loop.run_until_complete(self.send_packet())
        
        self.truncated = False

        self.action_space = spaces.Box(
            low=np.array([0.0, 0.0, 0.0]),  # Min: throttle=0.0, steer=-1.0 (full left), breaking=0.0
            high=np.array([1.0, 1.0, 1.0]), # Max: throttle=1.0 (full), steer=1.0 (full right), breaking=1.0 (full brake)
            dtype=np.float32
        )
        self.observation_space = spaces.Box(low=-750, high=750, shape=(7,), dtype=np.int64)  # Update shape accordingly

    async def connect_to_server(self, server):
        try:
            self.websocket = await websockets.connect(server)
            print(f"Connected to {server}")
        except Exception as e:
            print(f"Failed to connect to server: {e}")

    async def send_packet(self, throttle=0.0, steer=0.0, braking=0.0, id=-1):
        if self.websocket:
            await self.websocket.send(json.dumps({"throttle": float(throttle), "steer": float(steer), "breaking": float(braking), "id": id}))
        else:
            print("WEBSOCKET LOST")

    async def receive_packet(self):
        if self.websocket:
            return await self.websocket.recv()
        else:
            print("WEBSOCKET LOST")

    def calculate_reward(self, x_pos, y_pos, target_x, target_y, prev_distance, previous_target_x, previous_target_y):
        # Calculate the current distance to the target
        current_distance = math.sqrt((target_x - x_pos)**2 + (target_y - y_pos)**2)
        
        # Calculate change in distance
        distance_change = prev_distance - current_distance  # Positive if getting closer, negative if further away
        
        # Reward based on change in distance
        distance_reward = -1  # You can scale this reward if necessary

        # Reward for target position change
        if (target_x != previous_target_x) or (target_y != previous_target_y):
            target_change_reward = 2.0  # Reward for target position change
        else:
            target_change_reward = 0.0  # No reward if target position hasn't changed

        # Combine the rewards (adjust weighting as necessary)
        total_reward = distance_reward + target_change_reward  # Sum all rewards

        self.previous_target_x = self.targ_x
        self.previous_target_y = self.targ_y
        self.previous_distance = current_distance

        return total_reward

    def step(self, action):
        #print(f"id {self.id}")

        #SEND ACTIONS FIRST
        throttle, steer, braking = action
        #print(f"throttle: {throttle}, steer: {steer}, braking: {braking}")
        self.loop.run_until_complete(self.send_packet(throttle=throttle, steer=steer, braking=braking, id=self.id))

        #THEN PARSE NEW ENV STATE
        server_response = self.loop.run_until_complete(self.receive_packet())

        data = json.loads(server_response)

        self.x_pos = data.get("inputs", [0])[0]
        self.y_pos = data.get("inputs", [0])[1]
        self.heading = data.get("inputs", [0])[2]
        self.vel_x = data.get("inputs", [0])[3]
        self.vel_y = data.get("inputs", [0])[4]
        self.targ_x = data.get("inputs", [0])[5]
        self.targ_y = data.get("inputs", [0])[6]

        if data.get("kind") == "reset":
            print("RESET RECEIVED")
            self.resetFLAG = 1
            self.terminated = True

        self.observation = [self.x_pos, self.y_pos, self.heading, self.vel_x, self.vel_y, self.targ_x, self.targ_y]
        self.observation = np.array(self.observation)

        self.info = {
            "TimeLimit.truncated": self.truncated,  # Add this line
            "id": self.id  # You can add other relevant info as needed
        }

        self.truncated = False

        if self.render_mode == "human":
            self.render()

        self.reward = self.calculate_reward(self.x_pos, self.y_pos, self.targ_x, self.targ_y, self.previous_distance, self.previous_target_x, self.previous_target_y)

        return self.observation, self.reward, self.terminated, self.truncated, self.info

    def reset(self, seed=None, options=None):
        print("reset")
        #print(f"DONTREAD: {self.dontREAD}")
        server_response = '{"track":{"x":[253.73350286732244,232.65372999676703,185.78904340692844,114.54893270390353,51.607027149532,22.6053371974956,35.54465128765794,115.9841565350986,163.20853281635732,220.24615269032782],"y":[150,210.05144994092365,260.1473497047542,259.1071661924882,221.48667923274186,150.00000000000003,66.84332160279989,45.30999856494262,109.34831600085795,98.96318264171863],"length":10},"inputs":[253.73350286732244,150,0,0,0,0,0],"kind":"reset","waypoint-get":false,"id":3}'
        if self.dontREAD == 0:
            server_response = self.loop.run_until_complete(self.receive_packet())
            data = json.loads(server_response)            
            self.id = data.get("id")
            if self.websocket:
                self.websocket.close() #MAYBE THIS
            self.dontREAD = 1
        elif self.resetFLAG == 1:
            self.resetFLAG = 0
        else:
            server_response = self.loop.run_until_complete(self.receive_packet())
            data = json.loads(server_response)   

            self.x_pos = data.get("inputs", [0])[0]
            self.y_pos = data.get("inputs", [0])[1]
            self.heading = data.get("inputs", [0])[2]
            self.vel_x = data.get("inputs", [0])[3]
            self.vel_y = data.get("inputs", [0])[4]
            self.targ_x = data.get("inputs", [0])[5]
            self.previous_target_x = self.targ_x
            self.targ_y = data.get("inputs", [0])[6]
            self.previous_target_y = self.targ_y
            self.previous_distance = math.sqrt((self.targ_x - self.x_pos)**2 + (self.targ_y - self.y_pos)**2)
            self.id = data.get("id")

        self.terminated = False
        self.reward = 0    

        self.observation = [self.x_pos, self.y_pos, self.heading, self.vel_x, self.vel_y, self.targ_x, self.targ_y]
        self.observation = np.array(self.observation)

        if self.render_mode == "human":
            self.render()
            
        self.info = {
            "id": self.id,  # Include other relevant info as needed
        }

        return self.observation, self.info

    def close(self):
        print("CLOSE RAN")
        if self.websocket:
            self.loop.run_until_complete(self.websocket.close())
        return super().close()

    def render(self):
        if self.render_mode is None:
            assert self.spec is not None
            gym.logger.warn(
                "You are calling render method without specifying any render mode."
                "You can specify the render_mode at initialization,"
                f'e.g. gym.make("{self.spec.id}", render_mode="rgb_array")'
            )
            return
        else:
            return self._render(self.render_mode)
        
    def _render(self, mode: str):
        assert mode in self.metadata["render_modes"]
        # Your rendering logic remains unchanged...
