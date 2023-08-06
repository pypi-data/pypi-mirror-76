import unittest
import os
from pyiqoptionapi import IQOption
import logging
import time
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')


#579121
email = "cayem28791@mail2paste.com"
password = "testerforapi2020"


class TestCandle(unittest.TestCase):
  
    def test_Candle(self):
        #login
        I_want_money=IQOption(email, password)
        I_want_money.connect()
        I_want_money.change_balance("PRACTICE")
        I_want_money.reset_practice_balance()
        self.assertEqual(I_want_money.check_connect(), True)
        ALL_Asset=I_want_money.get_all_open_time()
        if ALL_Asset["turbo"]["EURUSD"]["open"]:
            ACTIVES="EURUSD"
        else:
            ACTIVES="EURUSD-OTC"
        I_want_money.get_candles(ACTIVES, 60, 1000, time.time())
        size="all"
        I_want_money.start_candles_stream(ACTIVES, size,10)
        I_want_money.get_realtime_candles(ACTIVES, size)
        I_want_money.stop_candles_stream(ACTIVES, size)
