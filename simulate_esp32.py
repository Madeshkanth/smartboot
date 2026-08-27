import requests
import time
import random

URL = "http://127.0.0.1:5000/api/boot-data"

reading_count = 0

while True:

    # Simulate left and right FSR values
    left = random.randint(0, 100)
    right = random.randint(0, 100)

    # Calculate average
    average = (left + right) // 2

    reading_count += 1

    print(
        f"Reading {reading_count} | "
        f"Left: {left}% | "
        f"Right: {right}% | "
        f"Average: {average}%"
    )

    # Send only every 3rd reading
    if reading_count == 3:

        print(f">>> Sending average: {average}%")

        response = requests.post(
            URL,
            json={"average": average}
        )

        print("Server response:", response.json())

        reading_count = 0

    time.sleep(2)