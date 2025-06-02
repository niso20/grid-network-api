import os
import time
import statistics
import json
from collections import deque
from typing import Optional
from Utilities import convertTimeToTimestamp


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
        if timestamp is None:
            timestamp = time.time()

        # Store the reading
        self.frequency_buffer.append(frequency)
        self.timestamp_buffer.append(timestamp)

        # Calculate ROCOF if we have previous reading
        if self.previous_frequency is not None and self.previous_timestamp is not None:
            delta_f = frequency - self.previous_frequency
            delta_t = timestamp - self.previous_timestamp

            if delta_t > 0:
                rocof = delta_f / delta_t
                self.rocof_buffer.append(rocof)

                # Update previous values
                self.previous_frequency = frequency
                self.previous_timestamp = timestamp

                return rocof

        # First reading - store as previous
        self.previous_frequency = frequency
        self.previous_timestamp = timestamp
        return None

    def process_frequency_data(self, normalized_payload: dict) -> dict:
        """
        Process frequency data and calculate ROCOF if the payload contains frequency information

        Args:
            normalized_payload: The normalized MQTT payload

        Returns:
            Enhanced payload with ROCOF data if frequency found
        """
        # Check if this is a frequency payload
        if normalized_payload.get("id") == "frequency":
            time = normalized_payload.get("t")

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

                    except (ValueError, TypeError) as e:
                        print(f"[ERROR] Could not parse frequency value '{frequency_str}': {e}")

        return rocof

    def get_instantaneous_rocof(self) -> Optional[float]:
        """Get the most recent ROCOF calculation"""
        return self.rocof_buffer[-1] if self.rocof_buffer else None

    def is_rocof_alarm(self, threshold: float = 0.5) -> bool:
        """
        Check if ROCOF exceeds alarm threshold

        Args:
            threshold: ROCOF threshold in Hz/s (typical: 0.5 Hz/s)

        Returns:
            True if ROCOF alarm condition met
        """
        rocof = self.get_instantaneous_rocof()
        if rocof is None:
            return False

        return abs(rocof) > threshold