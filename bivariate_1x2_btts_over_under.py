
import numpy as np

# this is useful for input handling, to get a non-negative float value

def get_pos():
    while True:
        x_s = input('(?) ')
        try:
            x = float(x_s)
            if x < 0 :
                print('value must be non-negative')
                continue
            return x
        except:
            print('bad input')

# this is the main function, a bivariate Poisson distribution
# muH = home mean, muA = away mean, cov = covariance
# returns three lists (1) 1x2 winning probabilities, (2) home/away/btts scoring probabilities
# and over/equal/under the "line" probabilities

def biv(muH, muA, cov, line, mg=31):

# three means for three Poisson distributions
    lam = [muH - cov, muA - cov, cov]

# getting three Poisson distributions ready in a memory efficient way
    p = np.empty((3,mg))
    for i in range(3):
        p[i, 0] = np.exp(-lam[i])
    for i in range(1, mg):
        for j in range(3):
            p[j][i] = p[j][i-1] * lam[j] / i

# m is a square matrix where m[i,j] = probability final score is i,j for home,away
    m = np.zeros((mg, mg))
    for k in range(mg):
        for i in range(mg-k):
            for j in range(mg-k):
                m[i+k, j+k] += p[0][i] * p[1][j] * p[2][k];

# always good to re-normalize to ensure coherence
    m /= m.sum()

# now getting output lists ready

# home/draw/away
    prob = [0.0, 0.0, 0.0]

# home scores/away scores/both score
    btts = [0.0, 0.0, 0.0]

# over/equal/under the line
    over = [0.0, 0.0, 0.0]

# we search through our matrix for conditions relating to lists above
    for i in range(mg):
        for j in range(mg):
            if i >  j : prob[0] += m[i,j]
            if i == j : prob[1] += m[i,j]
            if i <  j : prob[2] += m[i,j]
            if i >  0 : btts[0] += m[i,j]
            if j >  0 : btts[1] += m[i,j]
            if i > 0 and j > 0 : btts[2] += m[i,j]
            if i + j >  line : over[0] += m[i,j]
            if i + j == line : over[1] += m[i,j]
            if i + j <  line : over[2] += m[i,j]

# returns the three lists (each has three members)
    return prob, btts, over

def odds(prob, vig):
    return [round(1/((1+vig)*x),2) for x in prob]



print('\nBivariate Poisson for Soccer 1x2, btts and over/under\n\nhome mean: ')

muH = get_pos()

print('\naway mean: ')

muA = get_pos()

print('\ncovariance: ')

cov = get_pos()

# constraint: 0 <= covariance <= minimum of the two means

while cov < 0 or cov > min(muH, muA):
    print('0 <= cov <=', min(muH, muA))
    cov = get_pos()

print('\nenter the line for over/under: ')

line = get_pos()

prob, btts, over = biv(muH, muA, cov, line)

print('\nhome wins:',prob[0])
print('draw:',prob[1])
print('away wins:',prob[2],'\n')

print('home scores:',btts[0])
print('away scores:',btts[1])
print('both score: ',btts[2],'\n')

print('over',line,':',over[0])
print('equal',line,':',over[1])
print('under',line,':',over[2],'\n')

print('Apply a uniform overround')

get = input('(?) ')

if get=='y' :
    print('\nenter overround (%)')
    vig = get_pos()
    vig/=100
    oprob = odds(prob, vig)
    obtts = odds(btts, vig)
    oover = odds(over, vig)

    print('\nhome wins:',oprob[0])
    print('draw:',oprob[1])
    print('away wins:',oprob[2],'\n')

    print('home scores:',obtts[0])
    print('away scores:',obtts[1])
    print('both score: ',obtts[2],'\n')

    print('over',line,':',oover[0])
    print('equal',line,':',oover[1])
    print('under',line,':',oover[2],'\n')

