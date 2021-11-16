from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:perfume90210@127.0.0.1/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    print("Using database")
    try:
        yield db
    finally:
        db.close()


# run db query directly
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
#
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', user="postgres", password="perfume90210", database="fastapi",
#                                 cursor_factory=RealDictCursor)
#         curser = conn.cursor()
#         print("Connected to database")
#         break
#     except Exception as error:
#         print("Unable to connect to database")
#         print("Error: %s" % error)
#         time.sleep(5)
