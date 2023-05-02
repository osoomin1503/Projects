#2-1

# PythonLecture이라는 class 정의
#class PythonLecture:

    # 생성자 함수 정의
    def __init__(self, score1, score2, score3, absent):
        # 사용자의 입력값을 self.입력값의 형태로 지정
        # 1차 시험 점수
        self.score1 = score1
        # 2차 시험 점수
        self.score2 = score2
        # 3차 시험 점수
        self.score3 = score3
        # 결석 횟수
        self.absent = absent

    # 3개의 시험의 평균 점수를 산출하는 함수 정의
    def average_score(self):
        average = (self.score1 + self.score2 + self.score3)/3
        # 3개의 숫자를 더하고 3으로 나눈 average 값을 반환
        return average

    # 3개의 점수를 20,30,50% 가중치로 평균을 산출하는 함수 정의
    def weigh_average(self):
        average = 0.2*self.score1 + 0.3*self.score2 + 0.5*self.score3
        # 각 점수에 가중치를 부여해 구한 average 값을 반환
        return average

    # 결석 횟수가 5회 이상이면 성적과 상관없이 F학점을 산출하는 함수 정의
    def grade(self):
        if self.absent >= 5 :
            return 'F'


#2-2.
# PythonLecture이라는 class 정의
class PythonLecture:

    # 생성자 함수 정의
    def __init__(self, score1, score2, score3, absent):
        # 사용자의 입력값을 self.입력값의 형태로 지정
        # 1차 시험 점수
        self.score1 = score1
        # 2차 시험 점수
        self.score2 = score2
        # 3차 시험 점수
        self.score3 = score3
        # 결석 횟수
        self.absent = absent

    # 3개의 시험의 평균 점수를 산출하는 함수 정의
    def average_score(self):
        average = (self.score1 + self.score2 + self.score3)/3
        # 3개의 숫자를 더하고 3으로 나눈 average 값을 반환
        return average

    # 3개의 점수를 20,30,50% 가중치로 평균을 산출하는 함수 정의
    def weigh_average(self):
        average = 0.2*self.score1 + 0.3*self.score2 + 0.5*self.score3
        # 각 점수에 가중치를 부여해 구한 average 값을 반환
        return average

    # 결석 횟수가 5회 이상이면 성적과 상관없이 F학점을 산출하고,
    # weigh_average 함수의 반환값을 최종성적으로 받아 학점으로 산출하는 함수 정의
    def grade(self, avg_score):
        # 결석 횟수가 5회 이상일 때
        if self.absent >= 5 :
            return 'F'

        # avg_score이 각 구간에 속할 때 반환되는 학점
        if 100 >= avg_score >= 90 :
            return 'A'
        elif 80 <= avg_score < 90 :
            return 'B'
        elif 70 <= avg_score < 80 :
            return 'C'
        elif 60 <= avg_score < 70 :
            return 'D'
        elif avg_score < 60 :
            return 'F'