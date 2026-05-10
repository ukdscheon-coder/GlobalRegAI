@echo off
title GlobalRegAI — Auto Scheduler (24/7)

echo.
echo  GlobalRegAI 자동 업데이트 스케줄러 실행 중...
echo  - 매시간: FDA 리콜/RSS 업데이트
echo  - 매일 02:00: 전체 크롤링
echo  - 매주 일요일: PDF 재다운로드
echo.
echo  창을 닫지 마세요. (최소화는 가능)
echo  종료하려면 Ctrl+C 누르세요.
echo.

cd /d C:\Users\laser\GlobalRegAI
set OLLAMA_URL=http://localhost:11434
set QDRANT_URL=http://localhost:6333
python scripts\auto_scheduler.py
pause
