
import sys
import os
import pickle
import cv2
import mediapipe
import numpy
from flask import Flask

print("imports_successful")

try:
    with open('./models/model.p', 'rb') as f:
        model_dict = pickle.load(f)
        model = model_dict['model']
    print("model_loaded_successfully")
except Exception as e:
    print(f"model_load_failed: {e}")

try:
    from app import app, db
    with app.app_context():
        # Check if database file exists
        if os.path.exists('instance/database.db') or os.path.exists('database.db'):
            print("database_found")
        else:
            print("database_not_found")
except Exception as e:
    print(f"app_import_failed: {e}")
