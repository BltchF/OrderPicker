from test_db import get_database_engine
from app.models import Store, Menu, Order, OrderItem, User, Role, UserRole




def create_tables():
    engine = get_database_engine()
    if engine:
        with engine.connect():
            engine.execute("CREATE EXTENSION IF NOT EXISTS citext")
            db.create_all(engine)
        print("Tables created successfully!")
    else:
        print("Error: Could not create tables") 


