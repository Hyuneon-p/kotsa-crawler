import time
import requests

class Fetcher:
    def __init__(self, timeout=10):
        # 브라우저 설정을 추가해줘야 차단될 확률이 줄어듬. 근데 여전히 차단되긴 함 ㅋㅋㅋ
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.timeout = timeout

    def fetch(self, url: str, retries: int = 10) -> requests.Response:
        attempt = 0
        
        while attempt < retries:
            try:
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
                response.raise_for_status() 
                
                print(f"접속 성공: {url} ({response.status_code})")
                return response
            except (requests.exceptions.RequestException, Exception) as e:
                attempt += 1
                print(f"접속 실패 ({attempt}/{retries}): {url} | 사유: {e}")
                
                if attempt >= retries:
                    print(f"최대 재시도 초과, 사이트가 유효한지 확인해주세요. URL: {url}")
                    raise 
                
                wait_time = attempt * 2 
                time.sleep(wait_time)