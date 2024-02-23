This web application is designed to return information about the weather in a given city for the next 3 days.

To use the application, the program must be started, and the link http://127.0.0.1:5000 must be accessed.

The first page will appear containing a textbox where you can enter the name of the city and two buttons.

The button on the left will send the user to a page where they will see information about the weather of the respective day, such as an image, the maximum temperature,
the minimum temperature and the condition of that day (extracted from www.weatherapi.com) for the next 3 days (excluding the day from today) for the requested city.

The button on the right will send the user to a page where they will see information about the weather of the respective day at every hour. The time,
an image, the rounded celsius grids and the condition will be shown (all these extracted from www.weatherapi.com) for the next 3 days (excluding today) for the requested city.

Every time the user searches for information about a city, if that city and that date are not in the database, the date, city, maximum temperature, minimum temperature,
total precipitation, sunset time and sunrise time will be added to the database (all these extracted from www.weatherapi.com)

The endpoins "/all" and "/<cityName>" where created only to have some interaction with the database. They can be acessed with Postmamn using:

GET: http://127.0.0.1:5000/all (to get all the data in the database) and

GET: http://127.0.0.1:5000/{cityName} (to get all the data in the database about the given city)

The program can also be used by accessing Postman

For up-to-date data: GET: http://127.0.0.1:5000/forecast/daily/<city_name>

For the dates at the time: GET: http://127.0.0.1:5000/forecast/hourly/<city_name>

Hovewer, a raw html page will be returned.
