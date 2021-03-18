import threading
import time
import random as rd


class Petri(object):
    def __init__(self):
        super(Petri, self).__init__()
        self.ev_arq_pro = 2
        self.ev_pro_tes = 2
        self.sem1 = threading.Lock()
        self.sem_arq = threading.Semaphore(0)
        self.sem_prog = threading.Semaphore(0)
        self.sem_test = threading.Semaphore(0)


    # elemento arquitecto (alalista y diseñador)
    def arquitecto(self):
        while True :
            self.sem_arq.acquire()
            print("el %s está comenzando su trabajo\n" %threading.currentThread().getName())
            self.__tiempoTrabajo__()
            print("el %s ha terminado su trabajo\n" %threading.currentThread().getName())
            self.sem1.acquire()
            self.evento_diseño()
            self.sem1.release()


    # elemento programador
    def programador(self):
        while True:
            self.sem_prog.acquire()
            print("el programador%s está programando\n" %threading.currentThread().getName())
            self.__tiempoTrabajo__()
            print("el programador%s termino de programar\n" %threading.currentThread().getName())
            self.sem1.acquire()
            self.evento_programador()
            self.sem1.release()


    # elemento tester
    def tester(self):
        while True:
            self.sem_test.acquire()
            print("el tester está revisando el proyecto realizado por los programadores \n")
            self.__tiempoTrabajo__()
            print("el tester acaba de analizar el programa pero ha encontrado nuevas fallas \n")
            self.sem1.acquire()
            self.evento_tester()
            self.sem1.release()


    # evento de del diseñador, cuando el analista y diseñador termine, esta da inicio a los programadores
    def evento_diseño(self):
        self.ev_arq_pro -= 1
        if self.ev_arq_pro == 0:
            print ("analista y diseñador terminado, los programadores empiezan a programar")
            self.ev_arq_pro = 2
            self.sem_prog.release()
            self.sem_prog.release()


    # evento de de los programadores, al terminar ambos, este activa al tester  
    def evento_programador(self):
        self.ev_pro_tes -= 1
        if self.ev_pro_tes == 0:
            print ("los programadores han terminado, ahora el tester revisará el trabajo")
            self.ev_pro_tes = 2
            self.sem_test.release()


    # evento del tester, es el unico evento que tiene 1 entrada, por lo tanto, cuando esta termina, hace iniciar automaticamente al analista y diseñador
    def evento_tester(self):
        print ("se ha enviado de nuevo el trabajo al analista y diseñador, buena suerte \n")
        self.sem_arq.release()
        self.sem_arq.release()


    def __tiempoTrabajo__(self):
        time.sleep(1 + rd.random()*9)


    def run(self):
        # elementos de trabajo
        analista = threading.Thread(target=self.arquitecto, name='Analista')
        diseñador = threading.Thread(target=self.arquitecto, name='Diseñador')
        programadorA = threading.Thread(target=self.programador, name='A')
        programadorB = threading.Thread(target=self.programador, name='B')
        tester_th = threading.Thread(target=self.tester)

        #inicia cada uno de los modulos en forma concurrente
        analista.start()
        diseñador.start()
        programadorA.start()
        programadorB.start()
        tester_th.start()

        #libera el analista y diseñador, que en este caso, da inicio al bucle de desarroyo
        self.sem_arq.release()
        self.sem_arq.release()
        
        #espera eternamente a que termine las tareas
        analista.join()
        diseñador.join()
        tester_th.join()
        programadorA.join()
        programadorB.join()


tarea = Petri()
tarea.run()