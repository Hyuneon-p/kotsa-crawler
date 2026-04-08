# KOTSA 알림 봇

## 프로젝트 개요
- KOTSA(한국교통안전공단) 사이트에 자동차 용역 공고 등의 비즈니스 정보가 올라오는데 이를 매일 확인하기 번거로워 자동화 해달라는 요청이 있어 제작됨.

## 프로젝트 기술 개요
### 기술 스택
![Python](https://img.shields.io/badge/python-3.14-blue?logo=python&logoColor=white)
![uv](https://img.shields.io/badge/managed%20by-uv-purple?logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232088FF.svg?logo=githubactions&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

### 로직
1. 매 시간 정각 마다 실행
2. 대상 url 접속
3. 파싱
4. 이전 최신 값과 비교(last_id_.txt) 및 저장
- 값이 유효하면(아직 최신 값이면) 흐름 종료
6. 이메일 생성 및 대상자 발송
7. git commit & push
8. 흐름 종료

### 환경 변수 관리
- 로컬 환경: .env 파일을 생성하여 관리
- 프로덕션 환경: Github Actions의 Repository Secrets로 관리
