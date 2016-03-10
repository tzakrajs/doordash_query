# DDQ: Doordash Query

## What?
This is a script that you can use to look for specific food items. It produces an output similar to the following:
```
./ddq.py burrito spicy
==================================
Results: 3
==================================
Name: Chorizo Burrito
Description: Spicy chorizo, egg, country potatoes & cheese.
Price: $7.50
Restaurant: Cafe Rosalena
Category: All-Day Breakfast
URL: https://www.doordash.com/store/cafe-rosalena-san-jose-34847/
==================================
Name: Spicy Tofusion Burrito
Description: No Rice or beans, Grilled fajita mix, tofu, cabbage with a spicy garlic chipotle sauce.
Price: $6.99
Restaurant: Una Mas
Category: Burritos
URL: https://www.doordash.com/store/una-mas-san-jose-1454/
==================================
Name: SCReaM'n Burrito
Description: Spicy chicken with rice, cheese, mushrooms, flavored with our green sauce and famous Mr. Lee's spicy chili sauce.
Price: $8.50
Restaurant: Wahoo's Fish Taco
Category: Burritos
URL: https://www.doordash.com/store/wahoo-s-fish-taco-san-jose-537/
==================================
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
