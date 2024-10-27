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
        self.x_pos = 0
        self.y_pos = 0
        self.heading = 0
        self.vel_x = 0
        self.vel_y = 0
        self.targ_x = 0
        self.targ_y = 0
        self.id = -1
        self.websocket = None                   #Buffer for the websocket obj
        self.loop = asyncio.get_event_loop()    #Establish async loop for websocket operations

        # Connect to WebSocket Server Asynchronously
        self.loop.run_until_complete(self.connect_to_server('ws://192.168.0.20:8080/bots'))
        
        # Send Init Packet
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

    def step(self, action):
        print(f"id {self.id}")

        #SEND ACTIONS FIRST
        throttle, steer, braking = action
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

        self.observation = [self.x_pos, self.y_pos, self.heading, self.vel_x, self.vel_y, self.targ_x, self.targ_y]
        self.observation = np.array(self.observation)

        self.info = {
            "TimeLimit.truncated": self.truncated,  # Add this line
            "id": self.id  # You can add other relevant info as needed
        }

        self.truncated = False

        if self.render_mode == "human":
            self.render()

        self.reward = 0

        return self.observation, self.reward, self.terminated, self.truncated, self.info

    def reset(self, seed=None, options=None):
        print("reset")

        server_response = '{"track":{"x":[253.73350286732244,232.65372999676703,185.78904340692844,114.54893270390353,51.607027149532,22.6053371974956,35.54465128765794,115.9841565350986,163.20853281635732,220.24615269032782],"y":[150,210.05144994092365,260.1473497047542,259.1071661924882,221.48667923274186,150.00000000000003,66.84332160279989,45.30999856494262,109.34831600085795,98.96318264171863],"length":10},"inputs":[253.73350286732244,150,0,0,0,0,0],"kind":"reset","waypoint-get":false,"id":3}'
        if self.dontREAD == 0:
            self.dontREAD = 1
        else:
            server_response = self.loop.run_until_complete(self.receive_packet())
            data = json.loads(server_response)   

            self.x_pos = data.get("inputs", [0])[0]
            self.y_pos = data.get("inputs", [0])[1]
            self.heading = data.get("inputs", [0])[2]
            self.vel_x = data.get("inputs", [0])[3]
            self.vel_y = data.get("inputs", [0])[4]
            self.targ_x = data.get("inputs", [0])[5]
            self.targ_y = data.get("inputs", [0])[6]
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
