# +
print('\033[1;33;44mWarning: Do NOT say Prof.JakeZhao is getting fat. He will fail you!!!\033[0m')

def hw1(year=2020):
       
    print('''      
# Q1.Find all primes inside 10000
upper = int(input("Please input an upper bound for us to search primes inside: "))

for num in range(1,upper + 1):
    for i in range(2,num):
        if (num % i) == 0:
            break
    else:
        print(num)   
        
# Q2.Convert binomial number to decimal
b_num = input('Input a binomial number:')
d_num = 0

kk = len(b_num)

for ii in range(0,kk):
    if int(b_num[ii]) > 1:
        d_num = 'Wrong!'
        break
    else:
        d_num = d_num + 2**(kk-ii-1) * int(b_num[ii])
        
print(d_num)                
    ''')
    
    
def hw2(year=2020):
    
    print('Cake Eating Homework')
    
    print('''
    See the HW2.ipynb inside your package
        
    ''')
    
def hw3(year=2020):
    print('Huggett homework')
    print('See HW3.ipynb in package.')
    
def hw4(year=2020):
    print('Simulation homework')
    print('See HW4.ipynb in package.')
