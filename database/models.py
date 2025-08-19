from pydantic import BaseModel, PositiveInt
from datetime import date

class User(BaseModel):
    id : int
    username: str 
    email: str
    password: str 
    age: str
    weight: str 
    height: str
    goals: str

# Workouts: id, user_id, plan_name, date, exercises, duration
class Workouts(BaseModel): 
    workout_id: str
    user_id: User
    plan_name: str
    date: date
    excercises: str
    duration:  str


# Nutrition: id, user_id, date, meals, calories, macros
class Nutrition(BaseModel):
    nutrition_id: str
    user_id: User
    date: date
    meals: str

# Progress: id, user_id, workout_id, sets, reps, weights, notes
class Progress(BaseModel):
    id: str
    user_id : str   
    workout_id : Workouts
    sets: int
    reps : int
    weights: int
    notes: str
