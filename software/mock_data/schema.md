# Smart Greenhouse – Data Schema (v1)

## Measurement: `greenhouse_env`
| Category | Key              | Type   | Example | Description |
|-----------|------------------|--------|----------|--------------|
| **Tags**  | sensor_id        | str    | esp32-1  | Unique device ID |
|           | zone             | str    | A        | Zone name (bed/section) |
|           | plant            | str    | basil    | Plant species or ID |
| **Fields**| air_temp_c       | float  | 24.7     | Air temperature (°C) |
|           | rel_humidity     | float  | 52.3     | Relative humidity (%) |
|           | soil_moisture    | float  | 0.41     | Normalized 0–1 |
|           | light_on         | int    | 1        | 1 = on, 0 = off |
|           | fan_on           | int    | 0        | 1 = on, 0 = off |
|           | pump_on          | int    | 1        | 1 = on, 0 = off |
|           | water_tank_level | float  | 0.76     | 0–1 normalized tank level |
| **Time**  | timestamp        | ISO8601| ...Z     | UTC timestamp |
