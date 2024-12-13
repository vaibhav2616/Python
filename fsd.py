n= int(input())
sum=0
for i in range(n):
    if(n%3==0 or n%5==0):
        sum+=i
print(sum)