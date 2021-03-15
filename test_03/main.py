'''
자판기 어플리케이션
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
