'''
첨부 데이터(problem4.csv)를 변환합니다.
'''

from test_04.vectornizer.vectorizer import Vectorizer


def run_vectorizer():
    print("Vectorizer")

    # !! CSV 파일은 gitignore에 추가하여 별도오 업로드 하지 않았음.
    __csv_file = "./resources/problem4.csv"
    __save_path = "./tokenizer.json"

    mVectorizer = Vectorizer()

    # 생성된 tokenizer 값을 저장
    mVectorizer.fit(__csv_file, __save_path)


    '''
    Generator 로 생성하였으며, 전체 아이템에 따라  train/ valid/eval의 목적으로 나누어 사용할수 있다.
    Pandas 기본함수를 통하여 shuffle 기능을 추가하였다.
    '''
    __generator = mVectorizer.generate(__csv_file, shuffle=True)
    for __data in __generator:
        print(__data)

if __name__ == "__main__":
    run_vectorizer()

