class CredentialHelper(object):
    def __init__(self):
        self.key = None

    def check(self, authKey):
        if authKey == self.callAuthKey():
            return True
        else:
            return False

    def callAuthKey(self):
        '''
        서버 혹은 Vendingmachine 내부에서
        인증키 호출

        '''
        __dummy_authkey = "hello vendingmachine"
        return __dummy_authkey
