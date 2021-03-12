'''
각각 크기가 m 및 n 인 정렬된 배열 arr1 및 arr2의 중앙값을 반환합니다.
각각의 중앙 값이 아닌 합친 arr1과 arr2을 합친 내용에서의 중앙 값을 의미합니다.
중앙 값이 두 개일 수 있는 경우 두 값의 평균을 반환합니다.
Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Input: nums1 = [0,0], nums2 = [0,0]
Output: 0.00000
Input: nums1 = [], nums2 = [1]
Output: 1.00000
Input: nums1 = [2], nums2 = []
Output: 2.00000

def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) ->
float:

'''


def findMedianSortedArrays(nums1, nums2):
    '''
    파이썬 기본 함수인 len을 통하여 array의 길이를 확인하고,
    list 의 sum 함수를 이용하여 합계를 산출하였습니다.

    각 list 내부의 값을 조회하여 합을 구하므로, 
    시간 복잡도는
    Time complexity  = O(n)
    공간 복잡도는 초기 입력받는 array에 의하여 결정되므로,
    Space complexity = O(n)
    입니다.
    '''
    __avg_num1 = getListAverage(nums1)
    __avg_num2 = getListAverage(nums2)

    if __avg_num1 != None and __avg_num2 != None:
        return (__avg_num1 + __avg_num2) / 2
    elif __avg_num1 != None or __avg_num2 != None:
        if __avg_num1 != None:
            return __avg_num1
        else:
            return __avg_num2

    return 0.0


def getListAverage(targetList):
    __length = len(targetList)
    if __length == 0:
        return None
    __sum_elem = sum(targetList)
    __avg = __sum_elem / __length
    return __avg


def casetest():
    print("case Test")
    print(findMedianSortedArrays(nums1=[1, 3], nums2=[2]))
    print(findMedianSortedArrays(nums1=[1, 2], nums2=[3, 4]))
    print(findMedianSortedArrays(nums1=[0, 0], nums2=[0, 0]))
    print(findMedianSortedArrays(nums1=[], nums2=[1]))
    print(findMedianSortedArrays(nums1=[2], nums2=[]))


if __name__ == '__main__':
    casetest()
