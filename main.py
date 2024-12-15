import os, base64, requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_NAME = os.getenv("REPO_NAME")
FILE_PATH = os.getenv("FILE_PATH")
REMOTE_PATH = 'test_image.png'

# API URL
BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{REMOTE_PATH}"
FOLDER_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents"

def upload_file_to_github():
    try:
        # 파일 읽기 및 base64 인코딩
        with open(FILE_PATH, "rb") as file:
            content = base64.b64encode(file.read()).decode("utf-8")
        
        # 파일 존재 여부 확인 (GET 요청)
        response = requests.get(BASE_URL, headers={"Authorization": f"Bearer {GITHUB_TOKEN}"})
        if response.status_code == 200:
            # 파일이 이미 존재 -> 업데이트 요청
            sha = response.json()["sha"]  # 기존 파일의 SHA 필요
            data = {
                "message": "Update file via API",
                "content": content,
                "sha": sha
            }
        else:
            # 파일이 존재하지 않음 -> 새 파일 생성 요청
            data = {
                "message": "Add file via API",
                "content": content
            }
 
        # 파일 업로드 (PUT 요청)
        response = requests.put(BASE_URL, json=data, headers={"Authorization": f"Bearer {GITHUB_TOKEN}"})
        if response.status_code in [200, 201]:
            print("✅ 파일 업로드 성공:", response.json()["content"]["html_url"])
        else:
            print("❌ 파일 업로드 실패:", response.json())
    except Exception as e:
        print("오류 발생:", e)

def list_files_in_folder():
    try:
        # 폴더 내용 요청
        response = requests.get(FOLDER_URL, headers={"Authorization": f"Bearer {GITHUB_TOKEN}"})
        if response.status_code == 200:
            files = response.json()
            for file in files:
                print(f"파일 이름: {file['name']} | 다운로드 URL: {file['download_url']}")
        else:
            print(f"❌ 폴더 목록 가져오기 실패: {response.status_code}, {response.json()}")
    except Exception as e:
        print("오류 발생:", e)

# 실행
list_files_in_folder()
# 실행
# upload_file_to_github()