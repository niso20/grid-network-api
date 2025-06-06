import os
import time
from datetime import datetime
import statistics
import json
from middlewares.DbMiddleware import DB
from database import engine, SessionLocal
from collections import deque
from typing import Optional, TypedDict
from Utilities import convertTimeToTimestamp
from models.Frequency import Frequency

class FrequencyType(TypedDict):
    f: Optional[float] = None
    t: Optional[str] = None
    df: Optional[float] = None
    dt: Optional[float] = None
    rocof: Optional[float] = None

class FrequencyService:
    def __init__(self, db:DB):
        self.__db = db

    def save(self, data:FrequencyType):
        # print(data)
        FrequencyModel = Frequency(
            f=data["f"],
            t=data["t"],
            df=data.get("df"),
            dt=data.get("dt"),
            rocof=data.get("rocof"),
        )

        self.__db.add(FrequencyModel)
        self.__db.commit()
        self.__db.refresh(FrequencyModel)

        return FrequencyModel

    def getRocof(self):
        query = self.__db.query(Frequency)
        query = query.filter(Frequency.rocof.isnot(None))

        return query.order_by(Frequency.created_at.desc()).limit(300).all()

    def getLatestRocof(self):
        return (
            self.__db.query(Frequency)
            .filter(Frequency.rocof.isnot(None))
            .order_by(Frequency.created_at.desc())  # or Frequency.id.desc()
            .first()
        )


class ROCOFCalculator:
    def __init__(self, window_size: int = 10, sampling_interval: float = 2.0):
        """
        Initialize ROCOF calculator

        Args:
            window_size: Number of samples to keep for moving average (default: 10)
            sampling_interval: Time between samples in seconds (default: 2.0)
        """
        self.window_size = window_size
        self.sampling_interval = sampling_interval

        # Store frequency readings with timestamps
        self.frequency_buffer = deque(maxlen=window_size)
        self.timestamp_buffer = deque(maxlen=window_size)

        # Store ROCOF values for analysis
        self.rocof_buffer = deque(maxlen=window_size)
        self.rocof_series = deque(maxlen=window_size)

        self.previous_frequency = None
        self.previous_timestamp = None

    def add_frequency_reading(self, frequency: float, timestamp: Optional[float] = None) -> Optional[float]:
        """
        Add new frequency reading and calculate ROCOF

        Args:
            frequency: Frequency value in Hz
            timestamp: Unix timestamp (optional, uses current time if None)

        Returns:
            ROCOF value in Hz/s, or None if insufficient data
        """
        # print("Add frequency reading")
        if timestamp is None:
            timestamp = time.time()

        df = None
        dt = None
        rocof = None
        t = datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")

        # Store the reading
        self.frequency_buffer.append(frequency)
        self.timestamp_buffer.append(timestamp)

        # print("Add frequency reading")

        # Calculate ROCOF if we have previous reading
        if self.previous_frequency is not None and self.previous_timestamp is not None:
            delta_f = frequency - self.previous_frequency
            delta_t = timestamp - self.previous_timestamp

            df = delta_f
            dt = delta_t

            # print(delta_f)
            # print(delta_t)

            if delta_t > 0:
                rocof = delta_f / delta_t
                if rocof is not None:
                    rocof = round(rocof, 3)

                self.rocof_buffer.append(rocof)

                self.rocof_series.append({"rocof": rocof, "t": t})



                # Update previous values
                self.previous_frequency = frequency
                self.previous_timestamp = timestamp

        db = SessionLocal()
        frequencyService = FrequencyService(db)
        data = {"f": frequency, "t": t}
        if df is not None:
            data["df"] = df

        if dt is not None:
            data["dt"] = dt

        if rocof is not None:
            data["rocof"] = rocof

        frequencyService.save(data)

        # First reading - store as previous
        self.previous_frequency = frequency
        self.previous_timestamp = timestamp
        return rocof

    def process_frequency_data(self, normalized_payload: dict) -> dict:
        """
        Process frequency data and calculate ROCOF if the payload contains frequency information

        Args:
            normalized_payload: The normalized MQTT payload

        Returns:
            Enhanced payload with ROCOF data if frequency found
        """
        rocof = None
        # Check if this is a frequency payload
        if any(normalized_payload.get(key) == "phoenix" for key in ["id", "name"]):
            # print("process frequency")
            time = normalized_payload.get("t")
            # print(time)

            # Look for frequency data in components
            for component in normalized_payload.get("components", []):
                if "f" in component.get("data", {}):
                    try:
                        # Extract frequency value
                        frequency_str = component["data"]["f"]
                        frequency_value = float(frequency_str)

                        # Calculate ROCOF
                        timestamp = None
                        if time is not None:
                            timestamp = convertTimeToTimestamp(time)

                        rocof = self.add_frequency_reading(frequency_value, timestamp)
                        # print("rocof")
                        # print(rocof)

                    except (ValueError, TypeError) as e:
                        print(f"[ERROR] Could not parse frequency value '{frequency_str}': {e}")

        return rocof

    def getInstantaneousRocof(self) -> Optional[float]:
        """Get the most recent ROCOF calculation"""
        return self.rocof_buffer[-1] if self.rocof_buffer else None

    def getRocofStatistics(self) -> dict:
        """Get current ROCOF statistics"""
        rocof_values = list(self.rocof_buffer)

        if not rocof_values:
            return {"status": "no_data"}

        return {
            "current_rocof": rocof_values[-1],
            "average_rocof": statistics.mean(rocof_values),
            "max_rocof": max(rocof_values),
            "min_rocof": min(rocof_values),
            "sample_count": len(rocof_values),
            "alarm_status": self.is_rocof_alarm()
        }

    def getRocofValues(self) -> dict:
        """Get current ROCOF statistics"""
        rocof_values = dict(self.rocof_series)

        if not rocof_values:
            return {}

        return rocof_values


    def is_rocof_alarm(self, threshold: float = 0.5) -> bool:
        """
        Check if ROCOF exceeds alarm threshold

        Args:
            threshold: ROCOF threshold in Hz/s (typical: 0.5 Hz/s)

        Returns:
            True if ROCOF alarm condition met
        """
        rocof = self.getInstantaneousRocof()
        if rocof is None:
            return False

        return abs(rocof) > threshold