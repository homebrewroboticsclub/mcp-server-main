Based on https://github.com/lpigeon/ros-mcp-server

Functionality revised to match the specifics of the Baby Brewie

# Baby Brewie Powered by LLM

We’re turning the robot into an intuitive and accessible tool using the MCP server!

## Key Updates

### Updated ROS connection method.
Fixed bugs related to method calls via WebSocket.
The WebSocket manager was rewritten based on the roslibPY library using standard methods, for example:
```python
topic = roslibpy.Topic(self.ws, topic, topic_data_type)
```
Using JSON instead of standard network interaction
```python
# Ensure message is JSON serializable
json_msg = json.dumps(message)
self.ws.send(json_msg)
```
### A voice agent has been added for seamless control.
The voice agent is separated into its own Python file — voice_agent.py — and can be launched both on the robot itself and on a separate station.

Voice activation using the command “AiNex” was trained using the Porcupine Wake Word Python API.
Models have been prepared for running on both a Windows PC and the robot's Raspberry Pi 5.
* Ai-Nex_en_raspberry-pi_v3_0_0.ppn
* Ai-ex_en_windows_v3_0_0.ppn

During setup, specify the version appropriate for your chosen platform.

The Wake Word enables prompt response to user commands while using minimal resources.

After activation, the robot records and recognizes the spoken command using the SpeechRecognition package.

Next, the textual interpretation of the user's request is sent to the LLM. A system prompt is formed in advance, and optionally, the chat history is saved for context (history_active flag). Voice recognition can be disabled, and text chat mode can be selected using the text_input flag (true to disable voice input).

Interaction with the LLM is carried out via the Together API (https://together.ai/); you can choose any model available with your API key.

Responses are voiced using gTTS.

To reduce latency, responses that have already been spoken during the session are cached.
A hash of the LLM response is checked, and if it’s found in the cache, the local audio file is played instead.


### MCP passes to the LLM context the Action group files created in the native AiNex application.
Now the LLM can access files with robot actions (ActionGroups) previously created in the editor and call them according to the context. For this, a tool get_available_actions() is implemented in the MCP server.

### Additional MCP tools
* The get_image() function has been changed to work on a desktop and save the image to Downloads.
* Added function make_step(x: float, z: float): In accordance with the AiNex robot control model via joystick.
* Added function run_action(action_name: str): to call previously requested actions by name.

It is important to give prepared actions clear names for adequate context perception by the LLM. If everything is done correctly, the AI will be able to call the required action by description or situation, without requiring the user to specify the exact name.

## You will need API keys!

For https://together.ai/ and https://console.picovoice.ai/ (for quick voice activation). Fortunately, you can get them for free by signing up.

Keys are passed via environment variables at startup.

## Quick Start

Run the file ROS/action_groups.py on the robot to publish the current actions, first on the robot, then in docker

```bash
docker cp action_groups.py ainex:/home/ubuntu/ros_ws/src
```

Now, on the robot or desktop, deploy the MCP server (the desktop must be on the same network as the robot, or you will need to connect a microphone to the robot. If necessary, adjust the ROS IP for network operation).

MCP communicates with the agent via STDIO, so it is enough to launch the voice agent, and it will start the server itself.

For convenient package installation, UV is used.

To start everything, use the template bat file, adding your API keys to it

```bash
set TOGETHER_API_KEY=Your key
set WAKEUP_API_KEY=Your key
uv run voice_agent.py
```

On the first run, the necessary packages will be installed.

Now you are ready to unlock your robot in a new way with LLM!
