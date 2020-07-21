from FuncoesPrincipais import *
from ExerciciosRelatório import *

#   EP1 2019 MACHINE LEARNING
# Alunos: Rafael Sobral Augusto - NUSP:10337193, Gustavo Correia Neves Carvas - NUSP:10335962
# Turma: 4
# Professor: Salvador A. Zanata


def main():
    print('############--EP1 2019 MACHINE LEARNING--############')
    print()
    print('Alunos: Rafael Sobral Augusto - NUSP:10337193, Gustavo Correia Neves Carvas - NUSP:10335962')
    print('Professor: Salvador A. Zanata, Turma: 4')
    print()
    print()
    continuar = True
    while continuar:
        decisao = int(input("Você deseja realizar o treinamento e a classificação de digitos ou deseja realizar os exercicios a),b),c), d) ou a Segunda Tarefa do enunciado? \n Digite 1 para Treinamento e classificação, 0 para exercicios: "))
        if decisao == 1:
            TreinamentoClassificacao()
            continuar = int(input("Quer realizar outro treinamento/exercicio? \nDigite 1 caso sim: ")) == 1
            print()
        elif decisao == 0:
            Exercicio()
            continuar = int(input("Quer realizar outro treinamento/exercicio? \nDigite 1 caso sim: ")) == 1
            print()
        else:
            print("Entrada inválida, tente novamente")
main()