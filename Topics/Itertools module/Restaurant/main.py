import itertools

budget = 30
main_courses = ['beef stew', 'fried fish']
price_main_courses = [28, 23]

desserts = ['ice-cream', 'cake']
price_desserts = [2, 4]

drinks = ['cola', 'wine']
price_drinks = [3, 10]

for food, price in zip(itertools.product(main_courses, desserts, drinks), itertools.product(price_main_courses, price_desserts, price_drinks)):
    if sum(price) <= budget:
        print(*food, sum(price))




