import numpy as np
import time

def RotGivensComA(i,j,c,s,W,A):
    Maux=np.subtract(np.multiply(W[i],c),np.multiply(W[j],s)) #calcula uma vetor linha auxiliar resulado da conta W[i]*c-W[j]*s
    W[j]=np.add(np.multiply(W[i],s),np.multiply(W[j],c)) #redefine a linha j da matriz W como W[i]*s+W[j]*c
    W[i]=Maux #redefine a linha W[i] como a matriz auxiliar
    MauxA=np.subtract(np.dot(A[i],c),np.dot(A[j],s)) #faz as mesmas operacoes que acima, com os mesmos c e s definidos pela matriz W, para a matriz A
    A[j]=np.add(np.dot(A[i],s),np.dot(A[j],c))
    A[i]=MauxA

def EncontraWeA(M1,K2):
    M2 = np.copy(K2) #copia a matriz A original pra não ser alterada quando é escalonada
    for k in range(len (M1[0])): #roda as colunas de W
        for j in range(len(M1)-1, k, -1): #loop para calcular tau, c e s de cada linha e fazer o respectivo RotGivens
            i = j-1
            x=M1[j][k]
            y=M1[i][k]
            if x != 0:
                if abs(y)>abs(x):
                    t=-x/y
                    c=1/np.sqrt(1+t**2)
                    s=c*t
                else:
                    t=-y/x
                    s=1/np.sqrt(1+t**2)
                    c=s*t
                RotGivensComA(i,j,c,s,M1,M2)
    return M1, M2

def CalculaH(M1,M2):
    p = len(M1[0])
    if type(M2[0]) is np.float64: #uso essa função pra calcular quando M2 é so vetor, como pedido no exs a) e b) do pdf então preciso tratar o caso em que M2 é vetor
        m = 1
    else:
        m = len(M2[0])
    M3 = np.zeros((p,m))
    for k in range(p-1,-1,-1):
        M3[k]=np.divide((np.subtract(M2[k],np.dot(M1[k],M3))),M1[k][k])
    return M3

def montaA(arq,ndig_treino):
    X=np.zeros((784,ndig_treino)) #cria array inteiramente zerada com a dimensão de A - assume len como 784 porque é predefinido no enunciado
    for i in range(784):
        linha=arq.readline().strip()
        X[i]=np.array(linha.split())[0:ndig_treino]
        for j in range(len(X[i])):
            X[i][j]=int(X[i][j])/255 #transforma todos os elementos em int, normalizando
    return X

def TreinamentoClassificacao():
    start =  time.time()
    erro = 1e-5
    itmax = 100
    Wdic={} #dicionario que armazena todas as Wd calculadas
    m=int(input("Quantos arquivos voce quer usar pra treinar (De 0 a 5300)? "))
    p =int(input("Quantos componentes você deseja para aproximar? "))
    n_test=int(input("Quantos digitos voce quer testar (De 0 e 10000)? ")) #vamo fazer td os inputs direto
    for i in range(10):
        erroAnt = 10 #qualquer valor de erro só pra fazer a primeira comparação
        arquivo="train_dig{}.txt".format(i) 
        arqopen=open(arquivo,"r") #abre o arquivo correspondente ao digito a ser treinado
        Aorig=montaA(arqopen,m) #gera a matriz A que queremos usar pra treinar
        arqopen.close() #fecha o arquivo pra ele não ficar aberto o tempo todo que o programa roda
        n=len(Aorig)
        Aorigtransp=np.transpose(Aorig) #transpoe uma vez soh, pra nao ter que ficar transpondo
        W=np.random.rand(n,p) #cria matriz W randomicamente
        it = 0
        continuar = True #variavel booleana que encerra o loop de treino quando a diferenca entre os erros é menor que 10^-5
        while it < itmax and continuar:
            it+=1
            W = W/np.linalg.norm(W, axis=0) #normaliza W
            W, A = EncontraWeA(W, Aorig) #escalona W com A
            H = CalculaH(W, A) #resolve o mmq e calcula H
            H[H<0]=0 #transforma H numa matriz positiva
            Htransp = np.transpose(H) #transpoe H pra virar a matriz de coeficientes
            Htransp, Atransp = EncontraWeA(Htransp,Aorigtransp)
            Wtransp = CalculaH(Htransp, Atransp) #resolve mmq e calcula W
            Wtransp[Wtransp<0]=0 #transforma Wtransp em uma matriz positiva
            erroCalc = np.linalg.norm(np.subtract(Aorig,np.dot(W,H))) #calcula o modulo da diferença entre A e WH
            W = np.transpose(Wtransp) #destranspoe W
            if (abs(erroAnt - erroCalc)> erro):
                erroAnt = erroCalc
            else: #erro entre passos já é menor q o erro que se deseja
                continuar = False 
        Wdic[i]=W
        print("O digito {} treinou".format(i), "em",it,"iteracoes, com erro",erroCalc)
    teste=open("test_images.txt","r")
    Atesteorig=montaA(teste,n_test) #monta a A dos testes
    teste.close() #fecha o arquivo pra nao ficar aberto o programa todo
    i=0
    k=0
    digito=np.zeros((n_test,2))
    for k in range(10): #resolve o sistema WH=A pra todos os Wd e a A original do teste
        Wteste=np.copy(Wdic[k])
        Wteste, Ateste=EncontraWeA(Wteste,Atesteorig)
        Hteste=CalculaH(Wteste,Ateste)
        X=np.subtract(Atesteorig,np.dot(Wdic[k],Hteste)) #calcula A-WH
        for i in range(n_test): #calcula o erro de cada coluna pra ver qual é o menor
            erroteste=np.linalg.norm(X[:,i]) #calcula o modulo da diferença entre a coluna i de A e de WH
            if k==0:
                digito[i]=[k,erroteste]
            elif erroteste<digito[i][1]: #atualiza se o erro desse digito eh o menor ate o momento
                digito[i]=[k,erroteste]
    i,j=0,0
    teste_index=open("test_index.txt","r") 
    gabarito=teste_index.readlines()
    for i in range(len(gabarito)):
        gabarito[i]=int(gabarito[i][0])
    teste_index.close() #fecha arquivo de index pra nao ficar aberto tanto tempo
    certos=0
    k=0
    Porcentagem={} 
    acerto=np.zeros((10,2)) #armazena total de vezes que tem um digito no arquivo teste_index na posicao 1 e quantas vezes acerto isso na posicao 0
    for j in range(n_test):
        acerto[gabarito[j]][1]=acerto[gabarito[j]][1]+1 
        if digito[j][0]==gabarito[j]:
            certos+=1 #soma o total de acertos no arquivo inteiro
            acerto[gabarito[j]][0]=acerto[gabarito[j]][0]+1
    Porcentagem_total=(certos/n_test)
    Porcentagem = {} #armazena em um dicionario a porcentagem de acerto de cada digito
    for t in range(10):
        if acerto[t][1]!=0:
            Porcentagem[t]=acerto[t][0]/acerto[t][1] #calcula
        else:
            Porcentagem[t]="Não definida pois não há esse dígito no gabarito"
        print("O digito", t, "obteve uma porcentagem de acerto total igual a", 100*Porcentagem[t])
    print()
    print("A porcentagem total de acertos foi", 100*Porcentagem_total)
    print()
    end = time.time()
    print("O tempo total do código rodando para esses resultados foi:", end-start,"seg")
    print("Aproximadamente", int((end-start)//60),"min", round(end-start)%60, "seg")
    print(Porcentagem)        