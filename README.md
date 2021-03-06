###Optimal Locations for New Bay Area Bike Share Stations
####Website: http://optimalbikeshare.herokuapp.com/


I use a bike sharing program called Bay Area Bike Share (http://bayareabikeshare.com/). With Bay Area Bike Share, you can get a bike at any of the current 35 stations in the city and ride up to 30 minutes at a time to another station. I love it, especially since I don't have a car. However, the 35 Bay Area Bike Share stations in San Francisco (http://www.bayareabikeshare.com/stations) are only located in the Financial District and SOMA area. If I want to go to Golden Gate Park or Dolores Park, I'm out of luck.

![current stations](https://raw.githubusercontent.com/aluhrs/Optimal_Bike_Share_Locations/master/images/babikesharestations.png)

They are planning on expanding the program and create more stations around the city. Currently, people can vote for where they would like new stations to be on a crowdsourcing website (http://sfbikeshare.sfmta.com).

![http://sfbikeshare.sfmta.com)](https://raw.githubusercontent.com/aluhrs/Optimal_Bike_Share_Locations/master/images/crowdsourcing.png)

For my project, I decided I wanted to help them decide where to put new stations. I scraped the data from the crowdsourcing website, and I used the kmeans clustering algorithm to determine new locations. 

###K-means Clustering:
Given a dataset and the number of clusters desired, the data is partitioned into clusters and a single spot is created to represent each cluster.

![landing_page](https://raw.githubusercontent.com/aluhrs/Optimal_Bike_Share_Locations/master/images/cs_landing.png)

In addition to crowdsourced data, I've also included the ability for the user to choose locations based on the following options:

1. Elevation
2. Proximity to establishments that offer food such as Resturaunts, Cafes, and Bars
3. Proximity to Grocery Stores
4. Proximity to transportation such as Train Stations, Subway Stations, or Bus Stations
5. Proximity to other points of interest such as Parks, Shopping Malls, Movie Theaters, or Home Good Stores

The user can select any individual option or any combination of options to determine 100 optimal locations.

![elevation](https://raw.githubusercontent.com/aluhrs/Optimal_Bike_Share_Locations/master/images/elevation_1.png)
![all_options](https://raw.githubusercontent.com/aluhrs/Optimal_Bike_Share_Locations/master/images/all_options_1.png)

###Database Schema:
I set up my postgres (http://postgresapp.com/) database with three tables - the current stations, the data from the crowd sourcing website, and the optimized locations created from the clustering algorithm. Using Google Maps Elevation and Places API, I pulled elevation and points of interest data, such as transportation and grocery stores, for each crowd sourced point. 

###Ranking Points:
If a single point has similiar elevation to its surrounding points, the point would be ranked higher. I also ranked a point higher if it located within a certain distance to either grocery stores, transportation, restaurants, parks, movie theaters, or shopping malls.

###User Experience:
To create the fastest speeds and the best user experience, I ran all of the calculations beforehand. The optimal locations data is flagged with keys in the database, such as 'e' for elevation. For scalability, caching optimizations could be made.

###Possible Improvements:
I could improve my app by adding additional options such as crime or proximity to bike friendly routes. A more expansive improvement would be dynamically pulling newly created votes on the crowd sourcing webpage. A new vote would update my database, which would then recalculate the optimal locations. 

###Technologies Used:
1. Python/Javascript/jQuery/HTML/CSS/JSON/ajax
2. Flask
3. Postgres
4. Google Maps API - Elevation and Places
5. Beautiful Soup - Web Scraper
6. Scipy and Numpy - k-means Clustering Algorithm
7. Deployed on Heroku and Monitored with New Relic
