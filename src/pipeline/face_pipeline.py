import numpy as np
import dlib
import face_recognition_models
import streamlit as st
from sklearn.svm import SVC

from src.database.db import get_all_students

RESEMBLANCE_THRESHOLD = 0.6


  
# Model loading
@st.cache_resource  # Runs only once — loading dlib models is expensive
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec


  
# Face embedding
  

def get_face_embedding(image_np):
    detector, sp, facerec = load_dlib_models()

    faces = detector(image_np, 1)
    embeddings = []

    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
        # Explicitly cast dlib.vector → numpy array for safe arithmetic
        embeddings.append(np.array(face_descriptor))

    return embeddings


  
# Classifier training
@st.cache_resource
def get_train_model():
    X, y = [], []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:
        embedding = student.get("face_embedding")
        if embedding:
            X.append(np.array(embedding))
            # Force int to avoid string/int mismatch from Supabase
            y.append(int(student.get("student_id")))

    if len(X) == 0:
        return None

    clf = None  # stays None when only 1 student exists

    if len(set(y)) >= 2:
        # SVM needs at least 2 different students to train
        clf = SVC(kernel="linear", class_weight="balanced")
        try:
            clf.fit(X, y)
        except ValueError as e:
            print(f"[face_pipeline] Classifier training failed: {e}")
            return None
    else:
        # Only 1 student — skip SVM, distance check handles recognition
        print("[face_pipeline] Only 1 student in DB — skipping SVM, using distance matching only.")

    return {"clf": clf, "X": X, "y": y}


def train_classifier():
    # Only clear the classifier cache, NOT the dlib models cache
    get_train_model.clear()
    model_data = get_train_model()
    return bool(model_data)


  
# Helpers
  

def _best_match_distance(
    X_train: list,
    y_train: list,
    predicted_id: int,
    encoding: np.ndarray
) -> float:
    """
    Return the smallest L2 distance between `encoding` and any stored
    embedding that belongs to `predicted_id`.

    Checks ALL embeddings for that student, not just the first one,
    so students with multiple stored embeddings are handled correctly.
    """
    candidate_embeddings = [
        np.array(X_train[i])
        for i, label in enumerate(y_train)
        if label == predicted_id
    ]

    if not candidate_embeddings:
        return float("inf")

    distances = [np.linalg.norm(emb - encoding) for emb in candidate_embeddings]
    return min(distances)


  
# Attendance prediction
  

def predict_attendance(class_image_np):
    """
    Returns:
        detected_student  dict   {student_id: True} for confirmed matches
        all_students      list   all student IDs known to the model
        num_faces         int    number of faces found in the image
        best_match_score  float  lowest distance score seen — use this in
                                 the login screen to decide if an unrecognized
                                 face is truly new or just a poor lighting match
    """
    detected_student = {}
    best_match_score = float("inf")

    encodings = get_face_embedding(class_image_np)
    num_faces = len(encodings)

    model_data = get_train_model()

    if not model_data:
        return detected_student, [], num_faces, best_match_score

    clf = model_data["clf"]       # None when only 1 student in DB
    X_train = model_data["X"]
    y_train = model_data["y"]

    all_students = sorted(set(y_train))

    for encoding in encodings:
        encoding_np = np.array(encoding)

        if clf is not None and len(all_students) >= 2:
            # Normal path — SVM picks the most likely student
            predicted_id = int(clf.predict([encoding_np])[0])
        else:
            # Only 1 student in DB — assign directly, distance
            # check below still verifies it's actually them
            predicted_id = int(all_students[0])

        score = _best_match_distance(X_train, y_train, predicted_id, encoding_np)

        # Track the best (lowest) score across all faces in the image
        if score < best_match_score:
            best_match_score = score

        if score <= RESEMBLANCE_THRESHOLD:
            detected_student[predicted_id] = True

    return detected_student, all_students, num_faces, best_match_score
