# tenmen-tracker

Python web app for tracking, analyzing and visualizing match data from CSGO matches played on the scrim service [PopFlash](https://popflash.site/). The [match extracion](/match_extraction) module [scrapes](https://en.wikipedia.org/wiki/Web_scraping) the PopFlash match page and extracts the match data. The [database management](/database_management) module accepts the match data and adds it to a MySQL database. The ``__init__.py`` is the [Flask](https://flask.palletsprojects.com/en/1.1.x/) based Python backend interacting with the database and webscraper to present the stored matches and match data to the website. It also allows users to add their matches to be included as part of the total statistics.

A live demo of the website can be found [here](http://jakobvahlin.com/tenman)

![Website screenshots](README/readme_img.png)

## Table of Contents
- [Dependencies](#dependencies)
- [Hosting your own Web App](#hosting-your-own-web-app)
    - [Quickstart](#quickstart)
- [The match extraction module](#the-match-exctraction-module)    
- [The database management module](#the-database-management-module)

## Dependencies
The requried dependencies for the database management module, the match extraction module and the entire Wep App are specified in the [requirements.txt](requirements.txt) file. If you want to install **all** the dependencies run

``` ~$ pip install -r requirements.txt```

If you only want to install the dependencies for a specific module, see the requirements.txt file for the dependencies corresponding to the module of choice.
## Hosting the Web App

### Quickstart
Make sure you have installed the required [dependencies](#dependencies). If you are familiar with Python based web development and already have a MySQL database and Apache2 (or similar) on your server, clone this project into the folder hosting your web app. You will have to alter the login details of the database management module to match your own database. 


### Running on Ubuntu/Linux-based host system
There are several ways to host (Python based) web applications. If you are new to the field, I can recommend a [Digital Ocean droplet](https://www.digitalocean.com/products/droplets/) for hosting your web app. They will set you back $5 USD a month, however offer loads of great tutorial for beginners. To deploy the tenman-tracker Flask app, follow [this tutorial](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps). Navigate to the folder hosting your web app

```~$ cd /var/www/<FlaskApp>/<FlaskApp>```

and clone the git repository into the folder

``` ~$ git clone git@github.com:jakvah/tenmen-tracker.git```

## The match exctraction module

The match extraction module containes a simple Web Scraper that searches the match page of a given match ID and extracts relevant match data. Additionally it contains custom `Match`, ``Player`` and ``Team`` classes, which makes it easier to work with the match data.

A simple code example illustrating the usage of the classes and some of their class methods is shown below

```python
from match_extraction import popflash_scraper as ps
from match_extraction.Match import Match
from match_extraction.Team import Team
from match_extraction.Player import Player

# Get match data in an instance of the Match class
match_id = 123
match = ps.get_match_data(match_id)

# Get data for winning team in an instance of the Team class
winning_team = match.get_winner()
winning_team_score = winning_team.get_score()

# The team class is iterable, so we can iterate through the players in the team, and print each player (the Player class has a __str__ method)
for player in winning_team:
    print(player)

# Get the top player from the match in an instance of the Player class
top_player = match.get_highest_rated()
top_player_nick = top_player.get_nick()
```

For more class methods, see the source code for the various classes

## The database management module

