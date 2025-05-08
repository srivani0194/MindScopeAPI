from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import date

Base = declarative_base()  # this sets up the base class for tables

#This table stores user info
class User(Base):
   __tablename__ = "users"
   id = Column(Integer, primary_key=True, index=True)        # unique numbee for each user
   username = Column(String, unique=True, index=True)
   hashed_password = Column(String)

   mood_entries = relationship("MoodEntry", back_populates="user")    #links to mood


   # This table is for mood log
class MoodEntry(Base):
    __tablename__ = "mood_entries"
    id = Column(Integer, primary_key=True, index=True)
    mood = Column(String)       #like happy, sad, angry
    activity = Column(String)   # eg., work, running
    energy = Column(String)     # eg., high, low, okay
    date = Column(Date, default=date.today)    # date of the entry
    user_id = Column(Integer, ForeignKey("users.id"))     # Link to the user

    user = relationship("User", back_populates="mood_entries")
