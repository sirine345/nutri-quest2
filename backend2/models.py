from sqlalchemy import Column, Integer, String, JSON
from database import Base

class GameSave(Base):
    __tablename__ = "game_saves"

    id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String)
    phase = Column(String)
    data = Column(JSON)