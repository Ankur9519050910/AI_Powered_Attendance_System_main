from src.database.config import supabase
import bcrypt # this is for hashing means hash our password 
def hash_pass(pwd):
    return  bcrypt.hashpw(pwd.encode(),bcrypt.gensalt()).decode();

def check_pass(pwd,hash_pass):
    return bcrypt.checkpw(pwd.encode(),hash_pass.encode());

def check_teacher_exist(username):
    responce=supabase.table("teacher").select('username').eq('username',username).execute();
    return len(responce.data)>0;

def create_teacher(username,password,name):
    data={"username":username,"password":hash_pass(password),"name":name}
    responce=supabase.table("teacher").insert(data).execute();
    return responce.data;

def teacher_login(username,password):
    responce=supabase.table("teacher").select("*").eq("username",username).execute();
    if responce.data:
        teacher=responce.data[0];
        if check_pass(password,teacher["password"]):
            return teacher
    return None;

def get_all_students():
     responce=supabase.table("student").select("*").execute()
     return responce.data;


def create_student(name,face_emb,voice_emb):
    data={"name":name,"face_embedding":face_emb,"voice_embedding":voice_emb}
    responce=supabase.table("student").insert(data).execute()
    return responce.data;

def create_subject(sub_code,sub_name,section,teacher_id):
    data={"subject_code":sub_code,"name":sub_name,"section":section,"teacher_id":teacher_id}
    responce=supabase.table("subjects").insert(data).execute()
    return responce.data;



def get_teacher_subjects(teacher_id):
    responce=supabase.table("subjects").select("*,subject_student(count),attendance_logs(timestamp)").eq("teacher_id",teacher_id).execute()
    subjects=responce.data
    
    for sub in subjects:
        sub['total_students']=sub.get("subject_student",[{}])[0].get('count',0) if sub.get("subject_student") else 0
        attendance=sub.get("attendance_logs",[])
        unique_session=len(set(log['timestamp'] for log in attendance))
        sub['total_classes']=unique_session
        
        sub.pop('subject_student',None)
        sub.pop('attendance_logs',None)
    return subjects


def enroll_student_to_subject(student_id,subject_id):
    data={'student_id':student_id,'subject_id':subject_id}
    responce=supabase.table("subject_student").insert(data).execute()
    return responce.data


def unroll_student_to_subject(student_id,subject_id):
    responce=supabase.table("subject_student").delete().eq('student_id',student_id).eq("subject_id",subject_id).execute()
    return responce.data


def get_student_subject(student_id):
    responce=supabase.table("subject_student").select("*,subjects(*)").eq("student_id",student_id).execute()
    return responce.data

def get_student_attendance(student_id):
    responce=supabase.table("attendance_logs").select("*,subjects(*)").eq("student_id",student_id).execute()
    return responce.data


def create_attendance(logs):
    response = (
        supabase
        .table('attendance_logs')
        .insert(logs)
        .execute()
    )

    return response.data