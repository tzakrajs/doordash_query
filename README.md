# DDQ: Doordash Query

## What?
This is a script that you can use to look for specific food items. It produces an output similar to the following:
```
./ddq.py cookie
==================================
Results: 26
==================================
Name: Pizza Cookie
Description: Your choice of warm chocolate chip or white macadamia cookie topped w/ vanilla bean ice cream
Price: $8.50
Restaurant: 4th St. Pizza Co
Category: Dessert
URL: https://www.doordash.com/store/4th-st-pizza-co-san-jose-11027/16578/
==================================
Name: Pizooke Two Flavor
Description: Our famous, hot and freshly baked cookie topped with two scoops of vanilla bean ice cream and served in its own deep dish. Choose two-flavors for a half and half, Pizookie good time!
Price: $7.95
Restaurant: BJ's (Bay Area)
Category: Desserts
URL: https://www.doordash.com/store/bj-s-downtown-san-jose-2901/4294/
==================================
Name: Pizooke Two Flavor
Description: Our famous, hot and freshly baked cookie topped with two scoops of vanilla bean ice cream and served in its own deep dish. Choose two-flavors for a half and half, Pizookie good time!
Price: $7.50
Restaurant: BJ's (Downtown San Jose: Lunch)
Category: Desserts
URL: https://www.doordash.com/store/bj-s-downtown-san-jose-2901/16428/
==================================
Name: Chocolate Cream Pie
Description: Rich chocolate cream in a chocolate cookie crust. Topped with whipped cream.
Price: $6.95
Restaurant: Black Bear Diner All Day (Milpitas)
Category: Desserts
URL: https://www.doordash.com/store/black-bear-diner-milpitas-8145/48236/
==================================
…
```

## Configuration/Installation
First, you will want to install the requirements:
```
pip install -r requirements.txt
```

Then, you will want to modify the LATITUDE and LONGITUDE constants:
```
LATITUDE = 37.371941
LONGITUDE = -121.886283
```

## Thanks!
Big thanks to Doordash for a fantastic service, I just wanted a better way to search their menus, since it isn't always easy to find a menu item that is buried deep in the many restaurant pages.

Happy Doordashing!
