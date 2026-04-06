import os

class FileStorage:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_last_id(self) -> str:
        """파일에서 마지막으로 저장된 ID를 읽어옵니다."""
        if not os.path.exists(self.file_path):
            return "0"
        with open(self.file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return content if content else "0"

    def update_last_id(self, new_id: str):
        """새로운 ID를 파일에 기록합니다."""
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(str(new_id))