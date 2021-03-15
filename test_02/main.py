'''

def matrixBlockSum(self, matrix: List[List[int]], K: int) ->
List[List[int]]:
'''


def matrixBlockSum(mat, K):
    '''
    파이썬 기본 함수인 len을 통하여 array의  row, col 길이를 확인하고,
    정해진 규칙에 의하여 r 및 c 의 범위를 설정하였습니다.

    이후 각 선택된 2d list의 합을 구하며,
    이를 return list로 산재하므로,

    시간 복잡도는
    Time complexity  = O(n)
    공간 복잡도는 초기 입력받는 array에 의하여 결정되므로,
    Space complexity = O(n)
    입니다.
    '''
    _row_len = len(mat)
    _col_len = len(mat[0])

    __ret_matrix = list()


    for i in range(0, _row_len):
        __gen_col_list = list()
        for j in range(0, _col_len):
            _r_start = i - K
            if _r_start < 0:
                _r_start = 0

            _r_end = i + K + 1
            if _r_start > _row_len:
                _r_start = _row_len

            _c_start = j - K
            if _c_start < 0:
                _c_start = 0

            _c_end = j + K + 1
            if _c_end > _col_len:
                _c_end = _col_len

            __val = twoDimensionListSum(mat,  _r_start, _r_end, _c_start, _c_end)

            __gen_col_list.append(__val)
        __ret_matrix.append(__gen_col_list)

    return __ret_matrix

def twoDimensionListSum(mat, _r_start, _r_end, _c_start, _c_end):
    __sum_val = 0
    for row in mat[_r_start:_r_end]:
        __cache_col = row[_c_start:_c_end]
        __cache_sum = sum(__cache_col)
        __sum_val += __cache_sum
    return __sum_val


def casetest():
    print("case Test")

    print(matrixBlockSum(mat=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], K=1))
    print(matrixBlockSum(mat=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], K=2))


if __name__ == '__main__':
    casetest()
