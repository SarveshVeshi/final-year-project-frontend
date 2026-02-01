import mediapipe as mp
try:
    print("Mediapipe file:", mp.__file__)
    print("Solutions available:", dir(mp.solutions))
    mp_hands = mp.solutions.hands
    print("mp_hands accessed successfully")
except Exception as e:
    print("Error accessing mediapipe solutions:", e)
