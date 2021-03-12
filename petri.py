import threading
import time
# from random import *
import random as rd

ev_arq_pro = 2
ev_pro_tes = 2

sem1 = threading.Lock()

sem_arq = threading.Semaphore(0)
sem_prog = threading.Semaphore(0)
sem_test = threading.Semaphore(0)




# elemento alalista-diseñador
def arquitecto():
    while True :
        sem_arq.acquire()
        print("el %s está comenzando su trabajo\n" %threading.currentThread().getName())
        time.sleep(1 + rd.randrange(10))
        print("el %s ha terminado su trabajo\n" %threading.currentThread().getName())
        sem1.acquire()
        evento_diseño()
        sem1.release()
        

# elemento programador
def programador():
    while True:
        sem_prog.acquire()
        print("el programador%s está programando\n" %threading.currentThread().getName())
        time.sleep(1 + rd.randrange(10))
        print("el programador%s termino de programar\n" %threading.currentThread().getName())
        sem1.acquire()
        evento_programador()
        sem1.release()
        


# elemento tester
def tester():
    while True:
        sem_test.acquire()
        print("el tester está revisando el proyecto realizado por los programadores \n")
        time.sleep(1 +  rd.randrange(10) )
        print("el tester acaba de analizar el programa pero ha encontrado nuevas fallas \n")
        sem1.acquire()
        evento_tester()
        sem1.release()


# evento de del diseñador, cuando el analista y diseñador termine, esta da inicio a los programadores
def evento_diseño():
    global ev_arq_pro
    ev_arq_pro -= 1
    if ev_arq_pro == 0:
        print ("analista y diseñador terminado, los programadores empiezan a programar \n")
        ev_arq_pro = 2
        sem_prog.release()
        sem_prog.release()

    
# evento de de los programadores, al terminar ambos, este activa al tester  
def evento_programador():
    global ev_pro_tes
    ev_pro_tes -= 1
    if ev_pro_tes == 0:
        print ("los programadores han terminado, ahora el tester revisará el trabajo \n")
        ev_pro_tes = 2
        sem_test.release()



# evento del tester, es el unico evento que tiene 1 entrada, por lo tanto, cuando esta termina, hace iniciar automaticamente al analista y diseñador
def evento_tester():
    print ("se ha enviado de nuevo el trabajo al analista y diseñador, buena suerte \n")
    sem_arq.release()
    sem_arq.release()

# funcion principal donde setea el primer elemento (analista, diseñador), luego automaticamente realiza el ciclo
def main():

    # elementos de trabajo
    analista = threading.Thread(target=arquitecto, name='Analista')
    diseñador = threading.Thread(target=arquitecto, name='Diseñador')
    programadorA = threading.Thread(target=programador, name='A')
    programadorB = threading.Thread(target=programador, name='B')
    Tester = threading.Thread(target=tester)

    #inicia cada uno de los modulos en forma concurrente
    analista.start()
    diseñador.start()
    programadorA.start()
    programadorB.start()
    Tester.start()

    #libera el analista y diseñador, que en este caso, da inicio al bucle de desarroyo
    sem_arq.release()
    sem_arq.release()
    
    #espera eternamente a que termine las tareas
    analista.join()
    diseñador.join()
    programadorA.join()
    programadorB.join()
    Tester.join()


if __name__ == '__main__':
    main()
