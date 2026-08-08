import asyncio
from app.adapters.weather import OpenMeteoAdapter


async def main():
    # Thiruvananthapuram
    lat = 8.5241
    lon = 76.9366

    weather = await OpenMeteoAdapter.fetch_current_weather(lat, lon)

    if weather is None:
        print("Failed to fetch weather.")
        return

    print("===== Weather =====")
    print(weather)

    # If WeatherModule is a Pydantic model
    if hasattr(weather, "model_dump"):
        print("\nAs Dictionary:")
        print(weather.model_dump())


if __name__ == "__main__":
    asyncio.run(main())