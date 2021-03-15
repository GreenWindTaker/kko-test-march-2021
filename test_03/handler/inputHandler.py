class InputHandler(object):
    def __init__(self):
        self.display = None

    def setCallback(self, **kwargs):
        '''
        Input Handler로부터 발생하는 Event를 감지하여 리턴.
        '''
        pass

    def coinInput(self, coin):
        '''
        VendingMachine에 코인이 입력받는 event를 감지
        '''
        return coin

    def goodsButton(self, goods_name):
        '''
        VendingMachine에서 음료수를 선택하는 버튼이벤트를 감지한다 가정.
        '''
        print("Selected Item Name : " + str(goods_name))
        return goods_name
