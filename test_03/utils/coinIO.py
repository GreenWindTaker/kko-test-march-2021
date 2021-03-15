class CoinIO(object):
    '''
    Coin 입출력 관리용 Class

    - coinTable 구성
       -- Unique Key : [500, 100, 50, 10] 원 의 integer Unique Key값을 보유
       -- [stored] : 보유 Coin 수량 (int)

    - userCoinCaching
       -- 사용자가 입력한 Coin값을 Caching.
       -- Unique key : [500, 100, 50, 10, 'total'] 코인값 및 총합에 대한 정보 저장
       -- 구매없이 Refund하는 경우, 입력한 동전만 반환진행.
          ---> 100원 5개 Insert, 500원 1개 return을 방지하기 위하여.

    - 관리자 혹은 사용자에 의하여 코인을 추가하는 경우
        -- addCoin : (관리자&사용자) Vending machine 내 해당 Coin 수량 증가
        -- userInsertCoin : (사용자) 유저가 입력한 Coin값 확인

    - 아이템을 User가 구매하는 경우 현재 코인 수량 확인.
        -- 실제로 잔돈여부에 따른 환불가능 여부 체크

    - 최종 Refund가 진행되는 경우, 구매 및 환불 가능여부에 따라 동전 환불 진행.
        -- 환불하는 Coin 만큼 차감 진행
        -- 환불금액 최종확인 이후 User 가 입력 coin cache를 초기화

    '''

    def __init__(self):
        self.coinTable = dict()
        self.coinKeys = [500, 100, 50, 10]
        self.userCoinCaching = dict()
        self.resetUserCoinCaching()

    def resetUserCoinCaching(self):
        self.userCoinCaching = dict()
        self.userCoinCaching['total'] = 0

    def addCoin(self, coin, num_of_coins=1):
        if coin not in self.coinTable:
            self.coinTable[coin] = dict()
            self.coinTable[coin]['stored'] = 0
        self.coinTable[coin]['stored'] += num_of_coins

    def userInsertCoin(self, coin, num_of_coins=1):
        '''
        User가 입력하는 Coin 정보에 대한 cache 누적 진행.
        '''
        if coin not in self.userCoinCaching:
            self.userCoinCaching[coin] = dict()
            self.userCoinCaching[coin]['stored'] = 0
        self.userCoinCaching[coin]['stored'] += num_of_coins

        self.userCoinCaching['total'] += (coin * num_of_coins)

        ## Vending Machine 보유코인도 함께 증가
        self.addCoin(coin, num_of_coins)

    def getUserInsertCoinTotal(self):
        return self.userCoinCaching['total']

    def getCoinNums(self, coin):
        if coin in self.coinTable:
            return self.coinTable[coin]['stored']
        return None

    def getCoin(self, coin, num_of_coins):
        '''
        Coin Table에서 특정 coin을 해당 수량만큼 차감 진행
        '''
        self.coinTable[coin]['stored'] += -1 * (num_of_coins)

    # def getLackOfMoney(self, price):
    #     '''
    #     User가 가격보다 금액을 미지급한 상태인 경우
    #     남은 금액에 대한 정보를 제공
    #
    #     '''
    #     lack_of_money = price - self.userCoinCaching['total']
    #     if lack_of_money >= 0:
    #         return lack_of_money

    def isRefundable(self, price, get_money):
        '''
        User가 구매를 진행할 경우에 대비하여
        코인에 대한 환불 가능여부 체크 및 가능한 경우 Coin 정보를 제공
        ableToRefund: 환불 가능여부  (가능 : True, 뿔가능 :False) --> Vending Machine내 잔돈 재고 부족시에 False
        refund_coin : 환불이 가능할시, Coin 정보 제공 (Hashmap)
        '''
        ableToRefund = True
        __rest = get_money - price

        refund_coin = dict()
        for coin_key in self.coinKeys:
            if __rest != 0:
                __stored_coin_key = self.getCoinNums(coin_key)
                __num_of_target_coin = __rest // coin_key

                if __stored_coin_key >= __num_of_target_coin:
                    __rest = __rest - (coin_key * __num_of_target_coin)
                    refund_coin[coin_key] = __num_of_target_coin
                else:
                    __rest = __rest - (coin_key * __stored_coin_key)
                    refund_coin[coin_key] = __stored_coin_key

        if __rest != 0:
            ableToRefund = False
            return ableToRefund, None
        else:
            return ableToRefund, refund_coin

    def refund(self, refund_coin, isBuying=True):
        '''
        User가 구매하는 경우
            -- isBuying (구매여부 확인) == True
            -- isRefundable에서 생성된 Refund_coin을 받아서 환불 진행
            -- CoinTable에서 해당 코인만큼 차감 진행

        만일 User가 구매없는 경우, 혹은 Vening Machine 내 잔돈이 없어서 구매가 불가능한 경우
            -- isBuying (구매여부 확인 ) == False

        '''
        refunding_coin = None
        if isBuying == False:
            '''
            구매없음, userCoinCaching 의 코인만큼 Refund
            '''
            refunding_coin = dict()
            for coin_key in self.coinKeys:
                __get_num_of_coins = self.userCoinCaching[coin_key].get('stored')
                refunding_coin[coin_key] = __get_num_of_coins
                # 해당 코인만큼 coinTable에서 감소 진행
                self.getCoin(coin_key, __get_num_of_coins)

        else:
            '''
            구매진행
            '''
            refunding_coin = refund_coin
            for coin_key in refund_coin:
                _get_num_of_coins = refund_coin.get(coin_key)
                self.getCoin(coin_key, _get_num_of_coins)
        # 환불 진행함과 동시에 cache 되어 있는 User coin 정보 초기화
        self.resetUserCoinCaching()
        return refunding_coin
