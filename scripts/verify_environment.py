#!/usr/bin/env python3
"""
HandSignify — Environment verification script.
Checks Python version, required packages, and model file.
Run before starting the app: python scripts/verify_environment.py
"""
import sys
import os

REQUIRED_PYTHON = (3, 10)
REQUIRED_PACKAGES = [
    "flask",
    "flask_socketio",
    "flask_sqlalchemy",
    "flask_login",
    "flask_cors",
    "flask_wtf",
    "flask_bcrypt",
    "flask_mail",
    "cv2",
    "mediapipe",
    "numpy",
    "sklearn",
    "wtforms",
    "requests",
]
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "model.p")


def check_python():
    """Verify Python version."""
    v = sys.version_info
    ok = (v.major, v.minor) >= REQUIRED_PYTHON
    req = f"{REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}"
    cur = f"{v.major}.{v.minor}.{v.micro}"
    if ok:
        print(f"[OK] Python {cur} (>= {req})")
    else:
        print(f"[FAIL] Python {cur} (required >= {req})")
    return ok


def check_package(name):
    """Check if a package is importable."""
    if name == "cv2":
        try:
            import cv2
            return True
        except ImportError:
            return False
    if name == "sklearn":
        try:
            import sklearn
            return True
        except ImportError:
            return False
    try:
        __import__(name)
        return True
    except ImportError:
        return False


def check_packages():
    """Verify all required packages."""
    missing = []
    for pkg in REQUIRED_PACKAGES:
        if check_package(pkg):
            print(f"[OK] {pkg}")
        else:
            print(f"[FAIL] {pkg} not installed")
            missing.append(pkg)
    return len(missing) == 0, missing


def check_model():
    """Verify model file exists."""
    if os.path.isfile(MODEL_PATH):
        size = os.path.getsize(MODEL_PATH)
        print(f"[OK] Model file exists: {MODEL_PATH} ({size:,} bytes)")
        return True
    print(f"[FAIL] Model file not found: {MODEL_PATH}")
    print("       Run: python scripts/collect_imgs.py")
    print("       Then: python scripts/create_dataset.py")
    print("       Then: python scripts/train_classifier.py")
    return False


def main():
    print("HandSignify — Environment Verification")
    print("=" * 50)
    ok_py = check_python()
    ok_pkg, missing = check_packages()
    ok_model = check_model()
    print("=" * 50)

    if not ok_py:
        print("\nFix: Install Python 3.10 or 3.11")
        sys.exit(1)

    if not ok_pkg:
        print(f"\nFix: pip install -r requirements.txt")
        print(f"Missing packages: {', '.join(missing)}")
        sys.exit(1)

    if not ok_model:
        print("\nFix: Train the model (see models/README.md)")
        sys.exit(1)

    print("\nAll checks passed. You can run: python app.py")
    sys.exit(0)


if __name__ == "__main__":
    main()
