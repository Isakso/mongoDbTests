from fastapi import APIRouter, HTTPException
from typing import List
from models.DaySchedule import DaySchedule
from config.database import collection_name


router = APIRouter()

# Retrieve all day schedules
@router.get("/", response_model=List[DaySchedule])
async def get_day_schedules():
    try:
        schedules_cursor = collection_name.find()  # Fetch all schedules from MongoDB
        schedules = await schedules_cursor.to_list(length=None)  # Await async cursor
        print(f"Fetched schedules: {schedules}")  
        return [DaySchedule(**schedule) for schedule in schedules]  # Deserialize to DaySchedule
    except Exception as e:
        print(f"Error occurred while fetching schedules: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch schedules")

# Retrieve a day schedule by day
@router.get("/{day}", response_model=DaySchedule)
async def get_day_schedule(day: str):
    try:
        schedule_data = await collection_name.find_one({"day": day})
        print(f"Fetched schedule for {day}: {schedule_data}") 
        if schedule_data is None:
            raise HTTPException(status_code=404, detail="Day schedule not found")
        return DaySchedule(**schedule_data)  # Deserialize doc to DaySchedule
    except Exception as e:
        print(f"Error occurred while fetching schedule for day {day}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch day schedule")

# Create a new day schedule
@router.post("/", response_model=DaySchedule)
async def create_day_schedule(schedule: DaySchedule):
    try:
        # Check if a schedule for the specified day already exists
        existing_schedule = await collection_name.find_one({"day": schedule.day})
        if existing_schedule:
            raise HTTPException(status_code=400, detail="Schedule for this day already exists")

        # Insert the new schedule
        schedule_data = {
            "day": schedule.day,
            "todos": [todo.dict() for todo in schedule.todos]  # Serialize todos
        }
        await collection_name.insert_one(schedule_data)

        # Retrieve and return the created schedule
        created_schedule = await collection_name.find_one({"day": schedule.day})
        print(f"Created schedule: {created_schedule}")  
        return DaySchedule(**created_schedule)
    except Exception as e:
        print(f"Error occurred while creating schedule: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create day schedule")

# Update an existing day schedule by day
@router.put("/{day}", response_model=DaySchedule)
async def update_day_schedule(day: str, schedule: DaySchedule):
    try:
        # Prepare updated schedule data
        schedule_data = {
            "day": schedule.day,
            "todos": [todo.dict() for todo in schedule.todos]  # Serialize todos
        }

        # Perform the update
        result = await collection_name.update_one({"day": day}, {"$set": schedule_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Day schedule not found")

        # Retrieve and return the updated schedule
        updated_schedule = await collection_name.find_one({"day": day})
        return DaySchedule(**updated_schedule)
    except Exception as e:
        print(f"Error occurred while updating schedule for day {day}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update day schedule")
