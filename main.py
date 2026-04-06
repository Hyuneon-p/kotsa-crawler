import os
from dotenv import load_dotenv
from src.crawler.fetcher import Fetcher
from src.crawler.parser import KotsaParser
from src.crawler.storage import FileStorage
from src.crawler.sender import MailSender

def main():
    load_dotenv()
    
    fetcher = Fetcher()
    parser = KotsaParser()
    sender = MailSender()

    targets = [
        {
            "name": "자동차 기준 제작/개정",
            "url": os.environ.get("TARGET_URL_prestrd_list"),
            "type": "prestrd_list",
            "storage_file": "last_id_prestrd_list.txt"
        },
        {
            "name": "일반 공지",
            "url": os.environ.get("TARGET_URL_katri_list"),
            "type": "katri_list",
            "storage_file": "last_id_katri_list.txt"
        }
    ]

    all_new_items = {}

    for target in targets:
        print(f"\n[{target['name']}] 확인 중...")
        storage = FileStorage(target['storage_file'])
        
        try:
            response = fetcher.fetch(target['url'])
            items = parser.parse_list(response.text, target['type'])
            
            # 파일에서 마지막 id 읽어와서 비교한 후에 제일 최신 글 id 값만 업데이트함.
            last_id = int(storage.get_last_id())
            new_items = [item for item in items if item['id'] > last_id]
            
            if new_items:
                all_new_items[target['name']] = new_items
                latest_id = max(item['id'] for item in new_items)
                storage.update_last_id(latest_id)
                print(f"-> {len(new_items)}건의 새 글 발견")
            else:
                print("-> 새로운 글 없음")
        except Exception as e:
            print(f"-> 오류 발생: {e}")

    if all_new_items:
        sender.send(all_new_items)

if __name__ == "__main__":
    main()