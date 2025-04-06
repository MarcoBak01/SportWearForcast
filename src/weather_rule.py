class WeatherRule:
    def __init__(self, condition, action):
        self.condition = condition
        self.action = action

    def apply(self, weather_data):
        raise NotImplementedError("Subclasses should implement this method.")

class TemperatureRule(WeatherRule):
    def __init__(self, min_temp, max_temp, action):
        super().__init__("temperature", action)
        self.min_temp = min_temp
        self.max_temp = max_temp

    def apply(self, weather_data):
        temp = weather_data["main"]['temp']
        feel_temp = weather_data["main"]['feels_like']
        if self.min_temp <= temp <= self.max_temp:
            return f"Today it is {temp} degrees, that feels like {feel_temp}. " + self.action
        return None

class WindRule(WeatherRule):
    def __init__(self, min_wind_speed, action):
        super().__init__("wind", action)
        self.min_wind_speed = min_wind_speed

    def apply(self, weather_data):
        wind_speed = round(weather_data['wind']['speed'] * 3.6, 2)  # Convert m/s to kph
        if wind_speed >= self.min_wind_speed:
            return f"Windspeed of {wind_speed} kph. " + self.action
        return None

class RainRule(WeatherRule):
    def __init__(self, action):
        super().__init__("rain", action)

    def apply(self, weather_data):
        weather_type = str(weather_data['weather'][0]['id'])
        if weather_type.startswith('3') or weather_type.startswith('5'):
            return "It will be raining. " + self.action
        return None
    
class ThunderStormRule(WeatherRule):
    def __init__(self, action):
        super().__init__("thunder storm", action)

    def apply(self, weather_data):
        weather_type = str(weather_data['weather'][0]['id'])
        if weather_type.startswith('2'):
            return self.action
        return None

# NOTE Cannot be used for this, Subsription should be ugraded to ONE call 3.0    
class UVIndexRule(WeatherRule):
    def __init__(self):
        super().__init__("uv_index", "Don\'t forget to wear sunscreen!")

    def apply(self, weather_data):
        uv_index = weather_data['uvindex']
        if uv_index >= 3:
            return f"UV Index of {uv_index}. " + self.action
        return None
