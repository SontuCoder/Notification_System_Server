from time import sleep


from app.utils.logger import logger
from app.core.database import SessionLocal


while True:
    logger.info("Schedule worker run start")
    db = SessionLocal()
    try:
        print(...)
    except Exception as ex:
        logger.warning(f"Failed to send schedule notification {schedule.id} due {str(ex)}")
        schedule_service.mark_failed(db, schedule.id)
    finally:
        db.close()

    sleep(60)