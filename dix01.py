
import numpy as np

max_goals = 31

def dixon(muH, muA, rho, mg=max_goals):
    h = np.empty(mg)
    a = np.empty(mg)
    h[0] = a[0] = 1.0
    for i in range(1, mg):
        h[i] = h[i-1] * muH / i
        a[i] = a[i-1] * muA / i
    kh = np.exp(-muH)
    ka = np.exp(-muA)
    h *= kh
    a *= ka
    m = np.outer(h,a)
    m[0,0] *= (1 - rho * muH * muA)
    m[0,1] *= (1 + rho * muH)
    m[1,0] *= (1 + rho * muA)
    m[1,1] *= (1 - rho)
    return m

def hda(m) :
    prob = [0.0, 0.0, 0.0]
    prob[0] = np.tril(m,-1).sum()
    prob[1] = np.trace(m)
    prob[2] = np.triu(m, 1).sum()
    return prob

def score(m) :
    prob = [0.0, 0.0, 0.0]
    x = m[0, :].sum()
    y = m[:, 0].sum()
    prob[0] = 1 - x
    prob[1] = 1 - y
    prob[2] = 1 - x - y + m[0, 0]
    return prob

print('\nDixon-Coles Soccer\n\nenter home mean:')

muH = float(input('(?) '))

print('\nenter away mean:')

muA = float(input('(?) '))

print('')

rho = -0.15

m = dixon(muH, muA, rho)

q = score(m)

q = [round(x,4) for x in q]

print('home scores:',q[0],'\taway scores:',q[1],'\n')

while rho <= 0.0 :
    rho = round(rho,4)
    m = dixon(muH, muA, rho)
    p = hda(m)
    q = score(m)
    p = [round(x,4) for x in p]
    q = [round(x,4) for x in q]
    print('rho:',rho,'\thome:',p[0],'\tdraw:',p[1],'\taway:',p[2],'\tbtts:',q[2])
    rho+=0.01

print('')
