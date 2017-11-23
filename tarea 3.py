import threading
import time
from random import *


ev_arq_pro = 2
ev_pro_tes = 2
ev_tes_arq = 1

sem1 = threading.Lock()
sem2 = threading.Lock()
sem3 = threading.Lock()

def arquitecto():
    print("el %s está comenzando su trabajo\n" %threading.currentThread().getName())
    time.sleep( 1 + randrange(10))
    print("el %s ha terminado su trabajo\n" %threading.currentThread().getName())
    evento_diseño()

def programador():
    print("el programador%s está programando\n" %threading.currentThread().getName())
    time.sleep( 1 + randrange(10))
    print("el programador%s termino de programar\n" %threading.currentThread().getName())
    evento_programador()

def tester():
    print("el tester está revisando el proyecto realizado por los programadores \n")
    time.sleep( 1 + randrange(10) )
    print("el tester ha encontrado nuevas fallas y debe ser reenviado a los diseñadores para rehacer el software \n")
    evento_tester()

#----------------------------------------------------------

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

def evento_tester():
    analista = threading.Thread(target=arquitecto, name='Analista')
    diseñador = threading.Thread(target=arquitecto, name='Diseñador')
    analista.start()
    diseñador.start()
    analista.join()
    diseñador.join()
    


def main():
    analista = threading.Thread(target=arquitecto, name='Analista')
    diseñador = threading.Thread(target=arquitecto, name='Diseñador')
    analista.start()
    diseñador.start()
    analista.join()
    diseñador.join()


if __name__ == '__main__':
    main()