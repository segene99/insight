
import datetime
from database import SessionLocal
from models import ImageList, Question
from sqlalchemy.orm import Session

def fetch_content_from_db(siteurl: str) -> str:
    # Create a new session
    session = SessionLocal()
    try:
        # Get the content where the subject matches the given siteurl
        content = session.query(Question.content).filter(Question.subject == siteurl).first()
        return content[0] if content else None
    finally:
        session.close()


def check_ocr(siteURL: str) -> bool:    
    # Start a new session for the database operation
    session = SessionLocal()
    try:
        # Query the database to check if siteURL exists in the 'subject' column
        exists = session.query(Question).filter(Question.subject == siteURL).first() is not None
        print("=====check db=====")
    except:
        session.rollback()
        raise
    finally:
        session.close()

    return exists

def insert_ocr(texts: list, image_list: ImageList):
    # Insert detected text into the database
    # Start a new session for the database operation
    session = SessionLocal()
    detected_texts_str = " ".join(texts)

    try:
        insert_text_to_db(session, url=image_list.siteUrls, detected_text=detected_texts_str)
        session.commit()
    except:
        print("<<<<<<<rollback>>>>>>>>>")
        session.rollback()
        raise
    finally:
        session.close()

def insert_text_to_db(session: Session, url: str, detected_text: str):
    """Inserts detected text from an image URL into the database."""
    question = Question(subject=url, content=detected_text, create_date=datetime.datetime.now())
    session.add(question)
    session.commit()