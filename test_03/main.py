'''
자판기 어플리케이션
- 10원, 50원, 100원, 500원 동전을 받습니다.
- 콜라(650원), 사이다(550원), 환타(450원) 음료를 선택할 수 있습니다.
- 사용자가 아무것도 선택하지 않고 환불할 수 있습니다.
- 음료 선택 시 음료와 잔돈을 반환합니다.
- 음료의 재고가 부족한 경우, 사용자에게 재고 부족을 알려야 합니다.
- 금액이 모자란 경우에는 얼마만큼의 금액이 부족한지를 알려야 합니다.
- 관리자는 자판기에 새 음료를 추가할 수 있습니다.
'''


def runVendingMachine():
    from test_03.controller.machineController import MachineController

    # 초기화
    mMachineController = MachineController()
    mMachineController.setEventListener()

    # 실행
    mMachineController.run()


if __name__ == "__main__":
    runVendingMachine()
