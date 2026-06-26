# SnapClass — AI-Powered Attendance System

SnapClass automates classroom attendance using face recognition and voice recognition, so teachers don't have to call out names or pass around a sign-in sheet. Teachers create subjects, students enroll using a class code or QR code, and attendance is taken by snapping a classroom photo or recording a short audio clip.

Built with **Streamlit**, **Supabase (PostgreSQL)**, **dlib** face recognition, and **Resemblyzer** voice embeddings.

---

## Features

### For Teachers
- **Create & manage subjects** — subject name, code, and section
- **Share subjects** via a unique join code or a scannable QR code (generated with `segno`)
- **Take attendance two ways:**
  - 📸 **Face recognition** — upload or capture classroom photos; an SVM classifier trained on enrolled students' face embeddings identifies who's present
  - 🎙️ **Voice recognition** — record classroom audio; the app splits it into speech segments and matches each voice against enrolled students' voice embeddings
- **Review before saving** — every attendance run shows a results table (Present/Absent per student) before it's written to the database
- **Attendance records** — a searchable history of every session taken, grouped by time, subject, and code
- **Subject stats** — live count of enrolled students and number of classes held per subject

### For Students
- **Face-ID login** — no password; log in by showing your face to the camera
- **Self-registration** — first-time users are auto-detected as "new" (based on face-match confidence) and prompted to register with name, face, and optional voice sample
- **Enroll in subjects** — manually via a subject code, or automatically via a shared join link/QR code (`?join-code=...` query param)
- **Track your attendance** — see total classes vs. classes attended, per subject
- **Unenroll** from a subject at any time

---

## Tech Stack

| Layer | Technology |
|---|---|
| App framework | [Streamlit](https://streamlit.io) |
| Database | [Supabase](https://supabase.com) (PostgreSQL) |
| Face detection & embeddings | `dlib-bin`, `face_recognition_models` |
| Face classification | `scikit-learn` (linear SVM) |
| Voice embeddings | `resemblyzer`, `librosa` |
| QR code generation | `segno` |
| Password hashing | `bcrypt` |
| Image handling | `Pillow` |
| Data handling | `pandas`, `numpy` |

---

## Project Structure

```
.
├── app.py                          # Entry point — routes between Home / Student / Teacher screens
├── requirements.txt
└── src/
    ├── screen/
    │   ├── home_screen.py          # Landing page ("I'm Student" / "I'm Teacher")
    │   ├── student_screen.py       # Face-ID login, registration, student dashboard
    │   └── teacher_screen.py       # Teacher login/register, attendance + subject management
    │
    ├── components/
    │   ├── add_photo_dialog.py            # Camera/upload modal for classroom photos
    │   ├── voice_dialog.py                # Voice attendance recording + analysis modal
    │   ├── attendance_result_dialog.py    # Review & confirm attendance before saving
    │   ├── create_subject_dialog.py       # Teacher: create a new subject
    │   ├── share_subject_dialog.py        # Teacher: share subject via link + QR code
    │   ├── enroll_dialog.py               # Student: enroll using a manual subject code
    │   ├── enroll_auto_dialog.py          # Student: auto-enroll via shared join link
    │   ├── subjects_cards.py              # Reusable subject card UI
    │   ├── header.py / footer.py          # Shared layout pieces
    │
    ├── pipeline/
    │   ├── face_pipeline.py        # Face embedding extraction, SVM training, attendance prediction
    │   └── voice_pipeline.py       # Voice embedding extraction, speaker identification, bulk audio processing
    │
    ├── database/
    │   ├── config.py               # Supabase client initialization
    │   └── db.py                   # All database queries (teacher, student, subjects, enrollment, attendance)
    │
    └── ui/
        └── base_layout.py          # Global CSS theming (gradients, buttons, cards, inputs)
```

---

## How It Works

### Face Attendance
1. Teacher captures or uploads one or more classroom photos.
2. Each photo is scanned for faces using `dlib`'s frontal face detector.
3. Each detected face is converted into a 128-dimension embedding.
4. A linear SVM (trained on all enrolled students' stored embeddings) predicts the most likely student for each face.
5. The prediction is **double-checked** against the raw L2 distance to that student's stored embedding — only matches under `RESEMBLANCE_THRESHOLD` are accepted, to avoid false positives from the classifier alone.
6. Results are shown in a review table before being saved to `attendance_logs`.

### Voice Attendance
1. Teacher records classroom audio (e.g. students saying "I am present").
2. The audio is split into individual speech segments (silence-based splitting via `librosa.effects.split`).
3. Each segment is converted into a voice embedding via `resemblyzer`.
4. Each embedding is compared (cosine similarity) against enrolled students' stored voice embeddings; matches above the similarity threshold are marked present.
5. Same review-and-confirm flow as face attendance before saving.

### Student Registration
- On first face scan, if the face doesn't confidently match any existing student, the student is prompted to register.
- A **dual-threshold check** prevents duplicate accounts: a "familiar but unconfirmed" face is asked to retry rather than allowed to register fresh.
- Voice enrollment during registration is optional.

### Subject Enrollment
- **Manual:** student enters a subject code shared by the teacher.
- **QR / link:** teacher shares a QR code or link like `https://yourapp.streamlit.app/?join-code=CS101`; opening it on a logged-in student account triggers an auto-enroll confirmation dialog.

---

## Credits

Created by Ankur 💗
