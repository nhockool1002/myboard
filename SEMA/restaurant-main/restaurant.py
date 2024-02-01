# imports
import os
import random

# Wipe terminal on every start
os.system('cls' if os.name == 'nt' else 'clear')

# Lists
menuItems = ['French Fries', '1/4 Pound Burger', '1/4 Pound Cheeseburger', '1/2 Pound Burger', '1/2 Pound Cheeseburger', 'Medium Pizza', 'Medium Pizza + Extra Toppings', 'Large Pizza', 'Large Pizza + Extra toppings', 'Garlic bread']
menuPrices = [2.00, 5.00, 5.55, 7.00, 7.50, 9.00, 11.00, 12.00, 14.50, 4.50]
menuCodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Show menu
def displayMenu():
    print('\t\tMENU')
    print('------------------------------------------------------------------')
    print('Code\t\tItem\t\t\t\t\tPrice')
    print('------------------------------------------------------------------')
    for menu in range(len(menuItems)):
        print(f'{menuCodes[menu]}\t\t{menuItems[menu]:<30}\t\t${menuPrices[menu]:.2f}')
    print('------------------------------------------------------------------')

displayMenu()



orderItems = []
orderAmount = []
orderPrice = []

zippedlist = zip(orderItems, orderAmount)

# Get user input
def get_order():


    while True:
            activeOrder = int(input('Please put in the code of the item you want to order (to end type 10): '))

            if activeOrder == 10:
                break

            orderItems.append(menuItems[activeOrder])

            if activeOrder == 10:
                print('invalid code')
            else:
                print('You have chosen: ', menuItems[activeOrder])
                amount = int(input('How much of this item? '))
                orderAmount.append(amount)
                orderPrice.append(amount * menuPrices[activeOrder])
            
get_order()

# Clear terminal to display receipt cleanly
os.system('cls' if os.name == 'nt' else 'clear')

# Print receipt
def receipt():
    numReceipt = random.randint(1695,40501)
    print(f'\t\t\tRECEIPT | #{numReceipt}')
    print('------------------------------------------------------------------')
    print('Items\t\t\t\tAmount')
    print('------------------------------------------------------------------')
    for allitems in zip(orderItems, orderAmount):
        print(f'{orderItems}\t\t{orderAmount}\t\t')
    print('------------------------------------------------------------------')
    print(f'The total price for your order is: ${sum(orderPrice)}')



receipt()
