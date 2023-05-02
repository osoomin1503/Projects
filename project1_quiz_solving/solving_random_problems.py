#1-1
import random #난수발생모듈실행

n=1 #n:문제번호, 문제는 1번부터 시작하므로 n=1로 둠.

while True: #문장을 반복해서 사용해야하므로 while문 사용.
    num1 = random.randint(10, 99) #num1: 첫번째 숫자 -10과 99까지 그 사이의 랜덤한 정수로 설정
    num2 = random.randint(10, 99) #num2: 두번째 숫자 -10과 99까지 그 사이의 랜덤한 정수로 설정
    exam = '문제{}: {}+{}?'.format(n,num1, num2) #exam: 문제표현형식. 포멧함수로 {}에 ()의 원소들이 순서대로 나타나도록 설정
    result = int(input(exam)) #result: user가 입력한 값. user가 exam에 대한 답을 입력하고 컴퓨터가 정수로 인식할 수 있도록 설정.

    if num1+num2==result:
        print('정답입니다!') #컴퓨터가 계산한 값과 user가 입력한 값이 같으면 다음 실행문이 반환
    else:
        print('틀렸습니다!') #컴퓨터가 계산한 값과 user가 입력한 값이 다르면 다음 실행문이 반환

    n+=1
    if n>5:
        break #문제 갯수가 5개보다 많아지면 while문에서 빠져나오도록 설정.


#1-2
import random #난수발생모듈실행

n=1 #n:문제번호, 문제는 1번부터 시작하므로 n=1로 둠.

while True: #문장을 반복해서 사용해야하므로 while문 사용.
    num1 = random.randint(10, 99) #num1: 첫번째 숫자 -10과 99까지 그 사이의 랜덤한 정수로 설정
    num2 = random.randint(10, 99) #num2: 두번째 숫자 -10과 99까지 그 사이의 랜덤한 정수로 설정
    choice = random.randint(1,3) #choice: 계산방법선택 -덧셈, 뺄셈, 곱셈을 1,2,3의 경우로 바꾸어 선택하도록 설정

    if choice == 1:
        exam = '문제{}: {}+{}?'.format(n, num1, num2) #exam: 문제표현형식. 포멧함수로 {}에 ()의 원소들이 순서대로 나타나도록 설정(덧셈)
        answer = num1+num2 #answer: 컴퓨터가 계산한 값(덧셈)

    elif choice == 2:
        exam = '문제{}: {}-{}?'.format(n, num1, num2) #exam: 문제표현형식. 포멧함수로 {}에 ()의 원소들이 순서대로 나타나도록 설정(뺄셈)
        answer = num1-num2 #answer: 컴퓨터가 계산한 값(뺄셈)

    else: #choice==3일 때
        exam = '문제{}: {}*{}?'.format(n,num1, num2) #exam: 문제표현형식. 포멧함수로 {}에 ()의 원소들이 순서대로 나타나도록 설정(곱셈)
        answer = num1*num2 #answer: 컴퓨터가 계산한 값(곱셈)

    result = int(input(exam)) #result: user가 입력한 값. user가 exam에 대한 답을 입력하고 컴퓨터가 정수로 인식할 수 있도록 설정.

    if answer==result:
        print('정답입니다!') #컴퓨터가 계산한 값과 user가 입력한 값이 같으면 다음 실행문이 반환
    else:
        print('틀렸습니다!') #컴퓨터가 계산한 값과 user가 입력한 값이 다르면 다음 실행문이 반환

    n+=1
    if n>5:
        break #문제 갯수가 5개보다 많아지면 while문에서 빠져나오도록 설정.

#1-3
import random #난수발생모듈실행
import time #시간과 관련된 모듈 실행

n=1 #n:문제번호, 문제는 1번부터 시작하므로 n=1로 둠.
right = 0 #right: 맞은 문제 갯수, 초기값은 0으로 설정.

while True:
    num1 = random.randint(10, 99) #num1: 첫번째 숫자 -10과 99까지 그 사이의 랜덤한 정수로 설정
    num2 = random.randint(10, 99) #num2: 두번째 숫자 -10과 99까지 그 사이의 랜덤한 정수로 설정
    choice = random.randint(1,3) #choice: 계산방법선택 -덧셈, 뺄셈, 곱셈을 1,2,3의 경우로 바꾸어 선택하도록 설정

    start = time.time() #start: 문제를 풀기 시작한 현재시간을 실수형태로 설정.
    if choice == 1:
        exam = '문제{}: {}+{}?'.format(n, num1, num2) #exam: 문제표현형식. 포멧함수로 {}에 ()의 원소들이 순서대로 나타나도록 설정(덧셈)
        answer = num1+num2 #answer: 컴퓨터가 계산한 값(덧셈)
    elif choice == 2:
        exam = '문제{}: {}-{}?'.format(n, num1, num2) #exam: 문제표현형식. 포멧함수로 {}에 ()의 원소들이 순서대로 나타나도록 설정(뺄셈)
        answer = num1-num2 #answer: 컴퓨터가 계산한 값(뺄셈)
    else: #choice==3일 때
        exam = '문제{}: {}*{}?'.format(n,num1, num2) #exam: 문제표현형식. 포멧함수로 {}에 ()의 원소들이 순서대로 나타나도록 설정(곱셈)
        answer = num1*num2 #answer: 컴퓨터가 계산한 값(곱셈)

    result = int(input(exam)) #result: user가 입력한 값. user가 exam에 대한 답을 입력하고 컴퓨터가 정수로 인식할 수 있도록 설정.
    end = time.time() #end: 문제를 다 푼 현재시간을 실수형태로 설정.

    if answer==result: #컴퓨터가 계산한 값과 user가 입력한 값이 같을 때
        if end - start > 5 : #다 푼 시간에서 풀기 시작한 시간을 뺐을 때 5초가 초과됐을 때
            print('답을 맞췄으나 시간이 초과되었습니다.') #5초가 지나면 다음 실행문 반환, 하지만 맞은 문제 개수에서는 제외
        else:
            print('시간 내에 맞췄습니다.') #5초 내에 맞춘다면 다음 실행문 반환
            right += 1 #맞은 문제 갯수에서는 +1.
    else:
        print('틀렸습니다!') #컴퓨터가 계산한 값과 user가 입력한 값이 다를 때

    n+=1
    if n>5:
        break #문제 갯수가 5개보다 많아지면 while문에서 빠져나오도록 설정.

print('정답을 맞춘 갯수 : {}/5'.format(right)) #포멧함수로 {}에 ()의 원소인 right가 나타나고 마지막줄에 print되도록 설정.
