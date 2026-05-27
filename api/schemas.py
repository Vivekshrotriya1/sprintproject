from pydantic import BaseModel

class SalesInput(BaseModel):

    Store: int
    Dept: int
    IsHoliday: int
    Temperature: float
    Fuel_Price: float
    MarkDown1: float
    MarkDown2: float
    MarkDown3: float
    MarkDown4: float
    MarkDown5: float
    CPI: float
    Unemployment: float
    Size: int
    Year: int
    Month: int
    Week: int
    Type_B: int
    Type_C: int