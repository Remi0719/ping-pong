
# Gesture-Controlled Ping Pong Game

A modern take on the classic Ping Pong game using computer vision and hand gesture controls. Players use their hands to control paddles in real-time through their webcam.

## 🎮 Features

- Real-time hand gesture controls
- Smooth paddle movement
- Dynamic ball physics
- Score tracking
- Winner announcement
- Adjustable game parameters
- Fingertip tracking visualization

## 🛠️ Prerequisites

- Python 3.8 or higher
- Webcam
- Good lighting conditions
- Sufficient space for hand movements

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/gesture-ping-pong.git
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## 🎯 How to Play

1. Run the game:
```bash
python app.py
```

2. Position yourself in front of the webcam
3. Use your hands to control the paddles:
   - Left hand controls the left paddle
   - Right hand controls the right paddle
   - Move hands up and down to move paddles
4. Hit the orange ball with the green paddles
5. First player to reach 5 points wins
6. Press 'q' to quit the game

## 🎛️ Controls

- **Left Paddle**: Move left hand up/down on the left side of the camera
- **Right Paddle**: Move right hand up/down on the right side of the camera
- **Quit Game**: Press 'q' key

## 💡 Tips for Better Gameplay

1. Stand about 2-3 feet away from the camera
2. Ensure good lighting conditions
3. Keep both hands visible to the camera
4. Spread your fingers for better hand detection
5. Watch the green dots for finger tracking feedback

## 🔧 Customization

Game parameters can be adjusted in `srcpingpong/game.py`:
- Window dimensions
- Ball speed and size
- Paddle size
- Maximum score
- Hand tracking sensitivity

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenCV for computer vision capabilities
- MediaPipe for hand tracking technology
