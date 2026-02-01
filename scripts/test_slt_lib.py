import sign_language_translator as slt

print("Model Codes:", [m for m in dir(slt.ModelCodes) if not m.startswith('__')])

try:
    # Attempting with a known supported language code 'pk-sl'
    # or 'hindi-text' / 'urdu-text'
    print("Initializing ConcatenativeSynthesis...")
    model = slt.models.ConcatenativeSynthesis(
        text_language="english", 
        sign_language="pk-sl", 
        sign_format="video"
    )
    
    text = "Hello"
    print(f"Translating: {text}")
    sign_video = model.translate(text)
    
    # Save the video
    output_path = "test_slt_output.mp4"
    if hasattr(sign_video, 'save'):
        sign_video.save(output_path)
    else:
        # If it returns a list of frames or similar
        print("Result type:", type(sign_video))
    
    print(f"Done.")
except Exception as e:
    print(f"Initialization or translation failed: {e}")
    import traceback
    traceback.print_exc()
