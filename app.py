from srcpingpong.game import PingPongGame

def main():
    try:
        game = PingPongGame()
        game.run()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()