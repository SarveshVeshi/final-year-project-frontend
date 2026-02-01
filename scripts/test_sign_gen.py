from services.sign_service import sign_service
import os

def test_generation():
    print("Testing Professional Sign Language AI Generation...")
    text = "Machine learning is the future of accessibility"
    result = sign_service.generate_sign_video(text)
    
    if result['success']:
        print(f"Success! Video generated at: {result['video_url']}")
        print(f"Provider: {result['provider']}")
        # Check if file exists
        full_path = os.path.join(os.getcwd(), result['video_url'].lstrip('/'))
        if os.path.exists(full_path):
            print(f"Verified: File exists on disk ({os.path.getsize(full_path)} bytes)")
        else:
            print(f"Error: File NOT found at {full_path}")
    else:
        print(f"Generation failed: {result.get('error')}")
        print(f"Message: {result.get('message')}")

if __name__ == "__main__":
    test_generation()
