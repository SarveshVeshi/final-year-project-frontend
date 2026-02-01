import mediapipe
print("Mediapipe imported")
try:
    print("Direct solutions import...")
    import mediapipe.solutions
    print("Success: import mediapipe.solutions")
except ImportError as e:
    print("Fail: import mediapipe.solutions", e)

import mediapipe as mp
print("mp dir:", dir(mp))
try:
    print("mp.solutions:", mp.solutions)
except AttributeError:
    print("mp has no attribute solutions")
