import logging


def calculate_coin(coin: float) -> float:
    logging.debug("Calculating coin size for {}".format(coin))
    if coin == 2:
        return 25.75
    elif coin == 1:
        return 23.25
    elif coin == 0.5:
        return 24.25
    elif coin == 0.20:
        return 22.25
    elif coin == 0.10:
        return 19.75
    elif coin == 0.05:
        return 21.25
    else:
        logging.info("Coin size not found")
        raise IndexError()
