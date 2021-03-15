class DisplayHandler(object):
    def __init__(self):
        self.display = None

    def displayInit(self):
        '''
        VendingMachine에 Display가 있다 가정하고 진행.
        -- 디스플레이 초기화
        :return:
        '''
        pass

    def showMessage(self, message):
        '''
        여기서는 print를 통해서 Display 한다 가정하여 진행.
        '''
        print(message)
