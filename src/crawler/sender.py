import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class MailSender:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.receiver_email = os.getenv("RECEIVER_EMAIL")

    def send(self, section_results: dict[str, list[dict]]):
        total_count = sum(len(items) for items in section_results.values())
        if total_count == 0:
            return

        subject = f"[알림] KOTSA 신규 소식이 {total_count}건 도착했습니다."
        text_body = "새로운 글 목록:\n\n"
        html_sections = ""

        for section_name, items in section_results.items():
            if not items: continue
            
            text_body += f"--- {section_name} ---\n"
            html_sections += f"""
            <div style="margin: 30px 0 10px 0; border-bottom: 2px solid #007bff; padding-bottom: 5px;">
                <span style="background-color: #007bff; color: white; padding: 4px 12px; border-radius: 20px; font-size: 14px; font-weight: bold;">{section_name}</span>
            </div>
            """
            
            for item in items:
                text_body += f"- {item['title']}\n  링크: {item['url']}\n\n"
                html_sections += f"""
                <div style="padding: 15px; border: 1px solid #eee; border-radius: 8px; margin-bottom: 10px; background-color: #fafafa;">
                    <h4 style="margin: 0 0 10px 0; color: #333; font-size: 16px;">{item['title']}</h4>
                    <a href="{item['url']}" style="color: #007bff; font-size: 13px; text-decoration: none; font-weight: bold;">[게시글 바로가기]</a>
                </div>
                """

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
        </head>
        <body style="font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.08);">
                <div style="background-color: #007bff; color: #ffffff; padding: 40px 20px; text-align: center;">
                    <h1 style="margin: 0; font-size: 26px; font-weight: 800; letter-spacing: -0.5px;">KOTSA 신규 게시글 알림</h1>
                    <p style="margin: 10px 0 0; opacity: 0.9; font-size: 16px;">오늘 총 <strong>{total_count}건</strong>의 새로운 소식이 도착했습니다.</p>
                </div>
                <div style="padding: 30px 20px;">
                    {html_sections}
                </div>
                <div style="background-color: #f8f9fa; color: #adb5bd; padding: 30px 20px; text-align: center; font-size: 12px; border-top: 1px solid #eee;">
                    <p style="margin: 0;">본 메일은 크롤러 봇에 의해 자동으로 발송되었습니다.</p>
                    <p style="margin: 5px 0 0;">© 2026 germankorea IT manager. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        msg = MIMEMultipart("alternative")
        msg['From'] = self.smtp_user
        msg['To'] = self.receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            print(f"메일 발송 성공: {self.receiver_email}")