import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import numpy as np

start = datetime(2025, 1, 1)
end = start + timedelta(days=10)
date_range = pd.date_range(start=start, end=end, freq="1min")

df = pd.DataFrame({
    "timestamp": date_range,
    "wind_speed": np.random.uniform(3, 20, size=len(date_range)),
    "power": np.random.uniform(0, 1000, size=len(date_range)),
    "ambient_temprature": np.random.uniform(-5, 35, size=len(date_range))
})

engine = create_engine("postgresql://postgres:postgres@fonte_db:5432/fonte_db")
df.to_sql("data", engine, index=False, if_exists="replace")
