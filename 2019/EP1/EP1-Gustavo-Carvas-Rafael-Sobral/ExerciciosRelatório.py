import numpy as np
from FuncoesPrincipais import RotGivensComA, EncontraWeA, CalculaH

def Exercicio():
    tarefa = int(input('Quer realizar a Primeira Tarefa (digite 1) ou a Segunda Tarefa (digite 2)?'))
    if tarefa == 1:
        tipo = input('Escolha entre os exercicios, a), b), c) ou d): ')
        if tipo == 'a)' or tipo == 'a':
            n = 64
            m = 64
            W = np.zeros((n,m))
            A = np.zeros(n)
            i=0
            while i<n:
                A[i] = 1
                j=0
                while j<m:
                    if i == j:
                        W[i][j] = 2
                    elif abs(i-j) == 1:
                        W[i][j] = 1
                    j+=1
                i+=1
                
        elif tipo == 'b)' or tipo == 'b':
            n = 20
            m = 17
            W = np.zeros((n,m))
            A = np.zeros(n)
            i=0
            while i<n:
                A[i] = i+1
                j=0
                while j<m:
                    if abs(i-j)<=4:
                        W[i][j] = 1/((i+1)+(j+1)-1)   
                    j+=1
                i+=1

        elif tipo == 'c)' or tipo == 'c':
            n = 64
            p = 64
            m = 3
            W = np.zeros((n,p))
            A = np.zeros((n,m))
            i=0
            while i<n:
                k=0
                j=0
                while k<m:
                    if k == 0:
                        A[i][k] = 1
                    elif k == 1:
                        A[i][k] = i+1
                    else:
                        A[i][k] = 2*(i+1)-1
                    k+=1
                while j<p:
                    if i == j:
                        W[i][j] = 2
                    elif abs(i-j) == 1:
                        W[i][j] = 1
                    j+=1
                i+=1

        elif tipo == 'd)' or tipo == 'd':
            n = 20
            p = 17
            m = 3
            W = np.zeros((n,p))
            A = np.zeros((n,m))
            i=0
            while i<n:
                k=0
                while k<m:
                    if k == 0:
                        A[i][k] = 1
                    elif k == 1:
                        A[i][k] = i+1
                    else:
                        A[i][k] = 2*(i+1)-1
                    k+=1
                j=0
                while j<p:
                    if abs(i-j)<=4:
                        W[i][j] = 1/((i+1)+(j+1)-1)
                    j+=1
                i+=1
        W,A = EncontraWeA(W,A)
        H = CalculaH(W,A) # no caso do a) e b) esse H na verdade é o vetor x
        print("Segue a resposta encontrada: ")
        print()
        print(H)
        
    elif tarefa == 2:
        itmax = 100
        Aorig = np.array([[3/10,3/5,0],[1/2,0,1],[4/10,4/5,0]])
        Aorigtransp = np.transpose(Aorig)
        p = 2
        n = len(Aorig)
        m = len(Aorig[0])
        continuar = True
        erro = 1e-5
        W=np.random.rand(n,p) #cria matriz W randomicamente
        it = 0
        erroAnt = -100000 #qualquer valor de erro só pra fazer a primeira comparação
        erroCalc = -1000
        while it < itmax and continuar:
            it+=1
            W = W/np.linalg.norm(W, axis=0) #normaliza a matriz W
            W, A = EncontraWeA(W, Aorig) #escalona W com A
            H = CalculaH(W, A) #acha a soluçao H
            H[H<0]=0 #transforma H numa matriz positiva
            Hsalvo = np.copy(H)
            Htransp = np.transpose(H) #transpoe H pra virar a matriz de coeficientes
            Htransp, Atransp = EncontraWeA(Htransp,Aorigtransp) #escalona H e A transpostas
            Wtransp = CalculaH(Htransp, Atransp) #acha a solucao W
            Wtransp[Wtransp<0]=0 #transforma Wtransp em uma matriz positiva
            erroCalc = np.linalg.norm(np.subtract(Aorig,np.matmul(W,H))) #calcula o modulo da diferença entre A e WH
            W = np.transpose(Wtransp) #destranspoe W
            if (abs(erroAnt - erroCalc)> erro):
                erroAnt = erroCalc
            else: #erro entre passos já é menor q o erro que se deseja
                continuar = False 
        print('A original: \n', Aorig)
        print('W obtido: \n', W)
        print('H obtido: \n', Hsalvo)
# def Exercicio():
#     tipo = input('Escolha entre os exercicios, a), b), c) ou d): ')
#     exercicioRel(tipo)