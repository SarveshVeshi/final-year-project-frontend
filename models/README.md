# Models Directory

This folder stores the ML model and dataset used for sign language recognition.

---

## Required Model File

| Property | Value |
|----------|-------|
| **Filename** | `model.p` |
| **Extension** | `.p` (Python pickle) |
| **Location** | `models/model.p` (project root relative) |
| **Format** | Pickle dict: `{'model': RandomForestClassifier}` |

The app loads it at startup via:
```python
model_dict = pickle.load(open('./models/model.p', 'rb'))
model = model_dict['model']
```

---

## How the Model Was Trained

1. **Data collection** — `scripts/collect_imgs.py` captures webcam frames for each gesture class
2. **Dataset creation** — `scripts/create_dataset.py` extracts MediaPipe landmarks from images → `models/data.pickle`
3. **Training** — `scripts/train_classifier.py` trains a scikit-learn Random Forest and saves to `models/model.p`

**Algorithm:** RandomForestClassifier (scikit-learn)  
**Input:** 42-dimensional normalized hand landmarks from MediaPipe  
**Output:** Class labels (e.g. A–Z, Hello, Thank You)

---

## Regenerating the Model

If `model.p` is not present, regenerate it with:

```bash
# Step 1: Collect images (33 classes × 100 images per class; requires webcam)
python scripts/collect_imgs.py

# Step 2: Build dataset from data/ folder
python scripts/create_dataset.py

# Step 3: Train and save model
python scripts/train_classifier.py
```

**Prerequisites:**
- `data/` directory with subfolders `0`, `1`, …, `32` (one per class)
- Each subfolder contains `.jpg` images with hand gestures
- `models/` directory must exist

---

## Download Placeholder

The model is **not** included in the repository (large binary, gitignored).

**Options:**
1. **Train locally** — Use the scripts above (recommended)
2. **Release assets** — If the maintainer publishes a release, check:
   - https://github.com/SarveshVeshi/final-year-project-version-2/releases
   - Download `model.p` and place it in `models/`

---

## Python & Library Compatibility

| Requirement | Version |
|-------------|---------|
| **Python** | 3.10 or 3.11 recommended |
| **scikit-learn** | 1.3.0–1.6.x (model trained with 1.3.0; 1.5+ may show InconsistentVersionWarning but works) |
| **pickle** | Standard library; no extra install |
| **numpy** | Compatible with scikit-learn version |

**Note:** Models trained with scikit-learn 1.3.0 can be loaded with newer scikit-learn; a version warning may appear but inference is supported.
