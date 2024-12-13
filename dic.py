n= int(input())
temp=n
x=0
while(temp):
    temp//=10
    x+=1
temp=n
digit=0
result=0
while temp:
    digit=temp%10
    temp//=10
    result+=pow(digit,x)
if result==n :
    print("Armstrong")
else:
    print("Not Armstrong")