from bs4 import BeautifulSoup as bs
import re

class KotsaParser:
    def __init__(self):
        self.base_url_prestrd_list = "https://main.kotsa.or.kr/portal/bbs/prestrd_view.do"   
        self.base_url_katri_list = "https://katri.kotsa.or.kr/web/contents/katri301.do"

    def parse_list(self, html: str, site_type: str) -> list[dict]:
        soup = bs(html, 'html.parser')
        # 사이트 마다 DOM 구조가 달라서 분기 처리해야 됨.. 오래된 공기업 사이트 특징이 이렇다..
        if site_type == "prestrd_list":
            # 입찰 소식 > 사전규격공개
            rows = soup.select('#content > table > tbody > tr')
        elif site_type == "katri_list": 
            # 카트리 > 알림 마당 > 일반 공지
            rows = soup.select('#container > section > section.content > div.board-wrap > div.board-common > ul.board-list > li')
        parsed_data = []

        for row in rows:
            # 사이트에 따라서 파싱할 값 지정함. (아오.. 지 혼자 span.num이네..)
            if site_type == "prestrd_list":
                num_td = row.select_one('td:nth-child(1)')
                link_tag = row.select_one('td a')
            elif site_type == "katri_list":
                num_td = row.select_one('span.num')
                link_tag = row.select_one('li a')

            # num_td가 존재하지 않거나 숫자가 아닌 경우 해당 행은 append 하지 않고 무시함.
            if not num_td or not num_td.text.strip().isdigit():
                continue

            num = int(num_td.text.strip())

            # 예외 처리 안 하면 link_tag 건들일 때 큰일남.
            if not link_tag:
                continue
                
            # a 태그 내부 아이콘 텍스트 제외하고 실제 텍스트만 추출함, 
            # recursive=False를 주면 자신의 직계 자손 노드의 텍스트만 검색해서 매우 편하다.
            text_elements = link_tag.find_all(text=True, recursive=False)
            # 구분해서 자르고 다시 보정한 후 합치기
            title = ' '.join(text_elements).strip()
            
            # a 태그 onclick 속성에 담긴 값을 추출함. 이거 골 때리는게 사이트마다 파라미터 개수도 다르고 순서도 다름. 
            # 걍 무식하게 부호로 감싸진 애들만 다 추출해서 url 조립할 때 다 때려박음 ㅋㅋㅋㅋ
            onclick_val = link_tag.get('onclick', '')
            params = re.findall(r"'([^']*)'", onclick_val)
            
            if site_type == "prestrd_list" and len(params) >= 7:
                # url 골 때리네
                post_url = (
                    f"{self.base_url_prestrd_list}?bbscCode={params[0]}&cateCode={params[1]}&"
                    f"bbscSeqn={params[2]}&pageNumb={params[3]}&sechCdtn={params[4]}&"
                    f"sechKywd={params[5]}&menuCode={params[6]}"
                )
            elif site_type == "katri_list" and len(params) >= 1:
                post_url = (
                    # 실험해보니 필수 파라미터만 넣어도 되더라 뭐임 이거
                    f"{self.base_url_katri_list}?schM=view&id={params[0]}"
                    # 아 url 혐오스럽네 증말 ㅋㅋㅋㅋ
                    # f"{self.base_url_katri_list}?schM={params[0]}&page={params[1]}&"
                    # f"viewCount={params[2]}&id={params[3]}&schBdcode={params[4]}&"
                    # f"schGroupCode={params[5]}"
                )
            else:
                post_url = "#"
            
            # 전부 조립해서 딕셔너리로 return
            parsed_data.append({
                'id': num,
                'title': title,
                'url': post_url
            })

        return parsed_data