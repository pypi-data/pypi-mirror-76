# -*- coding: utf-8 -*-
from pyiqoptionapi.api.api import IQOptionAPI
import pyiqoptionapi.helpers.country_id as Country
import threading
import time
import logging
import operator
from collections import defaultdict
from collections import deque
from pyiqoptionapi.helpers.expiration import get_expiration_time, get_remaning_time
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.NullHandler())

websocket_logger = logging.getLogger("websocket")
websocket_logger.setLevel(logging.INFO)
websocket_logger.addHandler(logging.NullHandler())


__all__ = ['IQOption', ]


def nested_dict(n, type_dict):
    if n == 1:
        return defaultdict(type_dict)
    else:
        return defaultdict(lambda: nested_dict(n - 1, type_dict))


class IQOption:

    __version__ = "1.1.100"
    __status__ = "production"

    def __init__(self, email, password):
        self.size = [1, 5, 10, 15, 30, 60, 120, 300, 600, 900, 1800,
                     3600, 7200, 14400, 28800, 43200, 86400, 604800, 2592000]
        self.email = email
        self.password = password
        self.suspend = 0.5
        self.thread = None
        self._lock_candle = threading.RLock()
        self.subscribe_candle = []
        self.subscribe_candle_all_size = []
        self.subscribe_mood = []
        # for digit
        self.get_digital_spot_profit_after_sale_data = nested_dict(2, int)
        self.get_realtime_strike_list_temp_data = {}
        self.get_realtime_strike_list_temp_expiration = 0
        self.SESSION_HEADER = {
            "User-Agent": r"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}
        self.SESSION_COOKIE = {}
        self.api = None

    @property
    def actives(self):
        return self.api.actives

    @actives.setter
    def actives(self, actives):
        self.api.actives = actives

    def get_server_timestamp(self):
        return self.api.timesync.server_timestamp

    def re_subscribe_stream(self):
        try:
            with self._lock_candle:
                for ac in self.subscribe_candle:
                    sp = ac.split(",")
                    self.start_candles_one_stream(sp[0], sp[1])
        except Exception as e:
            logging.error('re-subscribe-stream -> {}'.format(e))

        try:
            with self._lock_candle:
                for ac in self.subscribe_candle_all_size:
                    self.start_candles_all_size_stream(ac)
        except Exception as e:
            logging.error('re-subscribe-stream -> {}'.format(e))

        try:
            with self._lock_candle:
                for ac in self.subscribe_mood:
                    self.start_mood_stream(ac)
        except Exception as e:
            logging.error('re-subscribe-stream -> {}'.format(e))

    def set_session(self, header, cookie):
        self.SESSION_HEADER = header
        self.SESSION_COOKIE = cookie

    @property
    def balance_id(self):
        return self.api.global_value.balance_id

    def connect(self):
        self.api = IQOptionAPI("iqoption.com", self.email, self.password)
        check = False
        self.api.set_session(headers=self.SESSION_HEADER, cookies=self.SESSION_COOKIE)
        check, reason = self.api.connect()
        if check:
            self.re_subscribe_stream()
            start = time.time()
            while 1:
                if self.api.global_value.balance_id:
                    break
                if time.time() - start > 10:
                    return False, 'The balance ID is unavailable. Response timeout.'
                time.sleep(.1)
            self.position_change_all("subscribeMessage", self.api.global_value.balance_id)
            self.order_changed_all("subscribeMessage")
            self.api.setOptions(1, True)
            return True, None
        else:
            return False, reason

    def check_connect(self):
        return bool(self.api.global_value.check_websocket_if_connect)

    def get_all_actives(self):
        return self.actives

    def update_actives(self):
        # update from binary option
        self.get_ALL_Binary_ACTIVES_OPCODE()
        # crypto /dorex/cfd
        self.instruments_input_all_in_ACTIVES()
        dicc = {}
        for lis in sorted(self.actives.items(), key=operator.itemgetter(1)):
            dicc[lis[0]] = lis[1]
        self.actives(dicc)

    def get_name_by_activeId(self, activeId):
        info = self.get_financial_information(activeId)
        try:
            return info["msg"]["data"]["active"]["name"]
        except:
            return None

    def get_financial_information(self, activeId):
        with self.api.lock_financial_info:
            self.api.financial_information = None
        self.api.get_financial_information(activeId)
        time.sleep(.2)
        start = time.time()
        while 1:
            if time.time() - start > 10:
                raise TimeoutError
            with self.api.lock_financial_info:
                if self.api.financial_information != None:
                    return self.api.financial_information

    def get_leader_board(self, country, from_position, to_position, near_traders_count, user_country_id=0,
                         near_traders_country_count=0, top_country_count=0, top_count=0, top_type=2):
        with self.api.lock_leaderbord_deals_client:
            self.api.leaderboard_deals_client = None
        country_id = Country.ID[country]
        self.api.Get_Leader_Board(country_id, user_country_id, from_position, to_position, near_traders_country_count,
                                  near_traders_count, top_country_count, top_count, top_type)
        time.sleep(2)
        start = time.time()
        while 1:
            with self.api.lock_leaderbord_deals_client:
                if self.api.leaderboard_deals_client != None:
                    return self.api.leaderboard_deals_client
            if time.time() - start > 30:
                raise TimeoutError
            time.sleep(.2)

    def get_instruments(self, type):
        # type="crypto"/"forex"/"cfd"
        time.sleep(self.suspend)
        with self.api.lock_instruments:
            self.api.instruments = None
        start = time.time()
        while 1:
            self.api.get_instruments(type)
            time.sleep(1)
            with self.api.lock_instruments:
                if self.api.instruments != None:
                    return self.api.instruments
            if time.time() - start > 10:
                raise TimeoutError

    def instruments_input_to_ACTIVES(self, type):
        instruments = self.get_instruments(type)
        for ins in instruments["instruments"]:
            self.actives[ins["id"]] = ins["active_id"]

    def instruments_input_all_in_ACTIVES(self):
        self.instruments_input_to_ACTIVES("crypto")
        self.instruments_input_to_ACTIVES("forex")
        self.instruments_input_to_ACTIVES("cfd")

    def get_ALL_Binary_ACTIVES_OPCODE(self):
        init_info = self.get_all_init()
        for dirr in (["binary", "turbo"]):
            for i in init_info["result"][dirr]["actives"]:
                self.actives[(init_info["result"][dirr]
                ["actives"][i]["name"]).split(".")[1]] = int(i)

    # _________________________self.iqoptionapi.get_api_option_init_all() wss______________________
    def get_all_init(self):
        while 1:
            with self.api.lock_option_init_all_result:
                self.api.api_option_init_all_result = None
            while 1:
                try:
                    self.api.get_api_option_init_all()
                    break
                except:
                    logging.error('**error** get all option need reconnect')
                    self.connect()
                    time.sleep(5)
            start = time.time()
            while 1:
                if time.time() - start > 30:
                    logging.error('**warning** get all option late 30 sec')
                    break
                with self.api.lock_option_init_all_result:
                    if self.api.api_option_init_all_result:
                        break
                time.sleep(.1)
            with self.api.lock_option_init_all_result:
                if self.api.api_option_init_all_result["isSuccessful"]:
                    return self.api.api_option_init_all_result

    def get_all_init_v2(self):
        with self.api.lock_option_init_all_result:
            self.api.api_option_init_all_result_v2 = None
        self.api.get_api_option_init_all_v2()
        time.sleep(1)
        start_t = time.time()
        while 1:
            with self.api.lock_option_init_all_result:
                if self.api.api_option_init_all_result_v2 != None:
                    return self.api.api_option_init_all_result_v2
            if time.time() - start_t >= 30:
                raise TimeoutError('**warning** get all option v2 late 30 sec')
            time.sleep(.1)

    # ------- chek if binary/digit/cfd/stock... if open or not

    def get_all_open_time(self):

        # for binary option turbo and binary
        OPEN_TIME = nested_dict(3, dict)
        binary_data = self.get_all_init_v2()
        binary_list = ["binary", "turbo"]
        for option in binary_list:
            for actives_id in binary_data[option]["actives"]:
                active = binary_data[option]["actives"][actives_id]
                name = str(active["name"]).split(".")[1]
                if active["enabled"] == True:
                    if active["is_suspended"] == True:
                        OPEN_TIME[option][name]["open"] = False
                    else:
                        OPEN_TIME[option][name]["open"] = True
                else:
                    OPEN_TIME[option][name]["open"] = active["enabled"]

        time.sleep(1)

        # for digital
        digital_data = self.get_digital_underlying_list_data()["underlying"]
        for digital in digital_data:
            name = digital["underlying"]
            schedule = digital["schedule"]
            OPEN_TIME["digital"][name]["open"] = False
            for schedule_time in schedule:
                start = schedule_time["open"]
                end = schedule_time["close"]
                if start < time.time() < end:
                    OPEN_TIME["digital"][name]["open"] = True

        # for OTHER
        # instrument_list = ["cfd", "forex", "crypto"]
        # for instruments_type in instrument_list:
        #     ins_data = self.get_instruments(instruments_type)["instruments"]
        #     for detail in ins_data:
        #         name = detail["name"]
        #         schedule = detail["schedule"]
        #         OPEN_TIME[instruments_type][name]["open"] = False
        #         for schedule_time in schedule:
        #             start = schedule_time["open"]
        #             end = schedule_time["close"]
        #             if start < time.time() < end:
        #                 OPEN_TIME[instruments_type][name]["open"] = True

        return OPEN_TIME

    # --------for binary option detail

    def get_binary_option_detail(self):
        detail = nested_dict(2, dict)
        init_info = self.get_all_init()
        for actives in init_info["result"]["turbo"]["actives"]:
            name = init_info["result"]["turbo"]["actives"][actives]["name"]
            name = name[name.index(".") + 1:len(name)]
            detail[name]["turbo"] = init_info["result"]["turbo"]["actives"][actives]

        for actives in init_info["result"]["binary"]["actives"]:
            name = init_info["result"]["binary"]["actives"][actives]["name"]
            name = name[name.index(".") + 1:len(name)]
            detail[name]["binary"] = init_info["result"]["binary"]["actives"][actives]
        return detail

    def get_all_profit(self):
        all_profit = nested_dict(2, dict)
        init_info = self.get_all_init()
        for actives in init_info["result"]["turbo"]["actives"]:
            name = init_info["result"]["turbo"]["actives"][actives]["name"]
            name = name[name.index(".") + 1:len(name)]
            all_profit[name]["turbo"] = (
                                                100.0 -
                                                init_info["result"]["turbo"]["actives"][actives]["option"]["profit"][
                                                    "commission"]) / 100.0

        for actives in init_info["result"]["binary"]["actives"]:
            name = init_info["result"]["binary"]["actives"][actives]["name"]
            name = name[name.index(".") + 1:len(name)]
            all_profit[name]["binary"] = (
                                                 100.0 -
                                                 init_info["result"]["binary"]["actives"][actives]["option"]["profit"][
                                                     "commission"]) / 100.0
        return all_profit

    # ----------------------------------------

    # ______________________________________self.iqoptionapi.getprofile() https________________________________

    def get_profile_ansyc(self):
        while self.api.profile.msg == None:
            pass
        return self.api.profile.msg

    """def get_profile(self):
        while True:
            try:

                respon = self.iqoptionapi.getprofile().json()
                time.sleep(self.suspend)

                if respon["isSuccessful"] == True:
                    return respon
            except:
                logging.error('**error** get_profile try reconnect')
                self.connect()"""

    def get_currency(self):
        balances_raw = self.get_balances()
        for balance in balances_raw["msg"]:
            if balance["id"] == self.api.global_value.balance_id:
                return balance["currency"]

    def get_balance_id(self):
        return self.api.global_value.balance_id

    """ def get_balance(self):
        self.iqoptionapi.profile.balance = None
        while True:
            try:
                respon = self.get_profile()
                self.iqoptionapi.profile.balance = respon["result"]["balance"]
                break
            except:
                logging.error('**error** get_balance()')

            time.sleep(self.suspend)
        return self.iqoptionapi.profile.balance"""

    def get_balance(self):
        balances_raw = self.get_balances()
        for balance in balances_raw["msg"]:
            if balance["id"] == self.api.global_value.balance_id:
                return balance["amount"]

    def get_balances(self):
        with self.api.lock_balances_raw:
            self.api.balances_raw = None
        self.api.get_balances()
        while 1:
            with self.api.lock_balances_raw:
                if self.api.balances_raw != None:
                    return self.api.balances_raw
            time.sleep(.1)

    def get_balance_mode(self):
        # self.iqoptionapi.profile.balance_type=None
        profile = self.get_profile_ansyc()
        for balance in profile["balances"]:
            if balance["id"] == self.api.global_value.balance_id:
                if balance["type"] == 1:
                    return "REAL"
                elif balance["type"] == 4:
                    return "PRACTICE"

    def reset_practice_balance(self):
        with self.api.lock_training_balance_reset:
            self.api.training_balance_reset_request = None
        self.api.reset_training_balance()
        time.sleep(1)
        while 1:
            with self.api.lock_training_balance_reset:
                if self.api.training_balance_reset_request != None:
                    return self.api.training_balance_reset_request
            time.sleep(.2)

    def position_change_all(self, Main_Name, user_balance_id):
        instrument_type = ["cfd", "forex", "crypto", "digital-option", "turbo-option", "binary-option"]
        for ins in instrument_type:
            self.api.portfolio(Main_Name=Main_Name, name="portfolio.position-changed", instrument_type=ins,
                               user_balance_id=user_balance_id)

    def order_changed_all(self, Main_Name):
        instrument_type = ["cfd", "forex", "crypto", "digital-option", "turbo-option", "binary-option"]
        for ins in instrument_type:
            self.api.portfolio(Main_Name=Main_Name, name="portfolio.order-changed", instrument_type=ins)

    def change_balance(self, Balance_MODE):
        def set_id(b_id):
            if self.api.global_value.balance_id != None:
                self.position_change_all("unsubscribeMessage", self.api.global_value.balance_id)
            self.api.global_value.balance_id = b_id
            self.position_change_all("subscribeMessage", b_id)

        real_id = None
        practice_id = None

        for balance in self.get_profile_ansyc()["balances"]:
            if balance["type"] == 1:
                real_id = balance["id"]
            if balance["type"] == 4:
                practice_id = balance["id"]

        if Balance_MODE == "REAL":
            set_id(real_id)
        elif Balance_MODE == "PRACTICE":
            set_id(practice_id)
        else:
            logging.error("ERROR doesn't have this mode")
            # exit(1)
            return False
        return True

    # ________________________________________________________________________
    # _______________________        CANDLE      _____________________________
    # ________________________self.iqoptionapi.getcandles() wss________________________

    def get_candles(self, ACTIVES, interval, count, endtime):
        self.api.candles.candles_data = None
        while True:
            try:
                self.api.getcandles(
                    self.actives[ACTIVES], interval, count, endtime)
                while self.check_connect and self.api.candles.candles_data == None:
                    pass
                if self.api.candles.candles_data != None:
                    break
            except:
                logging.error('**error** get_candles need reconnect')
                self.connect()
        return self.api.candles.candles_data

    #######################################################
    # ______________________________________________________
    # _____________________REAL TIME CANDLE_________________
    # ______________________________________________________
    #######################################################

    def start_candles_stream(self, ACTIVE, size, maxdict):

        if size == "all":
            for s in self.size:
                self.full_realtime_get_candle(ACTIVE, s, maxdict)
                with self.api.lock_real_time_candles:
                    self.api.real_time_candles_maxdict_table[ACTIVE][s] = maxdict
            self.start_candles_all_size_stream(ACTIVE)
        elif size in self.size:
            with self.api.lock_real_time_candles:
                self.api.real_time_candles_maxdict_table[ACTIVE][size] = maxdict
            self.full_realtime_get_candle(ACTIVE, size, maxdict)
            self.start_candles_one_stream(ACTIVE, size)
        else:
            logging.error('**error** start_candles_stream please input right size')

    def stop_candles_stream(self, ACTIVE, size):
        if size == "all":
            self.stop_candles_all_size_stream(ACTIVE)
        elif size in self.size:
            self.stop_candles_one_stream(ACTIVE, size)
        else:
            logging.error(
                '**error** start_candles_stream please input right size')

    def get_realtime_candles(self, ACTIVE, size):
        if size == "all":
            try:
                with self.api.lock_real_time_candles:
                    return self.api.real_time_candles[ACTIVE]
            except:
                logging.error('**error** get_realtime_candles() size="all" can not get candle')
                return False
        elif size in self.size:
            try:
                with self.api.lock_real_time_candles:
                    return self.api.real_time_candles[ACTIVE][size]
            except:
                logging.error('**error** get_realtime_candles() size=' + str(size) + ' can not get candle')
                return False
        else:
            logging.error('**error** get realtime candles please input right "size"')

    def get_all_realtime_candles(self):
        with self.api.lock_real_time_candles:
            return self.api.real_time_candles

    ################################################
    # ---------REAL TIME CANDLE Subset Function---------
    ################################################
    # ---------------------full dict get_candle-----------------------
    def full_realtime_get_candle(self, ACTIVE, size, maxdict):
        candles = self.get_candles(ACTIVE, size, maxdict, self.api.timesync.server_timestamp)
        for can in candles:
            with self.api.lock_real_time_candles:
                self.api.real_time_candles[str(ACTIVE)][int(size)][can["from"]] = can

    # ------------------------Subscribe ONE SIZE-----------------------
    def start_candles_one_stream(self, ACTIVE, size):
        if (str(ACTIVE + "," + str(size)) in self.subscribe_candle) == False:
            self.subscribe_candle.append((ACTIVE + "," + str(size)))
        start = time.time()
        with self.api.lock_real_time_candles:
            self.api.candle_generated_check[str(ACTIVE)][int(size)] = {}
        while 1:
            if time.time() - start > 20:
                logging.error('**error** start_candles_one_stream late for 20 sec')
                return False
            try:
                with self.api.lock_real_time_candles:
                    if self.api.candle_generated_check[str(ACTIVE)][int(size)] == True:
                        return True
            except:
                pass
            try:
                self.api.subscribe(self.actives[ACTIVE], size)
            except:
                logging.error('**error** start_candles_stream reconnect')
                self.connect()
            time.sleep(1)

    def stop_candles_one_stream(self, ACTIVE, size):
        if ((ACTIVE + "," + str(size)) in self.subscribe_candle) == True:
            self.subscribe_candle.remove(ACTIVE + "," + str(size))
        while True:
            try:
                with self.api.lock_real_time_candles:
                    if self.api.candle_generated_check[str(ACTIVE)][int(size)] == {}:
                        return True
            except:
                pass
            with self.api.lock_real_time_candles:
                self.api.candle_generated_check[str(ACTIVE)][int(size)] = {}
            self.api.unsubscribe(self.actives[ACTIVE], size)
            time.sleep(self.suspend * 10)

    # ------------------------Subscribe ALL SIZE-----------------------

    def start_candles_all_size_stream(self, ACTIVE):
        with self.api.lock_real_time_candles:
            self.api.candle_generated_all_size_check[str(ACTIVE)] = {}
        if (str(ACTIVE) in self.subscribe_candle_all_size) == False:
            self.subscribe_candle_all_size.append(str(ACTIVE))
        start = time.time()
        while 1:
            if time.time() - start > 20:
                logging.error('**error** fail ' + ACTIVE + ' start_candles_all_size_stream late for 10 sec')
                return False
            try:
                with self.api.lock_real_time_candles:
                    if self.api.candle_generated_all_size_check[str(ACTIVE)] == True:
                        return True
            except:
                pass
            try:
                self.api.subscribe_all_size(self.actives[ACTIVE])
            except:
                logging.error('**error** start_candles_all_size_stream reconnect')
                self.connect()
            time.sleep(1)

    def stop_candles_all_size_stream(self, ACTIVE):
        if (str(ACTIVE) in self.subscribe_candle_all_size) == True:
            self.subscribe_candle_all_size.remove(str(ACTIVE))
        while True:
            try:
                if self.api.candle_generated_all_size_check[str(ACTIVE)] == {}:
                    break
            except:
                pass
            self.api.candle_generated_all_size_check[str(ACTIVE)] = {}
            self.api.unsubscribe_all_size(self.actives[ACTIVE])
            time.sleep(self.suspend * 10)

    # ------------------------top_assets_updated---------------------------------------------

    def subscribe_top_assets_updated(self, instrument_type):
        self.api.Subscribe_Top_Assets_Updated(instrument_type)

    def unsubscribe_top_assets_updated(self, instrument_type):
        self.api.Unsubscribe_Top_Assets_Updated(instrument_type)

    def get_top_assets_updated(self, instrument_type):
        with self.api.lock_top_assets_updated:
            if instrument_type in self.api.top_assets_updated_data:
                return self.api.top_assets_updated_data[instrument_type]
            else:
                return None

    # ------------------------commission_________
    # instrument_type: "binary-option"/"turbo-option"/"digital-option"/"crypto"/"forex"/"cfd"
    def subscribe_commission_changed(self, instrument_type):

        self.api.Subscribe_Commission_Changed(instrument_type)

    def unsubscribe_commission_changed(self, instrument_type):
        self.api.Unsubscribe_Commission_Changed(instrument_type)

    def get_commission_change(self, instrument_type):
        with self.api.lock_subscribe_commission:
            return self.api.subscribe_commission_changed_data[instrument_type]

    # -----------------------------------------------

    # -----------------traders_mood----------------------

    def start_mood_stream(self, ACTIVES):
        if ACTIVES not in self.subscribe_mood:
            self.subscribe_mood.append(ACTIVES)

        start = time.time()
        actives = self.actives[ACTIVES]
        while 1:
            if time.time() - start > 60:
                raise TimeoutError('tempo de resposta excedido')
            self.api.subscribe_Traders_mood(actives)
            time.sleep(3)
            try:
                with self.api.lock_mood:
                    self.api.traders_mood[actives]
                break
            except:
                time.sleep(5)

    def stop_mood_stream(self, ACTIVES):
        if ACTIVES in self.subscribe_mood == True:
            del self.subscribe_mood[ACTIVES]
        self.api.unsubscribe_Traders_mood(self.actives[ACTIVES])

    def get_traders_mood(self, ACTIVES):
        # return highter %
        with self.api.lock_mood:
            return self.api.traders_mood[self.actives[ACTIVES]]

    def get_all_traders_mood(self):
        # return highter %
        with self.api.lock_mood:
            return self.api.traders_mood

    ##############################################################################################

    def check_win(self, id_number):
        # 'win':win money 'equal':no win no loose   'loose':loose money
        while 1:
            try:
                listinfodata_dict = self.api.listinfodata.get(id_number)
                if listinfodata_dict["game_state"] == 1:
                    break
            except:
                pass
        self.api.listinfodata.delete(id_number)
        return listinfodata_dict["win"]

    def check_win_v2(self, id_number, polling_time=5):
        while 1:
            check, data = self.get_betinfo(id_number)
            try:
                win = data["result"]["data"][str(id_number)]["win"]
            except:
                pass
            if check and win != "":
                try:
                    return data["result"]["data"][str(id_number)]["profit"] - data["result"]["data"][str(id_number)][
                        "deposit"]
                except:
                    pass
            time.sleep(polling_time)

    def check_win_v3(self, id_number):
        while 1:
            if self.get_async_order(id_number)["option-closed"] != {}:
                break

        return self.get_async_order(id_number)["option-closed"]["msg"]["profit_amount"] - \
               self.get_async_order(id_number)["option-closed"]["msg"]["amount"]

    async def check_win_v4(self, id_number):
        try:
            if self.get_async_order(id_number)["option-closed"] == {}:
                return False, None
        except:
            return False, None
        else:
            return True, self.get_async_order(id_number)["option-closed"]["msg"]["profit_amount"] - \
                   self.get_async_order(id_number)["option-closed"]["msg"]["amount"]

    # -------------------get infomation only for binary option------------------------

    def get_betinfo(self, id_number):

        while 1:
            self.api.game_betinfo.isSuccessful = None
            try:
                self.api.get_betinfo(id_number)
            except:
                logging.error( '**error** def get_betinfo  self.iqoptionapi.get_betinfo reconnect')
                self.connect()
            start = time.time()
            while self.api.game_betinfo.isSuccessful == None:
                if time.time() - start > 10:
                    time.sleep(5)
                    break
                time.sleep(1)

            if self.api.game_betinfo.isSuccessful:
                return self.api.game_betinfo.isSuccessful, self.api.game_betinfo.dict
            else:
                return self.api.game_betinfo.isSuccessful, None



    def get_optioninfo(self, limit):
        with self.api.lock_api_game_getoptions:
            self.api.api_game_getoptions_result = None
        self.api.get_options(limit)
        time.sleep(1)
        while 1:
            with self.api.lock_api_game_getoptions:
                if self.api.api_game_getoptions_result != None:
                    return self.api.api_game_getoptions_result
            time.sleep(.2)

    def get_optioninfo_v2(self, limit):
        with self.api.lock_get_options_v2:
            self.api.get_options_v2_data = None
        self.api.get_options_v2(limit, "binary,turbo")
        time.sleep(1)
        while 1:
            with self.api.lock_get_options_v2:
                if self.api.get_options_v2_data != None:
                    return self.api.get_options_v2_data

    # __________________________BUY__________________________

    # __________________FOR OPTION____________________________

    def buy_multi(self, price, ACTIVES, ACTION, expirations):
        with self.api.lock_buy_multi:
            self.api.buy_multi_option = {}
        if len(price) == len(ACTIVES) == len(ACTION) == len(expirations):
            buy_len = len(price)
            for idx in range(buy_len):
                self.api.buyv3(price[idx], self.actives[ACTIVES[idx]], ACTION[idx], expirations[idx], idx)
            while 1:
                with self.api.lock_buy_multi:
                    if len(self.api.buy_multi_option) >= buy_len:
                        buy_id = []
                        for key in sorted(self.api.buy_multi_option.keys()):
                            try:
                                value = self.api.buy_multi_option[str(key)]
                                buy_id.append(value["id"])
                            except:
                                buy_id.append(None)
                        return buy_id
                time.sleep(.2)
        else:
            logging.error('buy_multi error please input all same len')

    def get_remaning(self, duration):
        for remaning in get_remaning_time(self.api.timesync.server_timestamp):
            if remaning[0] == duration:
                return remaning[1]
        logging.error('get_remaning(self,duration) ERROR duration')
        return "ERROR duration"

    def buy_by_raw_expirations(self, price, active, direction, option, expired):
        with self.api.lock_buy_multi:
            self.api.buy_multi_option = {}
        with self.api.lock_buy:
            self.api.buy_successful = None
        req_id = "buyraw"
        try:
            with self.api.lock_buy_multi:
                self.api.buy_multi_option[req_id]["id"] = None
        except:
            pass
        self.api.buyv3_by_raw_expired(price, self.actives[active], direction, option, expired, request_id=req_id)
        start_t = time.time()
        id = None
        with self.api.lock_buy_multi:
            self.api.result = None
        while 1:
            with self.api.lock_buy_multi:
                if self.api.result != None or id != None:
                    try:
                        if "message" in self.api.buy_multi_option[req_id].keys():
                            logging.error('**warning** buy' + str(self.api.buy_multi_option[req_id]["message"]))
                            return False, self.api.buy_multi_option[req_id]["message"]
                        return self.api.result, self.api.buy_multi_option[req_id]["id"]
                    except:
                        pass
                try:
                    id = self.api.buy_multi_option[req_id]["id"]
                except:
                    pass
                if time.time() - start_t >= 5:
                    logging.error('**warning** buy late 5 sec')
                    return False, 'Timeout response ID Buy'
            time.sleep(.2)

    def buy(self, price, ACTIVES, ACTION, expirations):
        with self.api.lock_buy_multi:
            self.api.buy_multi_option = {}
        with self.api.lock_buy:
            self.api.buy_successful = None
        try:
            with self.api.lock_buy_multi:
                self.api.buy_multi_option["buy"]["id"] = None
        except:
            pass
        self.api.buyv3(price, self.actives[ACTIVES], ACTION, expirations, "buy")
        start_t = time.time()
        id_buy = None
        with self.api.lock_buy_multi:
            self.api.result = None
        while 1:
            with self.api.lock_buy_multi:
                try:
                    if self.api.result or id_buy:
                        if "message" in self.api.buy_multi_option["buy"].keys():
                            return False, self.api.buy_multi_option["buy"]["message"]
                        return self.api.result, self.api.buy_multi_option["buy"]["id"]
                except (KeyError, ValueError):
                    pass
                except Exception as e:
                    logging.error('get-message-result-buy -> {}'.format(e))
                try:
                    id_buy = self.api.buy_multi_option["buy"]["id"]
                except:
                    pass
            if time.time() - start_t >= 5:
                logging.error('**warning** buy late 5 sec')
                return False, 'Timeout response ID Buy'
            time.sleep(.1)

    def sell_option(self, options_ids):
        with self.api.lock_sold_options_respond:
            self.api.sold_options_respond = None
        self.api.sell_option(options_ids)
        time.sleep(.2)
        start = time.time()
        while 1:
            with self.api.lock_sold_options_respond:
                if self.api.sold_options_respond != None:
                    return self.api.sold_options_respond
            if time.time()-start>5:
                logging.error('sell option timeout')
                return False
            time.sleep(.2)

    def get_digital_underlying_list_data(self):
        self.api.underlying_list_data = None
        self.api.get_digital_underlying()
        start_t = time.time()
        while self.api.underlying_list_data == None:
            if time.time() - start_t >= 10:
                logging.error(
                    '**warning** get_digital_underlying_list_data late 10 sec')
                return None
        return self.api.underlying_list_data

    def get_strike_list(self, ACTIVES, duration):
        self.api.strike_list = None
        self.api.get_strike_list(ACTIVES, duration)
        ans = {}
        while self.api.strike_list == None:
            pass
        try:
            for data in self.api.strike_list["msg"]["strike"]:
                temp = {}
                temp["call"] = data["call"]["id"]
                temp["put"] = data["put"]["id"]
                ans[("%.6f" % (float(data["value"]) * 10e-7))] = temp
        except:
            logging.error('**error** get_strike_list read problem...')
            return self.api.strike_list, None
        return self.api.strike_list, ans

    def subscribe_strike_list(self, ACTIVE, expiration_period):
        with self.api.lock_instrument_quote:
            self.api.subscribe_instrument_quites_generated(ACTIVE, expiration_period)

    def unsubscribe_strike_list(self, ACTIVE, expiration_period):
        with self.api.lock_instrument_quote:
            del self.api.instrument_quites_generated_data[ACTIVE]
            self.api.unsubscribe_instrument_quites_generated(ACTIVE, expiration_period)

    def get_instrument_quites_generated_data(self, ACTIVE, duration):
        start = time.time()
        while 1:
            with self.api.lock_instrument_quote:
                if self.api.instrument_quotes_generated_raw_data[ACTIVE][duration * 60] != {}:
                    return self.api.instrument_quotes_generated_raw_data[ACTIVE][duration * 60]
            if time.time() - start > 10:
                raise TimeoutError
            time.sleep(.1)

    def get_realtime_strike_list(self, ACTIVE, duration):
        while 1:
            with self.api.lock_instrument_quote:
                if self.api.instrument_quites_generated_data[ACTIVE][duration * 60]:
                    break
            time.sleep(.1)
        """
        strike_list dict: price:{call:id,put:id}
        """
        ans = {}
        with self.api.lock_instrument_quote:
            now_timestamp = self.api.instrument_quites_generated_timestamp[ACTIVE][duration * 60]

        while ans == {}:
            if self.get_realtime_strike_list_temp_data == {} or now_timestamp != self.get_realtime_strike_list_temp_expiration:
                raw_data, strike_list = self.get_strike_list(ACTIVE, duration)
                self.get_realtime_strike_list_temp_expiration = raw_data["msg"]["expiration"]
                self.get_realtime_strike_list_temp_data = strike_list
            else:
                strike_list = self.get_realtime_strike_list_temp_data
            with self.api.lock_instrument_quote:
                profit = self.api.instrument_quites_generated_data[ACTIVE][duration * 60]
            for price_key in strike_list:
                try:
                    side_data = {}
                    for side_key in strike_list[price_key]:
                        detail_data = {}
                        profit_d = profit[strike_list[price_key][side_key]]
                        detail_data["profit"] = profit_d
                        detail_data["id"] = strike_list[price_key][side_key]
                        side_data[side_key] = detail_data
                    ans[price_key] = side_data
                except:
                    pass
        return ans

    def get_digital_current_profit(self, ACTIVE, duration):
        profit = self.api.instrument_quites_generated_data[ACTIVE][duration * 60]
        for key in profit:
            if key.find("SPT") != -1:
                return profit[key]
        return False

    # thank thiagottjv
    # https://github.com/Lu-Yi-Hsun/iqoptionapi/issues/65#issuecomment-513998357
    def buy_digital_spot(self, active, amount, action, duration):
        # Expiration time need to be formatted like this: YYYYMMDDHHII
        # And need to be on GMT time
        # Type - P or C
        if action == 'put':
            action = 'P'
        elif action == 'call':
            action = 'C'
        else:
            logging.error('buy_digital_spot active error')
            return -1
        # doEURUSD201907191250PT5MPSPT
        timestamp = int(self.api.timesync.server_timestamp)
        if duration == 1:
            exp, _ = get_expiration_time(timestamp, duration)
        else:
            now_date = datetime.fromtimestamp(timestamp) + timedelta(minutes=1, seconds=30)
            while 1:
                if now_date.minute % duration == 0 and time.mktime(now_date.timetuple()) - timestamp > 30:
                    break
                now_date = now_date + timedelta(minutes=1)
            exp = time.mktime(now_date.timetuple())
        dateFormated = str(datetime.utcfromtimestamp(exp).strftime("%Y%m%d%H%M"))
        instrument_id = "do" + active + dateFormated + "PT" + str(duration) + "M" + action + "SPT"
        with self.api.lock_digital_option_placed_id:
            self.api.digital_option_placed_id = None
        self.api.place_digital_option(instrument_id, amount)
        time.sleep(.2)
        while 1:
            with self.api.lock_digital_option_placed_id:
                if self.api.digital_option_placed_id is not None:
                    if isinstance(self.api.digital_option_placed_id, int):
                        return True, self.api.digital_option_placed_id
                    else:
                        return False, self.api.digital_option_placed_id
            time.sleep(.2)

    def get_digital_spot_profit_after_sale(self, position_id):
        def get_instrument_id_to_bid(data, instrument_id):
            for row in data["msg"]["quotes"]:
                if row["symbols"][0] == instrument_id:
                    return row["price"]["bid"]
            return None

        # Author:Lu-Yi-Hsun 2019/11/04
        # email:yihsun1992@gmail.com
        # Source code reference
        # https://github.com/Lu-Yi-Hsun/Decompiler-IQ-Option/blob/master/Source%20Code/5.27.0/sources/com/iqoption/dto/entity/position/Position.java#L564
        while self.get_async_order(position_id)["position-changed"] == {}:
            pass
        # ___________________/*position*/_________________
        position = self.get_async_order(position_id)["position-changed"]["msg"]
        # doEURUSD201911040628PT1MPSPT
        # z mean check if call or not
        if position["instrument_id"].find("MPSPT"):
            z = False
        elif position["instrument_id"].find("MCSPT"):
            z = True
        else:
            logging.error(
                'get_digital_spot_profit_after_sale position error' + str(position["instrument_id"]))

        ACTIVES = position['raw_event']['instrument_underlying']
        amount = max(position['raw_event']["buy_amount"], position['raw_event']["sell_amount"])
        start_duration = position["instrument_id"].find("PT") + 2
        end_duration = start_duration + \
                       position["instrument_id"][start_duration:].find("M")

        duration = int(position["instrument_id"][start_duration:end_duration])
        z2 = False

        getAbsCount = position['raw_event']["count"]
        instrumentStrikeValue = position['raw_event']["instrument_strike_value"] / 1000000.0
        spotLowerInstrumentStrike = position['raw_event']["extra_data"]["lower_instrument_strike"] / 1000000.0
        spotUpperInstrumentStrike = position['raw_event']["extra_data"]["upper_instrument_strike"] / 1000000.0

        aVar = position['raw_event']["extra_data"]["lower_instrument_id"]
        aVar2 = position['raw_event']["extra_data"]["upper_instrument_id"]
        getRate = position['raw_event']["currency_rate"]

        # ___________________/*position*/_________________
        instrument_quites_generated_data = self.get_instrument_quites_generated_data(
            ACTIVES, duration)

        # https://github.com/Lu-Yi-Hsun/Decompiler-IQ-Option/blob/master/Source%20Code/5.5.1/sources/com/iqoption/dto/entity/position/Position.java#L493
        f_tmp = get_instrument_id_to_bid(
            instrument_quites_generated_data, aVar)
        # f is bidprice of lower_instrument_id ,f2 is bidprice of upper_instrument_id
        if f_tmp != None:
            self.get_digital_spot_profit_after_sale_data[position_id]["f"] = f_tmp
            f = f_tmp
        else:
            f = self.get_digital_spot_profit_after_sale_data[position_id]["f"]

        f2_tmp = get_instrument_id_to_bid(
            instrument_quites_generated_data, aVar2)
        if f2_tmp != None:
            self.get_digital_spot_profit_after_sale_data[position_id]["f2"] = f2_tmp
            f2 = f2_tmp
        else:
            f2 = self.get_digital_spot_profit_after_sale_data[position_id]["f2"]

        if (spotLowerInstrumentStrike != instrumentStrikeValue) and f != None and f2 != None:

            if (spotLowerInstrumentStrike > instrumentStrikeValue or instrumentStrikeValue > spotUpperInstrumentStrike):
                if z:
                    instrumentStrikeValue = (spotUpperInstrumentStrike - instrumentStrikeValue) / abs(
                        spotUpperInstrumentStrike - spotLowerInstrumentStrike)
                    f = abs(f2 - f)
                else:
                    instrumentStrikeValue = (instrumentStrikeValue - spotUpperInstrumentStrike) / abs(
                        spotUpperInstrumentStrike - spotLowerInstrumentStrike)
                    f = abs(f2 - f)

            elif z:
                f += ((instrumentStrikeValue - spotLowerInstrumentStrike) /
                      (spotUpperInstrumentStrike - spotLowerInstrumentStrike)) * (f2 - f)
            else:
                instrumentStrikeValue = (spotUpperInstrumentStrike - instrumentStrikeValue) / (
                        spotUpperInstrumentStrike - spotLowerInstrumentStrike)
                f -= f2
            f = f2 + (instrumentStrikeValue * f)

        if z2:
            pass
        if f != None:
            # price=f/getRate
            # https://github.com/Lu-Yi-Hsun/Decompiler-IQ-Option/blob/master/Source%20Code/5.27.0/sources/com/iqoption/dto/entity/position/Position.java#L603
            price = (f / getRate)
            # getAbsCount Reference
            # https://github.com/Lu-Yi-Hsun/Decompiler-IQ-Option/blob/master/Source%20Code/5.27.0/sources/com/iqoption/dto/entity/position/Position.java#L450
            return price * getAbsCount - amount
        else:
            return None

    def buy_digital(self, amount, instrument_id):
        with self.api.lock_digital_option_placed_id:
            self.api.digital_option_placed_id = None
        self.api.place_digital_option(instrument_id, amount)
        time.sleep(1)
        start = time.time()
        while 1:
            with self.api.lock_digital_option_placed_id:
                if self.api.digital_option_placed_id != None:
                    return True, self.api.digital_option_placed_id
            if time.time() - start > 30:
                logging.error('buy_digital loss digital_option_placed_id')
                return False, None
            time.sleep(.2)

    def close_digital_option(self, position_id):
        with self.api.lock_buy_multi:
            self.api.result = None
        while self.get_async_order(position_id)["position-changed"] == {}:
            time.sleep(.2)
        position_changed = self.get_async_order(position_id)["position-changed"]["msg"]
        self.api.close_digital_option(position_changed["external_id"])
        time.sleep(1)
        while 1:
            with self.api.lock_buy_multi:
                if self.api.result != None:
                    return self.api.result

    def check_win_digital(self, buy_order_id, polling_time=1):
        while True:
            data = self.get_digital_position(buy_order_id)
            time.sleep(polling_time)
            if data["msg"]["position"]["status"] == "closed":
                if data["msg"]["position"]["close_reason"] == "default":
                    return data["msg"]["position"]["pnl_realized"]
                elif data["msg"]["position"]["close_reason"] == "expired":
                    return data["msg"]["position"]["pnl_realized"] - data["msg"]["position"]["buy_amount"]

    def check_win_digital_v2(self, buy_order_id):

        while self.get_async_order(buy_order_id)["position-changed"] == {}:
            pass
        order_data = self.get_async_order(buy_order_id)["position-changed"]["msg"]
        if order_data != None:
            if order_data["status"] == "closed":
                if order_data["close_reason"] == "expired":
                    return True, order_data["close_profit"] - order_data["invest"]
                elif order_data["close_reason"] == "default":
                    return True, order_data["pnl_realized"]
            else:
                return False, None
        else:
            return False, None

    async def check_win_digital_v3(self, buy_order_id):
        try:
            order_data = self.get_async_order(buy_order_id)["position-changed"]["msg"]
            if order_data != None:
                if order_data["status"] == "closed":
                    if order_data["close_reason"] == "expired":
                        return True, order_data["close_profit"] - order_data["invest"]
                    elif order_data["close_reason"] == "default":
                        return True, order_data["pnl_realized"]
                else:
                    return False, None
            else:
                return False, None
        except:
            return False, None

    # ----------------------------------------------------------
    # -----------------BUY_for__Forex__&&__stock(cfd)__&&__ctrpto

    def buy_order(self, instrument_type, instrument_id, side, amount, leverage,
                  type, limit_price=None, stop_price=None, stop_lose_kind=None, stop_lose_value=None,
                  take_profit_kind=None, take_profit_value=None, use_trail_stop=False,
                  auto_margin_call=False, use_token_for_commission=False):

        with self.api.lock_buy_order_id:
            self.api.buy_order_id = None
        self.api.buy_order(
            instrument_type=instrument_type, instrument_id=instrument_id,
            side=side, amount=amount, leverage=leverage,
            type=type, limit_price=limit_price, stop_price=stop_price,
            stop_lose_value=stop_lose_value, stop_lose_kind=stop_lose_kind,
            take_profit_value=take_profit_value, take_profit_kind=take_profit_kind,
            use_trail_stop=use_trail_stop, auto_margin_call=auto_margin_call,
            use_token_for_commission=use_token_for_commission
        )
        time.sleep(.2)
        order_id = None
        start = time.time()
        while 1:
            if time.time() - start > 30:
                raise TimeoutError('tempo excedido')
            with self.api.lock_buy_order_id:
                if self.api.buy_order_id != None:
                    order_id = self.api.buy_order_id
                    break
            time.sleep(.2)
        check, data = self.get_order(order_id)
        start = time.time()
        while 1:
            if time.time() - start > 30:
                raise TimeoutError('tempo excedido')
            if data.get("status") == "pending_new":
                check, data = self.get_order(self.api.buy_order_id)
            else:
                break
            time.sleep(1)
        if check:
            if data.get("status") != "rejected":
                return True, order_id
            else:
                return False, data.get("reject_status")
        else:
            return False, None

    def change_auto_margin_call(self, ID_Name, ID, auto_margin_call):
        with self.api.lock_auto_margin_call_changed:
            self.api.auto_margin_call_changed_respond = None
        self.api.change_auto_margin_call(ID_Name, ID, auto_margin_call)
        time.sleep(1)
        while 1:
            with self.api.lock_auto_margin_call_changed:
                if self.api.auto_margin_call_changed_respond != None:
                    if self.api.auto_margin_call_changed_respond["status"] == 2000:
                        return True, self.api.auto_margin_call_changed_respond
                    else:
                        return False, self.api.auto_margin_call_changed_respond
            time.sleep(.2)

    def change_order(self, ID_Name, order_id,
                     stop_lose_kind, stop_lose_value,
                     take_profit_kind, take_profit_value,
                     use_trail_stop, auto_margin_call):
        check = True
        if ID_Name == "position_id":
            check, order_data = self.get_order(order_id)
            position_id = order_data["position_id"]
            ID = position_id
        elif ID_Name == "order_id":
            ID = order_id
        else:
            logging.error('change_order input error ID_Name')

        if check:
            with self.api.lock_tpsl_changed_respond:
                self.api.tpsl_changed_respond = None
            self.api.change_order(ID_Name=ID_Name, ID=ID, stop_lose_kind=stop_lose_kind,
                                  stop_lose_value=stop_lose_value, take_profit_kind=take_profit_kind,
                                  take_profit_value=take_profit_value, use_trail_stop=use_trail_stop)
            time.sleep(.5)
            self.change_auto_margin_call(ID_Name=ID_Name, ID=ID, auto_margin_call=auto_margin_call)
            time.sleep(1)
            while 1:
                with self.api.lock_tpsl_changed_respond:
                    if self.api.tpsl_changed_respond != None:
                        if self.api.tpsl_changed_respond["status"] == 2000:
                            return True, self.api.tpsl_changed_respond["msg"]
                        else:
                            return False, self.api.tpsl_changed_respond
                time.sleep(.2)
        else:
            logging.error('change_order fail to get position_id')
            return False, None

    def get_async_order(self, buy_order_id):
        # name': 'position-changed', 'microserviceName': "portfolio"/"digital-options"
        with self.api.lock_position_change:
            return self.api.order_async[buy_order_id]

    def get_order(self, buy_order_id):
        # self.iqoptionapi.order_data["status"]
        # reject:you can not get this order
        # pending_new:this order is working now
        # filled:this order is ok now
        # new
        with self.api.lock_buy_order_id:
            self.api.order_data = None
        self.api.get_order(buy_order_id)
        time.sleep(1)
        start = time.time()
        while 1:
            if time.time() - start > 10:
                raise TimeoutError('tempo de resposta excedido')
            with self.api.lock_buy_order_id:
                if self.api.order_data != None:
                    if self.api.order_data["status"] == 2000:
                        return True, self.api.order_data.get("msg")
                    else:
                        return False, None
            time.sleep(.1)

    def get_pending(self, instrument_type):
        with self.api.lock_deferred_orders:
            self.api.deferred_orders = None
        self.api.get_pending(instrument_type)
        time.sleep(1)
        start = time.time()
        while 1:
            if time.time() - start > 10:
                raise TimeoutError('tempo de resposta excedido')
            with self.api.lock_deferred_orders:
                if self.api.deferred_orders != None:
                    if self.api.deferred_orders["status"] == 2000:
                        return True, self.api.deferred_orders["msg"]
                    else:
                        return False, None
            time.sleep(.2)

    # this function is heavy
    def get_positions(self, instrument_type, time_limit=0):
        with self.api.lock_positions:
            self.api.positions = None
        self.api.get_positions(instrument_type)
        time.sleep(1)
        start = time.time()
        while 1:
            if time.time() - start > time_limit and time_limit > 0:
                raise TimeoutError('tempo de resposta excedido')
            with self.api.lock_positions:
                if self.api.positions != None:
                    if self.api.positions["status"] == 2000:
                        return True, self.api.positions["msg"]
                    else:
                        return False, None
            time.sleep(.2)

    def get_position(self, buy_order_id):
        with self.api.lock_positions:
            self.api.position = None
        check, order_data = self.get_order(buy_order_id)
        position_id = order_data["position_id"]
        self.api.get_position(position_id)
        time.sleep(1)
        start = time.time()
        while 1:
            if time.time() - start > 10:
                raise TimeoutError('tempo de resposta excedido')
            with self.api.lock_positions:
                if self.api.position != None:
                    if self.api.position["status"] == 2000:
                        return True, self.api.position["msg"]
                    else:
                        return False, None
            time.sleep(.2)

    # this function is heavy

    def get_digital_position_by_position_id(self, position_id, limit_time=0):
        with self.api.lock_positions:
            self.api.position = None
        self.api.get_digital_position(position_id)
        time.sleep(3)
        start = time.time()
        while 1:
            if time.time() - start > 60 and limit_time > 0:
                raise TimeoutError('tempo de resposta excedido')
            with self.api.lock_positions:
                if self.api.position != None:
                    return self.api.position
            time.sleep(.2)

    def get_digital_position(self, order_id, limit_time=0):
        with self.api.lock_positions:
            self.api.position = None
        start = time.time()
        while self.get_async_order(order_id)["position-changed"] == {}:
            if time.time() - start > 60 and limit_time > 0:
                raise TimeoutError('tempo de resposta excedido')
            time.sleep(.2)
        position_id = self.get_async_order(order_id)["position-changed"]["msg"]["external_id"]
        self.api.get_digital_position(position_id)
        time.sleep(1)
        start = time.time()
        while 1:
            if time.time() - start > limit_time and limit_time > 0:
                raise TimeoutError('tempo de resposta excedido')
            with self.api.lock_positions:
                if self.api.position != None:
                    return self.api.position
            time.sleep(.2)

    def get_position_history(self, instrument_type, limit_time=0):
        with self.api.lock_position_history:
            self.api.position_history = None
        self.api.get_position_history(instrument_type)
        time.sleep(1)
        start = time.time()
        while 1:
            if time.time() - start > limit_time and limit_time > 0:
                raise TimeoutError('tempo de resposta excedido')
            with self.api.lock_position_history:
                if self.api.position_history != None:
                    if self.api.position_history["status"] == 2000:
                        return True, self.api.position_history["msg"]
                    else:
                        return False, None
            time.sleep(.2)

    def get_position_history_v2(self, instrument_type, limit, offset, start, end, limit_time=0):
        # instrument_type=crypto forex fx-option multi-option cfd digital-option turbo-option
        with self.api.lock_position_history:
            self.api.position_history_v2 = None
        self.api.get_position_history_v2(instrument_type, limit, offset, start, end)
        time.sleep(1)
        start = time.time()
        while 1:
            if time.time() - start > limit_time and limit_time > 0:
                raise TimeoutError('tempo de resposta excedido')
            with self.api.lock_position_history:
                if self.api.position_history_v2 != None:
                    if self.api.position_history_v2["status"] == 2000:
                        return True, self.api.position_history_v2["msg"]
                    else:
                        return False, None
            time.sleep(.2)

    def get_available_leverages(self, instrument_type, actives="", limit_time=0):
        with self.api.lock_leverage:
            self.api.available_leverages = None
        if actives == "":
            self.api.get_available_leverages(instrument_type, "")
        else:
            self.api.get_available_leverages(instrument_type, self.actives[actives])
        time.sleep(1)
        start = time.time()
        while 1:
            if time.time() - start > limit_time and limit_time > 0:
                raise TimeoutError('tempo de resposta excedido')
            with self.api.lock_leverage:
                if self.api.available_leverages != None:
                    if self.api.available_leverages["status"] == 2000:
                        return True, self.api.available_leverages["msg"]
                    else:
                        return False, None
                time.sleep(.2)

    def cancel_order(self, buy_order_id):
        with self.api.lock_order_canceled:
            self.api.order_canceled = None
        self.api.cancel_order(buy_order_id)
        time.sleep(1)
        while 1:
            with self.api.lock_order_canceled:
                if self.api.order_canceled != None:
                    if self.api.order_canceled["status"] == 2000:
                        return True
                    else:
                        return False
            time.sleep(.2)

    def close_position(self, position_id):
        check, data = self.get_order(position_id)
        if data["position_id"] != None:
            with self.api.lock_close_position_data:
                self.api.close_position_data = None
            self.api.close_position(data["position_id"])
            time.sleep(1)
            while 1:
                with self.api.lock_close_position_data:
                    if self.api.close_position_data != None:
                        if self.api.close_position_data["status"] == 2000:
                            return True
                        else:
                            return False
                time.sleep(.2)
        else:
            return False

    def close_position_v2(self, position_id):
        while self.get_async_order(position_id) == None:
            pass
        position_changed = self.get_async_order(position_id)
        self.api.close_position(position_changed["id"])
        time.sleep(1)
        while 1:
            with self.api.lock_close_position_data:
                if self.api.close_position_data != None:
                    if self.api.close_position_data["status"] == 2000:
                        return True
                    else:
                        return False
            time.sleep(.2)

    def get_overnight_fee(self, instrument_type, active):
        with self.api.lock_overnight_fee:
            self.api.overnight_fee = None
        self.api.get_overnight_fee(instrument_type, self.actives[active])
        time.sleep(1)
        while 1:
            with self.api.lock_overnight_fee:
                if self.api.overnight_fee != None:
                    if self.api.overnight_fee["status"] == 2000:
                        return True, self.api.overnight_fee["msg"]
                    else:
                        return False, None
            time.sleep(.2)

    def get_option_open_by_other_pc(self):
        with self.api.lock_socket_option_opened:
            return self.api.socket_option_opened

    def del_option_open_by_other_pc(self, id):
        with self.api.lock_socket_option_opened:
            del self.api.socket_option_opened[id]

    # -----------------------------------------------------------------

    def opcode_to_name(self, opcode):
        return list(self.actives.keys())[list(self.actives.values()).index(opcode)]

    # name:
    # "live-deal-binary-option-placed"
    # "live-deal-digital-option"
    def subscribe_live_deal(self, name, active, _type, buffersize):
        active_id = self.actives[active]
        self.api.Subscribe_Live_Deal(name, active_id, _type)
        """
        self.iqoptionapi.live_deal_data[name][active][_type]=deque(list(),buffersize) 

        while len(self.iqoptionapi.live_deal_data[name][active][_type])==0:
            self.iqoptionapi.Subscribe_Live_Deal(name,active_id,_type)
            time.sleep(1)
        """

    def unscribe_live_deal(self, name, active, _type):
        active_id = self.actives[active]
        self.api.Unscribe_Live_Deal(name, active_id, _type)
        """

        while len(self.iqoptionapi.live_deal_data[name][active][_type])!=0:
            self.iqoptionapi.Unscribe_Live_Deal(name,active_id,_type)
            del self.iqoptionapi.live_deal_data[name][active][_type]
            time.sleep(1)
        """

    async def get_live_deal(self, name, active, _type):
        with self.api.lock_live_deal_data:
            return self.api.live_deal_data[name][active][_type]

    def pop_live_deal(self, name, active, _type):
        with self.api.lock_live_deal_data:
            return self.api.live_deal_data[name][active][_type].pop()

    async def clear_live_deal(self, name, active, _type, buffersize):
        with self.api.lock_live_deal_data:
            self.api.live_deal_data[name][active][_type] = deque(list(), buffersize)

    def get_user_profile_client(self, user_id):
        with self.api.lock_user_profile_client:
            self.api.user_profile_client = None
        self.api.Get_User_Profile_Client(user_id)
        time.sleep(.2)
        while 1:
            with self.api.lock_user_profile_client:
                if self.api.user_profile_client:
                    return self.api.user_profile_client
            time.sleep(.1)

    def get_user_profile_client_by_name(self, user_name):
        with self.api.lock_user_profile_client:
            self.api.user_profile_client = None
        self.api.Get_User_Profile_Client_By_Name(user_name)
        time.sleep(1)
        while 1:
            with self.api.lock_user_profile_client:
                if self.api.user_profile_client:
                    return self.api.user_profile_client
            time.sleep(.1)

    def request_leaderboard_userinfo_deals_client(self, user_id, country_id):
        with self.api.lock_leaderboard_userinfo:
            self.api.leaderboard_userinfo_deals_client = None
        self.api.Request_Leaderboard_Userinfo_Deals_Client(user_id, country_id)
        while 1:
            try:
                with self.api.lock_leaderboard_userinfo:
                    if self.api.leaderboard_userinfo_deals_client["isSuccessful"] == True:
                        return self.api.leaderboard_userinfo_deals_client
            except:
                pass
            time.sleep(0.2)

    def get_users_availability(self, user_id):
        with self.api.lock_leaderboard_userinfo:
            self.api.users_availability = None
        self.api.Get_Users_Availability(user_id)
        time.sleep(.2)
        while 1:
            with self.api.lock_leaderboard_userinfo:
                if self.api.users_availability != None:
                    return self.api.users_availability
            time.sleep(.2)
