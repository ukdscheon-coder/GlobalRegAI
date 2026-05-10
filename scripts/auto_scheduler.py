#!/usr/bin/env python3
"""
GlobalRegAI — 자동 데이터 업데이트 스케줄러
매일 새벽 2시: 전체 크롤링
매시간: FDA RSS + 리콜 업데이트
"""

import schedule
import time
import logging
from datetime import datetime
from pathlib import Path

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/scheduler.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger("GlobalRegAI-Scheduler")


def job_hourly_fda():
    """매시간: FDA 리콜/RSS 업데이트"""
    log.info("=== Hourly FDA Update ===")
    try:
        from data_crawler import FDACrawler, RSSCrawler
        fda = FDACrawler()
        n1 = fda.crawl_device_recalls()
        n2 = fda.crawl_drug_enforcement()
        n3 = fda.crawl_food_enforcement()
        rss = RSSCrawler()
        n4 = rss.crawl_all()
        log.info(f"Hourly update: recalls={n1+n2+n3}, rss={n4} chunks")
    except Exception as e:
        log.error(f"Hourly update failed: {e}")


def job_daily_full():
    """매일 새벽 2시: 전체 크롤링"""
    log.info("=== Daily Full Crawl ===")
    try:
        from data_crawler import run_full_pipeline
        run_full_pipeline()
        log.info("Daily full crawl completed")
    except Exception as e:
        log.error(f"Daily crawl failed: {e}")


def job_weekly_pdf():
    """매주 일요일: PDF 재다운로드 & 수집"""
    log.info("=== Weekly PDF Update ===")
    try:
        from pdf_bulk_downloader import download_all_pdfs, ingest_pdfs_to_qdrant
        download_all_pdfs()
        ingest_pdfs_to_qdrant()
        log.info("Weekly PDF update completed")
    except Exception as e:
        log.error(f"Weekly PDF update failed: {e}")


if __name__ == "__main__":
    print("\n GlobalRegAI Auto-Scheduler Started")
    print(" Schedule:")
    print("   Every hour     → FDA recalls + RSS feeds")
    print("   Daily 02:00    → Full regulatory crawl (all sources)")
    print("   Sunday 03:00   → PDF bulk download & ingest")
    print(" Press Ctrl+C to stop\n")

    schedule.every(1).hours.do(job_hourly_fda)
    schedule.every().day.at("02:00").do(job_daily_full)
    schedule.every().sunday.at("03:00").do(job_weekly_pdf)

    # 시작 시 즉시 한 번 실행
    log.info("Scheduler started — running initial update")
    job_hourly_fda()

    while True:
        schedule.run_pending()
        time.sleep(60)
