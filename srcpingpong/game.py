import cv2

import numpy as np
import os

import mediapipe as mp  # Fixed import statement


class PingPongGame:

    def __init__(self):
        # Initialize MediaPipe hands with warning suppression
        import logging
        logging.getLogger('mediapipe').setLevel(logging.ERROR)
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            model_complexity=0,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.5
        )
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("Could not open camera. Please check if camera is connected.")
        
        # Game parameters first
        self.window_width = 1280
        self.window_height = 720
        self.palm_height = 140
        self.palm_width = 25
        self.ball_size = 20
        self.ball_speed = 8
        self.max_ball_speed = 15
        self.max_score = 5
        self.palm_smoothing = 0.8
        
        # Then initialize game state
        self.score_left = 0
        self.score_right = 0
        self.left_palm_pos = self.window_height//2
        self.right_palm_pos = self.window_height//2
        
        # Initialize ball position and direction
        self.reset_game()

    def update_game_state(self):
        # Update ball speed with gentler acceleration
        self.ball_speed = min(8 + max(self.score_left, self.score_right) * 0.5, self.max_ball_speed)
        # Update ball position
        self.ball_pos[0] += self.ball_speed * self.ball_dir[0]
        self.ball_pos[1] += self.ball_speed * self.ball_dir[1]
        
        # Ball collision with top and bottom
        if self.ball_pos[1] <= 0 or self.ball_pos[1] >= self.window_height:
            self.ball_dir[1] *= -1
        
        # Ball collision with left palm
        if self.ball_pos[0] <= self.palm_width + 30:
            if abs(self.ball_pos[1] - self.left_palm_pos) < self.palm_height//2:
                self.ball_dir[0] *= -1
                self.score_left += 1
            else:
                self.reset_game()
                self.score_right += 1
        
        # Ball collision with right palm
        if self.ball_pos[0] >= self.window_width - (self.palm_width + 30):
            if abs(self.ball_pos[1] - self.right_palm_pos) < self.palm_height//2:
                self.ball_dir[0] *= -1
                self.score_right += 1
            else:
                self.reset_game()
                self.score_left += 1

        # Check for winner
        if self.score_left >= self.max_score:
            self.show_winner("Left Player")
        elif self.score_right >= self.max_score:
            self.show_winner("Right Player")

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (self.window_width, self.window_height))
            
            self.detect_paddles(frame)
            self.update_game_state()
            
            game_frame = np.zeros((self.window_height, self.window_width, 3), dtype=np.uint8)
            
            # Draw palm areas
            cv2.circle(game_frame, (self.palm_width, self.left_palm_pos), 30, (0, 255, 0), -1)
            cv2.circle(game_frame, (self.window_width - self.palm_width, self.right_palm_pos), 30, (0, 255, 0), -1)
            
            # Draw ball as simple circle
            cv2.circle(game_frame, (int(self.ball_pos[0]), int(self.ball_pos[1])), 
                      self.ball_size, (0, 165, 255), -1)  # Orange ball
            
            final_frame = cv2.addWeighted(frame, 0.3, game_frame, 0.7, 0)
            
            # Display scores
            cv2.putText(final_frame, f'{self.score_left}', (50, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
            cv2.putText(final_frame, f'{self.score_right}', (self.window_width - 80, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
            
            cv2.imshow('Ping Pong', final_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()

    def reset_game(self):
        self.ball_pos = [self.window_width//2, self.window_height//2]
        self.ball_dir = [1 if np.random.random() > 0.5 else -1, 
                        1 if np.random.random() > 0.5 else -1]

    def show_winner(self, winner):
        end_frame = np.zeros((self.window_height, self.window_width, 3), dtype=np.uint8)
        cv2.putText(end_frame, f"{winner} Wins!", 
                   (self.window_width//2 - 200, self.window_height//2),
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        cv2.imshow('Ping Pong', end_frame)
        cv2.waitKey(3000)
        self.cap.release()
        cv2.destroyAllWindows()
        exit()

    def detect_paddles(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            frame_height, frame_width, _ = frame.shape
            left_hand_y = None
            right_hand_y = None
            
            for hand_landmarks in results.multi_hand_landmarks:
                # Get all finger landmarks
                fingers_y = [hand_landmarks.landmark[i].y for i in [4, 8, 12, 16, 20]]
                palm_y = sum(fingers_y) / len(fingers_y)
                x = int(hand_landmarks.landmark[9].x * frame_width)
                y = int(palm_y * frame_height)
                
                # Draw hand landmarks
                for i in [4, 8, 12, 16, 20]:
                    fx = int(hand_landmarks.landmark[i].x * frame_width)
                    fy = int(hand_landmarks.landmark[i].y * frame_height)
                    cv2.circle(frame, (fx, fy), 5, (0, 255, 0), -1)
                
                if x < frame_width//2:
                    left_hand_y = y
                else:
                    right_hand_y = y
            
            # Update palm positions with smoothing
            if left_hand_y is not None:
                self.left_palm_pos = int(self.palm_smoothing * self.left_palm_pos + 
                                       (1 - self.palm_smoothing) * left_hand_y)
            if right_hand_y is not None:
                self.right_palm_pos = int(self.palm_smoothing * self.right_palm_pos + 
                                        (1 - self.palm_smoothing) * right_hand_y)