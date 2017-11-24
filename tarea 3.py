import threading
import time
from random import *


ev_arq_pro = 2
ev_pro_tes = 2

sem1 = threading.Lock()
sem2 = threading.Lock()

# elemento alalista-diseñador
def arquitecto():
    print("el %s está comenzando su trabajo\n" %threading.currentThread().getName())
    time.sleep( 1 + randrange(10))
    print("el %s ha terminado su trabajo\n" %threading.currentThread().getName())
    evento_diseño()

# elemento programador
def programador():
    print("el programador%s está programando\n" %threading.currentThread().getName())
    time.sleep( 1 + randrange(10))
    print("el programador%s termino de programar\n" %threading.currentThread().getName())
    evento_programador()

# elemento tester
def tester():
    print("el tester está revisando el proyecto realizado por los programadores \n")
    time.sleep( 1 + randrange(10) )
    print("el tester ha encontrado nuevas fallas y debe ser reenviado a los diseñadores para rehacer el software \n")
    evento_tester()


# evento de del diseñador, cuando el analista y diseñador termine, esta da inicio a los programadores
def evento_diseño():
    sem1.acquire()
    global ev_arq_pro
    ev_arq_pro -= 1
    if ev_arq_pro == 0:
        ev_arq_pro = 2
        programadorA = threading.Thread(target=programador, name='A')
        programadorB = threading.Thread(target=programador, name='B')
        sem1.release()
        programadorA.start()
        programadorB.start()
        programadorA.join()
        programadorB.join()
    else:
        sem1.release()
    
# evento de de los programadores, al terminar ambos, este activa al tester  
def evento_programador():
    sem2.acquire()
    global ev_pro_tes
    ev_pro_tes -= 1
    if ev_pro_tes == 0:
        ev_pro_tes = 2
        Tester = threading.Thread(target=tester)
        sem2.release()
        Tester.start()
        Tester.join()
    else:
        sem2.release()


# evento del tester, es el unico evento que tiene 1 entrada, por lo tanto, cuando esta termina, hace iniciar automaticamente al analista y diseñador
def evento_tester():
    analista = threading.Thread(target=arquitecto, name='Analista')
    diseñador = threading.Thread(target=arquitecto, name='Diseñador')
    analista.start()
    diseñador.start()
    analista.join()
    diseñador.join()
    

# funcion principal donde setea el primer elemento (analista, diseñador), luego automaticamente realiza el ciclo
def main():
    analista = threading.Thread(target=arquitecto, name='Analista')
    diseñador = threading.Thread(target=arquitecto, name='Diseñador')
    analista.start()
    diseñador.start()
    analista.join()
    diseñador.join()


if __name__ == '__main__':
    main()
