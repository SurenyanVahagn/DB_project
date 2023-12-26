
from fastapi import FastAPI, HTTPException, Depends, Body
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session

# FastAPI app initialization
app = FastAPI()

# Database configuration (replace with your actual database URL)
DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy base declarative class
Base = declarative_base()

# Example of Todo model
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations for Todo model
@app.post("/todos/", response_model=Todo)
def create_todo(todo: Todo, db: Session = Depends(get_db)):
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@app.get("/todos/", response_model=list[Todo])
def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    todos = db.query(Todo).offset(skip).limit(limit).all()
    return todos

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_data: dict = Body(...), db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in todo_data.items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"ok": True}
