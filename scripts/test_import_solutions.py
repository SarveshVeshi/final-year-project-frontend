
try:
    import mediapipe.solutions
    print("Success import mediapipe.solutions")
except Exception as e:
    print(f"Failed import mediapipe.solutions: {e}")

try:
    from mediapipe import solutions
    print("Success from mediapipe import solutions")
except Exception as e:
    print(f"Failed from mediapipe import solutions: {e}")
