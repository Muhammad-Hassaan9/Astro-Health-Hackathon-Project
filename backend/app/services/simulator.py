import random
from datetime import datetime, timezone

def generate_health_reading() -> dict:
    """
    Generate simulated health readings for an astronaut.

    Scenarios:
    - 70% normal readings
    - 10% abnormal heart rate
    - 10% low SpO2
    - 10% abnormal body temperature

    Synthetic data for prototype and dashboard testing only.
    """

    scenario = random.choices(
        population=[
            "normal",
            "heart_rate_alert",
            "spo2_alert",
            "temperature_alert",
        ],
        weights=[70, 10, 10, 10],
        k=1,
    )[0]

    # Generate normal readings by default.
    heart_rate = round(random.uniform(60, 100), 1)
    spo2 = round(random.uniform(95, 100), 1)
    body_temperature = round(random.uniform(36.1, 37.5), 1)

    # Generate one abnormal reading depending on the scenario.
    if scenario == "heart_rate_alert":
        heart_rate = round(random.choice([
            random.uniform(45, 59.9),
            random.uniform(100.1, 115),
        ]), 1)

    elif scenario == "spo2_alert":
        spo2 = round(random.uniform(85, 94.9), 1)

    elif scenario == "temperature_alert":
        body_temperature = round(random.choice([
            random.uniform(34.5, 35.9),
            random.uniform(38.1, 39.5),
        ]), 1)

    return {
        "heart_rate": heart_rate,
        "spo2": spo2,
        "body_temperature": body_temperature,
        "physical_activity": round(random.uniform(0, 100), 1),
        "sleep_duration": round(random.uniform(5, 9), 1),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "data_status": "SIMULATED",
    }

def generate_health_readings(count: int = 1) -> list[dict]:
    """Generate multiple simulated health readings."""

    if count < 1 or count > 1000:
        raise ValueError("Count must be between 1 and 1000.")

    return [
        generate_health_reading()
        for _ in range(count)
    ]