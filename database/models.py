from pydantic import BaseModel, PositiveInt
from datetime import date
from typing import Optional
from dataclasses import Field

class User(BaseModel):
    username: str 
    email: str
    password: str 
    age: str
    weight: str 
    height: str
    goals: str

# Workouts: , plan_name, date, exercises, duration
class Workouts(BaseModel): 
    user_id: User
    plan_name: str
    date: date
    excercises: str
    duration:  str

# Nutrition: , date, meals, calories, macros
class Nutrition(BaseModel):
    user_id: User
    date: date
    meals: str

# Progress: , workout_id, sets, reps, weights, notes
class Progress(BaseModel):
    user_id : str   
    workout_id : Workouts
    sets: int
    reps : int
    weights: int
    notes: str
