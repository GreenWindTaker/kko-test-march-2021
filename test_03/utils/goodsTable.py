class GoodsTable(object):
    '''
    Vendingmachine 재고 관리용 Class
    - goodsTable 구성
       -- Unique Key : 아이템 이름을 Unique Key로 보유함 (string)
       -- [stored] : 보유 수량 (int)
       -- [price] : 아이템 가격 (int)
       -- [status] : 판매가능 여부 (string) => 판매가능 : "ON_SALE" / 재고없음 : "OUT_OF_STOCK"

    - 관리자에 의하여 재고를 추가하는 경우
        - addItem : 아이템
    - 아이템을 User가 구매하는 경우 수량을 확인함.
        -- 아이템 재고가 없는 경우 "판매불가" Return
        -- 아이템 재고가 있는 경우는 해당 아이템의 가격을 Return

    - User가 실재로 아이템을 구매하는 경우, 아이템 재고 차감 진행
        -- 재고가 없으면 선택이 불가능함.
    '''

    def __init__(self):
        self.goodsTable = dict()
        self.base_err_msg = "ERR"

    def addItem(self, goods_name, goods_cnt, goods_price=None):
        '''
        아이템 이름과 정보를 goodTable로 추가함.
        - 아이템 이름과 재고추가, 그리고 가격 변동에 대한 처리
        - ItemSTatus 확인 function을 호출하여 반영.
        '''
        if goods_name not in self.goodsTable:
            self.goodsTable[goods_name] = dict()
            self.goodsTable[goods_name]["stored"] = 0
        self.goodsTable[goods_name]["price"] = goods_price

        if goods_price != None:
            self.goodsTable[goods_name]["stored"] += goods_cnt

        self.setItemStatus(goods_name)

    def setItemStatus(self, goods_name):
        '''
        아이템의 판매가능 여부를 확인
        '''
        if self.goodsTable[goods_name]["stored"] > 0:
            self.goodsTable[goods_name]["status"] = "ON_SALE"
        else:
            self.goodsTable[goods_name]["status"] = "OUT_OF_STOCK"

    def getItemStatus(self, goods_name):
        '''
        Main Controller에서 아이템 재고 확인을 필요로 하는경우
        정보를 Return
        '''
        if goods_name in self.goodsTable:
            __get_status = self.goodsTable[goods_name].get('status', self.base_err_msg)
            return __get_status
        return self.base_err_msg

    def getItemNum(self, goods_name):
        return self.goodsTable[goods_name]["stored"]

    def getItemPrice(self, goods_name):
        return self.goodsTable[goods_name]["price"]

    def getItem(self, goods_name, goods_num=1):
        '''
        User에 의하여 해당 item을 선택하는 경우, 자동으로 차감하며
        재고 정보에 대한 Update를 진행
        '''
        if goods_name in self.goodsTable:
            __get_stored = self.goodsTable[goods_name].get("stored")
            if __get_stored > 0:
                self.goodsTable[goods_name]["stored"] += -1 * goods_num

                self.setItemStatus(goods_name)
                return True
        return False

