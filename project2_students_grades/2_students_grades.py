#2-3
# PythonLecture이라는 class 정의
class PythonLecture:
    # 생성자 함수 정의
    def __init__(self, score1, score2, score3, absent):
        # 사용자의 입력값을 self.입력값의 형태로 지정
        self.score1 = score1
        self.score2 = score2
        self.score3 = score3
        self.absent = absent
    # 3개의 시험의 평균 점수를 산출하는 함수 정의
    def average_score(self):
        average = (self.score1 + self.score2 + self.score3) / 3
        return average
    # 3개의 점수를 20,30,50% 가중치로 평균을 산출하는 함수 정의
    def weigh_average(self):
        average = 0.2 * self.score1 + 0.3 * self.score2 + 0.5 * self.score3
        return average
    # 결석 횟수가 5회 이상이면 성적과 상관없이 F학점을 산출하고,
    # weigh_average 함수의 반환값을 최종성적으로 받아 학점으로 산출하는 함수 정의
    def grade(self, avg_score):
        # 결석 횟수가 5회 이상일 때
        if self.absent >= 5:
            return 'F'

        # avg_score이 각 구간에 속할 때 반환되는 학점
        if 100 >= avg_score >= 90:
            return 'A'
        elif 80 <= avg_score < 90:
            return 'B'
        elif 70 <= avg_score < 80:
            return 'C'
        elif 60 <= avg_score < 70:
            return 'D'
        elif avg_score < 60:
            return 'F'

print('='*30)
print('Python Leture Score Calculator')
print('='*30)

# 구현할 세명의 학생들을 리스트로 배열하도록 설정
Students = []

# 세 명의 학생 정보를 수식하기 위한 반복문
for i in range (3) :
    # input 함수를 출력할 때 같이 출력할 구문 설정
    input_string = "Student {} > ".format(i+1)
    # split 함수를 이용해 ' '를 기준으로 입력값을 구분하도록 설정
    score1, score2, score3, absent = input(input_string).split(' ')
    # int를 사용해 각 입력값을 정수로 받도록 설정
    score1, score2, score3, absent = int(score1), int(score2), int(score3), int(absent)
    # 리스트에 학생을 추가하는 함수 구현.
    Students.append( PythonLecture(score1, score2, score3, absent) )

print('='*10,'Result','='*10)
print('Num  Score  Grade ')

# 세 학생의 숫자, 점수, 학점을 출력할 반복문
for i in range (3) :
    # class의 weigh_average 함수로 가중치를 적용한 평균을 구하는 작업, 소수점 있는 숫자로 반환.
    avg_score = float( Students[i].weigh_average() )
    # class의 grade 함수로 avg_score일 때의 학점을 구하는 작업
    grade = Students[i].grade( avg_score )
    # 학생 번호, 가중치 적용한 평균, 학점 출력
    print(' %d   %2.2f    %s' % (i+1, avg_score, grade ) )