import os
import shutil

# 상위 폴더 경로
parent_folder = 'C:\\Users\\KOLO\\Desktop\\thresh\\train\\0'

# 모든 하위 폴더에서 파일을 상위 폴더로 이동
for subdir, dirs, files in os.walk(parent_folder):
    for file in files:
        # 파일의 현재 경로
        cur_path = os.path.join(subdir, file)
        # 파일을 이동할 경로
        new_path = os.path.join(parent_folder, file)

        # 파일을 상위 폴더로 이동, 같은 이름의 파일이 존재하면 덮어쓰지 않고 넘어감
        if cur_path != new_path:  # 현재 파일이 상위 폴더에 이미 있는지 확인
            if not os.path.exists(new_path):  # 동일한 파일이 이미 있는지 확인
                shutil.move(cur_path, new_path)
                print(f"File {file} moved to {parent_folder}")
            else:
                print(f"File {file} already exists in {parent_folder}")

# 이제 모든 파일이 이동되었으므로 빈 폴더를 삭제합니다.
for subdir, dirs, files in os.walk(parent_folder, topdown=False):
    # os.rmdir을 사용하여 비어 있는 폴더만 삭제합니다.
    if not os.listdir(subdir):
        os.rmdir(subdir)
        print(f"Empty folder {subdir} deleted")
