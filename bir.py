import json, config, time
from binance.client import Client
from binance.enums import *


client = Client(config.API_KEY, config.API_SECRET, tld='com')


def order(symbol, side, sideSP, quantity, stopPriceSL, stopPriceTP1, stopPriceTP2, stopPriceTP3, type='MARKET'):
    try:
        poz_info = client.futures_position_information(symbol=symbol)
	pozAmt = float(poz_info[-1]['positionAmt'])
	q13 = int(-1*quantity//3*-1)
        if pozAmt == 0:
            co = client.futures_cancel_all_open_orders(symbol=symbol)
            print(f"sending order {type} - {side} {quantity} {symbol}")
            order = client.futures_create_order(symbol=symbol, side=side, type=type, quantity=quantity)
            orderSL = client.futures_create_order(symbol=symbol,side=sideSP, reduceOnly=True, type='STOP_MARKET', quantity=quantity, stopPrice=stopPriceSL)
            orderTP1 = client.futures_create_order(symbol=symbol,side=sideSP, reduceOnly=True, type='TAKE_PROFIT_MARKET', quantity=q13, stopPrice=stopPriceTP1)
            orderTP2 = client.futures_create_order(symbol=symbol,side=sideSP, reduceOnly=True, type='TAKE_PROFIT_MARKET', quantity=q13, stopPrice=stopPriceTP2)
            orderTP3 = client.futures_create_order(symbol=symbol,side=sideSP, reduceOnly=True, type='TAKE_PROFIT_MARKET', quantity=int(quantity-q13*2), stopPrice=stopPriceTP3)
        elif pozAmt > 0 and side == 'SELL':
	    co = client.futures_cancel_all_open_orders(symbol=symbol)
	    orderS = client.futures_create_order(symbol=symbol, side=side, type=type, quantity=int(pozAmt))
	    time.sleep(5)
	    order = client.futures_create_order(symbol=symbol, side=side, type=type, quantity=quantity)
            orderSL = client.futures_create_order(symbol=symbol,side=sideSP, reduceOnly=True, type='STOP_MARKET', quantity=quantity, stopPrice=stopPriceSL)
            orderTP1 = client.futures_create_order(symbol=symbol,side=sideSP, reduceOnly=True, type='TAKE_PROFIT_MARKET', quantity=q13, stopPrice=stopPriceTP1)
            orderTP2 = client.futures_create_order(symbol=symbol,side=sideSP, reduceOnly=True, type='TAKE_PROFIT_MARKET', quantity=q13, stopPrice=stopPriceTP2)
            orderTP3 = client.futures_create_order(symbol=symbol,side=sideSP, reduceOnly=True, type='TAKE_PROFIT_MARKET', quantity=int(quantity-q13*2), stopPrice=stopPriceTP3)
	elif pozAmt < 0 and side == 'BUY':
	    co = client.futures_cancel_all_open_orders(symbol=symbol)
	    orderS = client.futures_create_order(symbol=symbol, side=side, type=type, quantity=int(pozAmt))
	    time.sleep(5)
	    order = client.futures_create_order(symbol=symbol, side=side, type=type, quantity=quantity)
            orderSL = client.futures_create_order(symbol=symbol,side=sideSP, reduceOnly=True, type='STOP_MARKET', quantity=quantity, stopPrice=stopPriceSL)
            orderTP1 = client.futures_create_order(symbol=symbol,side=sideSP, reduceOnly=True, type='TAKE_PROFIT_MARKET', quantity=q13, stopPrice=stopPriceTP1)
            orderTP2 = client.futures_create_order(symbol=symbol,side=sideSP, reduceOnly=True, type='TAKE_PROFIT_MARKET', quantity=q13, stopPrice=stopPriceTP2)
            orderTP3 = client.futures_create_order(symbol=symbol,side=sideSP, reduceOnly=True, type='TAKE_PROFIT_MARKET', quantity=int(quantity-q13*2), stopPrice=stopPriceTP3)
	else:
            print("non order")
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return order, orderSL, orderTP1, orderTP2, orderTP3


def Signal(msg):
    

    if msg['passphrase'] == config.ZZ_PASSPHRASE:
        
        symbol = msg['symbol'][:-2]

        side = msg['sid']

        price = float(msg['price'])

        quantity = 11 // price

        if side == 'SELL':
            sideSP = 'BUY'
            stopPriceSL = format(price + (price * 0.0065),'.4f')
            stopPriceTP1 = format(price - (price * 0.0065),'.4f')
            stopPriceTP2 = format(price - (price * 0.011),'.4f')
            stopPriceTP3 = format(price - (price * 0.02),'.4f')
        elif side == 'BUY':
            sideSP = 'SELL'
            stopPriceSL = format(price - (price * 0.0065),'.4f')
            stopPriceTP1 = format(price + (price * 0.0065),'.4f')
            stopPriceTP2 = format(price + (price * 0.011),'.4f')
            stopPriceTP3 = format(price + (price * 0.02),'.4f')
        else:
            return {
                "code": "error",
                "message": "sideSP failed"
            }
                
        order_response = order(symbol, side, sideSP, quantity, stopPriceSL, stopPriceTP1, stopPriceTP2, stopPriceTP3)

    else:
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }