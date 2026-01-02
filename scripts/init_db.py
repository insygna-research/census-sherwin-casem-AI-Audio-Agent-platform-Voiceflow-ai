#!/usr/bin/env python3
from sqlalchemy import create_engine
from voiceflow.models.call import Base as CallBase
from voiceflow.models.customer import Base as CustomerBase
from voiceflow.config import get_settings

settings = get_settings()


def init_database():
    engine = create_engine(settings.database_url)
    
    CallBase.metadata.create_all(engine)
    CustomerBase.metadata.create_all(engine)
    
    print("Database initialized successfully!")


if __name__ == "__main__":
    init_database()
