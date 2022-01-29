from cs50 import get_float


def get_change():
    while True:
        change = get_float("change due? ")
        if change > 0:
            break
    return change * 100

    
def give_coins(change):
    coins = 0
    cents = change
    while True:    
        if cents == 0:
            break
        elif cents >= 25:
            cents = cents - 25
            coins += 1
        elif cents >= 10 and cents < 25:
            cents = cents - 10
            coins += 1
        elif cents >= 5 and cents < 10:
            cents = cents - 5
            coins += 1
        elif cents >= 1 and cents < 5:
            cents = cents - 1
            coins += 1
    print(coins)
    
                
def main():
    give_coins(get_change())
    
    
main()    
            