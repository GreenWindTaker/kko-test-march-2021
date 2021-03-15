from test_03.utils.goodsTable import GoodsTable
from test_03.utils.coinIO import CoinIO
from test_03.helper.credentialHelper import CredentialHelper
from test_03.handler.inputHandler import InputHandler
from test_03.handler.displayHandler import DisplayHandler


class MachineController(object):
    def __init__(self):
        '''
        아이템 관리를 위한 GoodsTable 초기화
        코인 입출력 관리를 위한 CoinIO 초기화
        관리자 인증을 위하 CredentialHelper 호출
        디스플레이 출력을 위한 Display Handler
        유저 입력 Event를 감지하기 위한 Input Handler
        '''
        self.cache = dict()
        self.goodTable = GoodsTable()
        self.coinIo = CoinIO()
        self.credentialHelper = CredentialHelper()
        self.display = DisplayHandler()
        self.inputs = InputHandler()


    def setEventListener(self):
        '''
        InputHandler의 Event Listener로 동작하기 위하여 등록
        '''
        self.inputs.setCallback(listenser=self.eventListener)

    def run(self):
        '''
        Controller 서비스 등록 및 실행
        '''

    def healthCheck(self):
        return True

    def eventListener(self, params):
        __mode = params.get("mode")
        if __mode == "manager":
            return self.managerMode(params)
        elif __mode == "guest":
            return self.guestMode(params)

    def managerMode(self, params):
        '''
        관리자 전용 모드
        [auth] : 관리자 인증 진행 (여기서는 생략)
        [command] : 명령어
            - "coinCollect" : 코인 수거
            - "coinUpdate" : 코인 추가
            - "goodsCollect" : 음료수 재고 수거
            - "goodsUpdate" : 음료수 재고 추가 및 가격변동
        [message] : 관리 message options
        '''
        __auth = params.get('auth')

        if self.credentialHelper.check(__auth) == False:
            return self.display.showMessage("ERROR")

        __command = params.get("command")
        __message = params.get('message')
        if __command == "coinCollect":
            return self.__m_coinCollect(__message)
        if __command == "coinUpdate":
            return self.__m_coinUpdate(__message)
        if __command == "goodsCollect":
            return self.__m_goodsCollect(__message)
        if __command == "goodsUpdate":
            return self.__m_goodsUpdate(__message)

    def __m_coinCollect(self, message):
        for coin, coin_num in message:
            __get_coin_num = self.coinIo.getCoinNums(coin)
            if coin_num > __get_coin_num:
                coin_num = __get_coin_num
            self.coinIo.getCoin(coin, coin_num)
        self.display.showMessage("코인 수거")

    def __m_coinUpdate(self, message):
        for coin, coin_num in message:
            self.coinIo.addCoin(coin, coin_num)
        self.display.showMessage("코인 추가")

    def __m_goodsCollect(self, message):
        for goods_name, goods_num in message:
            __get_goods_num = self.goodTable.getItemNum(goods_name)
            if goods_num > __get_goods_num:
                goods_num = __get_goods_num
            self.goodTable.getItem(goods_name, goods_num)
        self.display.showMessage("아이템 수거")

    def __m_goodsUpdate(self, message):
        for goods_name, goods_num, goods_price in message:
            self.goodTable.addItem(goods_name, goods_num, goods_price)
        self.display.showMessage("아이템 추가")

    def guestMode(self, params):
        '''
        고객 응대
        [action]: 고객 행동패턴
            - "insertCoin" : 코인 삽입
            - "selectGoods" : 음료수 선택
            - "pushRefund" : 구매없이 환불
        '''
        __command = params.get("action")
        __message = params.get('message')

        if __command == "insertCoin":
            return self.__g_insertCoin(__message)
        if __command == "selectGoods":
            return self.__g_selectGoods(__message)
        if __command == "pushRefund":
            return self.__g_pushRefund()

    def __g_insertCoin(self, message):
        '''
        사용자 코인은 한번에 한번씩 입력한다 가정.
        '''
        __coin = message.get("coin")
        # for coin in message:
        self.coinIo.userInsertCoin(__coin)
        __insert_total = self.coinIo.getUserInsertCoinTotal()
        self.display.showMessage("입력금액 " + str(__insert_total))

    def __g_selectGoods(self, message):
        '''
        * 아이템은 한번에 하나의 선택이 가능하며, itemA가 선택된 상황에서 itemB를 선택하면
        itemB에 대하여 구매를 진행합니다.

        아이템 선택버튼 클릭
            - item price > 총 입력 금액 : 부족금액 출력
            - item price == 총 입력 금액 : 아이템 구매
            - item price < 총 입력 금액 : 잔돈 확인후 refund 혹은 구매 불가

        '''
        __select_item = message.get("selected_goods")

        # 재고확인
        __item_status = self.goodTable.getItemStatus(__select_item)
        if __item_status == False:
            self.display.showMessage(str(__select_item) + " 재고가 부족합니다.")
            return

        __item_price = self.goodTable.getItemPrice(__select_item)
        __get_inserted_coin = self.coinIo.getUserInsertCoinTotal()

        if __item_price > __get_inserted_coin:
            __lack_of_money = __item_price - __get_inserted_coin
            self.display.showMessage("금액이 부족합니다. " + str(__lack_of_money) + " 원이 부족합니다.")
            return

        if __item_price == __get_inserted_coin:
            self.display.showMessage("선택하신 제품 " + str(__select_item) + "을/를 구매합니다. ")
            self.goodTable.getItem(__select_item)
            self.coinIo.resetUserCoinCaching()

        if __item_price < __get_inserted_coin:
            __ableToRefund, __refund_coins = self.coinIo.isRefundable(__item_price, __get_inserted_coin)
            if __ableToRefund == False:

                # Vendingmachine 내 잔액이 부족한 경우
                self.display.showMessage("자판기 내 잔액이 부족하여 구매가 불가능 합니다. 죄송합니다.")
                self.coinIo.refund(None, False)
            else:
                __refund_money = __get_inserted_coin - __item_price
                self.display.showMessage("선택하신 제품 " + str(__select_item) + "을/를 구매합니다. ")
                self.display.showMessage("잔액은 " + str(__refund_money) + " 원 입니다.")
                self.coinIo.refund(__refund_coins, True)

    def __g_pushRefund(self):
        self.display.showMessage("환불을 진행합니다.")
        self.coinIo.refund(None, False)
