import bcrypt
from src.database.config import supabase


# Password utilities


def hash_password(pwd: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()


def verify_password(pwd: str, hashed: str) -> bool:
    """Check a plaintext password against a bcrypt hash."""
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


# Teacher


def check_teacher_exist(username: str) -> bool:
    try:
        response = (
            supabase.table("teacher")
            .select("username")
            .eq("username", username)
            .execute()
        )
        return len(response.data) > 0
    except Exception as e:
        print(f"[db] check_teacher_exist error: {e}")
        return False


def create_teacher(username: str, password: str, name: str):
    try:
        data = {
            "username": username,
            "password": hash_password(password),
            "name": name,
        }
        response = supabase.table("teacher").insert(data).execute()
        return response.data
    except Exception as e:
        print(f"[db] create_teacher error: {e}")
        return None


def teacher_login(username: str, password: str):
    try:
        response = (
            supabase.table("teacher")
            .select("*")
            .eq("username", username)
            .execute()
        )
        if response.data:
            teacher = response.data[0]
            if verify_password(password, teacher["password"]):
                return teacher
    except Exception as e:
        print(f"[db] teacher_login error: {e}")
    return None


# Student


def get_all_students():
    try:
        response = supabase.table("student").select("*").execute()
        return response.data
    except Exception as e:
        print(f"[db] get_all_students error: {e}")
        return []


def create_student(name: str, face_emb, voice_emb):
    try:
        data = {
            "name": name,
            "face_embedding": face_emb,
            "voice_embedding": voice_emb,
        }
        response = supabase.table("student").insert(data).execute()
        return response.data
    except Exception as e:
        print(f"[db] create_student error: {e}")
        return None


# Subjects


def delete_subject(subject_id: int):
    
    # we are going to delete the subject when not student is enrolled in tht subject 
    
    """
    Safe-mode delete: only removes the subject if NO students are enrolled.
    Returns (True, None) on success, (False, reason_string) on failure.
    """
    
    try:
        enrolled = (
            supabase.table("subject_student")
            .select("student_id", count="exact")
            .eq("subject_id", subject_id)
            .execute()
        )
        count = enrolled.count if enrolled.count is not None else len(enrolled.data)

        if count > 0:
            return False, f"Cannot delete — {count} student(s) are still enrolled. Ask them to unenroll first."

        # Clean up any orphaned attendance logs before removing subject
        supabase.table("attendance_logs").delete().eq("subject_id", subject_id).execute()
        supabase.table("subjects").delete().eq("subject_id", subject_id).execute()
        return True, None

    except Exception as e:
        print(f"[db] delete_subject error: {e}")
        return False, str(e)


def update_subject(subject_id: int, name: str, subject_code: str, section: str):
    """Update subject name, code, and section."""
    try:
        supabase.table("subjects").update({
            "name": name,
            "subject_code": subject_code,
            "section": section,
        }).eq("subject_id", subject_id).execute()
        return True
    except Exception as e:
        print(f"[db] update_subject error: {e}")
        return False


def create_subject(sub_code: str, sub_name: str, section: str, teacher_id: int):
    try:
        data = {
            "subject_code": sub_code,
            "name": sub_name,
            "section": section,
            "teacher_id": teacher_id,
        }
        response = supabase.table("subjects").insert(data).execute()
        return response.data
    except Exception as e:
        print(f"[db] create_subject error: {e}")
        return None


def get_teacher_subjects(teacher_id: int):
    try:
        response = (
            supabase.table("subjects")
            .select("*, subject_student(count), attendance_logs(timestamp)")
            .eq("teacher_id", teacher_id)
            .execute()
        )
        subjects = response.data

        for sub in subjects:
            # Total enrolled students
            sub["total_students"] = (
                sub.get("subject_student", [{}])[0].get("count", 0)
                if sub.get("subject_student")
                else 0
            )

            # Count unique attendance *runs* (one run = one Run Face Analysis /
            # Use Voice Attendance click). Each run writes all its logs with the
            # SAME full timestamp (see current_timestamp in
            # teacher_tab_take_attendance), so counting distinct full
            # timestamps == counting distinct attendance-taking events.
            # (Previously this sliced to [:10], which collapsed everything
            # down to distinct calendar DATES instead of distinct runs.)

            attendance = sub.get("attendance_logs", [])
            unique_sessions = len(
                set(log["timestamp"] for log in attendance if log.get("timestamp"))
            )
            sub["total_classes"] = unique_sessions

            sub.pop("subject_student", None)
            sub.pop("attendance_logs", None)

        return subjects
    except Exception as e:
        print(f"[db] get_teacher_subjects error: {e}")
        return []


# Enrollment


def enroll_student_to_subject(student_id: int, subject_id: int):
    try:
        # Check for existing enrollment to avoid duplicate constraint errors
        existing = (
            supabase.table("subject_student")
            .select("student_id")
            .eq("student_id", student_id)
            .eq("subject_id", subject_id)
            .execute()
        )
        if existing.data:
            print(f"[db] Student {student_id} already enrolled in subject {subject_id}")
            return existing.data

        data = {"student_id": student_id, "subject_id": subject_id}
        response = supabase.table("subject_student").insert(data).execute()
        return response.data
    except Exception as e:
        print(f"[db] enroll_student_to_subject error: {e}")
        return None


def unroll_student_to_subject(student_id: int, subject_id: int):
    try:
        response = (
            supabase.table("subject_student")
            .delete()
            .eq("student_id", student_id)
            .eq("subject_id", subject_id)
            .execute()
        )
        return response.data
    except Exception as e:
        print(f"[db] unroll_student_to_subject error: {e}")
        return None


def get_student_subject(student_id: int):
    try:
        response = (
            supabase.table("subject_student")
            .select("*, subjects(*)")
            .eq("student_id", student_id)
            .execute()
        )
        return response.data
    except Exception as e:
        print(f"[db] get_student_subject error: {e}")
        return []


# Attendance


def get_student_attendance(student_id: int):
    try:
        response = (
            supabase.table("attendance_logs")
            .select("*, subjects(*)")
            .eq("student_id", student_id)
            .execute()
        )
        return response.data
    except Exception as e:
        print(f"[db] get_student_attendance error: {e}")
        return []


def create_attendance(logs: list):
    try:
        response = supabase.table("attendance_logs").insert(logs).execute()
        return response.data
    except Exception as e:
        print(f"[db] create_attendance error: {e}")
        return None


def get_attendance_for_teacher(teacher_id):
    responce = supabase.table("attendance_logs").select("*,subjects!inner(*)").eq("subjects.teacher_id", teacher_id).execute()
    return responce.data