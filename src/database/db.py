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
    