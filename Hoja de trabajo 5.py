import simpy
import random
random.seed(0)

Process={}
IO={}
CPU={}
Time={}
TInitial={}
interval=0

env=simpy.Environment()
initial_ram = simpy.Container(env, 100, init=100)
initial_cpu = simpy.Resource(env, capacity=2)
initial_process = 200
def process(name, env, memory, arrival, CPU_Time, RamUsed):

    yield env.timeout(arrival)
    print('%s proceso en cola NEW --> %d cantidad ram requerida %d' % (name, env.now, RamUsed))
    memory.get(RamUsed)
    Processinuse=Process.get(name)
    CPU[name]=Processinuse
    print('%s proceso en cola READY --> %d Cantidad de ram %d' % (name, env.now, RamUsed))
    with initial_cpu.request() as req:
        yield req
        CPU_Time=CPU_Time-3
    if CPU_Time<=0:
        print('%s proceso ha salido de la cola RUNNING --> %s' %(name, env.now))
        tFinal=env.now
        TInitial=TInitial[name]
        prom=tFinal-TInitial
        Time[name]=[prom]
        memory.put(RamUsed)
        CPU.pop(name)
        for i in range(len(Time)):
            key1=list(Time.items())[i][0]
            print(Time[key1])
    elif CPU_Time>0:
        n1=random.randint(1, 2)
        if n1==1:
            Processinuse=CPU.get(name)
            name=Processinuse[0]
            env=Processinuse[1]
            memory=Processinuse[2]
            arrival=Processinuse[3]
            CPU_Time=CPU_Time
            RamUsed=Processinuse[5]
            env.process(process(name, env, memory, arrival, CPU_Time, RamUsed))
        else:
            IO[name]=CPU.get(name)

    while len(IO)>0:
        if len(IO)>=1:
            n2=random.randint(1,2)
            if n2==1:
                key2=list(IO.items())[0][0]
                print('%s proceso en cola Ready --> %s' % (name, env.now))
                Processinuse=IO.get(key2)
                name = Processinuse[0]
                env = Processinuse[1]
                memory = Processinuse[2]
                arrival = Processinuse[3]
                CPU_Time = CPU_Time
                RamUsed = Processinuse[5]
                IO.pop(key2)
                env.process(process(name, env, memory, arrival, CPU_Time, RamUsed))



for i in range(initial_process):
    arrival=interval
    CPU_Time = random.randint(1, 10)
    RamUsed = random.randint(1, 10)
    iString=str(i)
    Process["Proceso "+ iString]=["Proceso "+iString, env, initial_ram, arrival, CPU_Time, RamUsed]
    interval+=1

for i in range(len(Process)):
    iString=str(i)
    ProcessUse=Process.get("Proceso "+iString)
    name=ProcessUse[0]
    env=ProcessUse[1]
    memory=ProcessUse[2]
    arrival=ProcessUse[3]
    CPU_Time=ProcessUse[4]
    RamUsed=ProcessUse[5]
    TInicial[name]=arrival
    env.process(process(name, env, memory, arrival, CPU_Time, RamUsed))

env.run()

