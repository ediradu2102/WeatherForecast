from app import db


class WeatherForecast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    max_temperature = db.Column(db.Float, nullable=False)
    min_temperature = db.Column(db.Float, nullable=False)
    total_precipitation = db.Column(db.Float, nullable=False)
    sunrise = db.Column(db.String(5), nullable=False)
    sunset = db.Column(db.String(5), nullable=False)

    def __repr__(self):
        return f"<WeatherForecast {self.city}, Date: {self.date}>"

    def to_dict(self):
        """
        Converts the WeatherForecast instance to a dictionary.
        """
        return {
            "id": self.id,
            "city": self.city,
            "date": self.date,
            "max_temperature": self.max_temperature,
            "min_temperature": self.min_temperature,
            "total_precipitation": self.total_precipitation,
            "sunrise": self.sunrise,
            "sunset": self.sunset
        }
