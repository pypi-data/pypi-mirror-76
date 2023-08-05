import synacell.cmodule
import synacell.signal
import matplotlib.pyplot as plt
import math
import numpy as np
import random
import time


def plot_simple() -> (int, str):
    """
    Test CellIntegrator

    :return: (int, str) 0 is success, everything else is error, str is mesage
    """

    # Generate wav file
    signal = synacell.signal
    sin1 = signal.func_generator(func_name="sin", freq=127.0, amp=200.0, phase=math.pi/2)
    sin1_arr = signal.func_to_nparray(func=sin1, t_min=0.0, t_max=1.0)
    signal.make_wav(sin1_arr, "./fft_simple.wav")

    api = synacell.cmodule.SnnAPI
    net = api.new_net()
    # Zero layer
    net.add_part("id=0,type=CellData,file=./fft_simple.wav")
    # First layer
    net.add_part("id=100,type=CellValve,ofs=0,opn=1,cls=3")
    net.add_part("id=101,type=CellValve,ofs=1,opn=1,cls=3")
    net.add_part("id=102,type=CellValve,ofs=2,opn=1,cls=3")
    net.add_part("id=103,type=CellValve,ofs=3,opn=1,cls=3")
    net.add_part("id=1000,type=SynaBuffer,ciid=0,coid=100")
    net.add_part("id=1001,type=SynaBuffer,ciid=0,coid=101")
    net.add_part("id=1002,type=SynaBuffer,ciid=0,coid=102")
    net.add_part("id=1003,type=SynaBuffer,ciid=0,coid=103")
    # Second layer
    net.add_part("id=200,type=CellIntegrator")
    net.add_part("id=201,type=CellIntegrator")
    net.add_part("id=202,type=CellIntegrator")
    net.add_part("id=203,type=CellIntegrator")
    net.add_part("id=2000,type=SynaRCA,ciid=100,coid=200")
    net.add_part("id=2001,type=SynaRCA,ciid=101,coid=201")
    net.add_part("id=2002,type=SynaRCA,ciid=102,coid=202")
    net.add_part("id=2003,type=SynaRCA,ciid=103,coid=203")

    net.connect_syna()
    net.set_recorder("id=0,pid=0,value=vo,beg=0,size=5000")
    net.set_recorder("id=100,pid=100,value=vo,beg=0,size=5000")
    net.set_recorder("id=200,pid=200,value=vo,beg=0,size=5000")
    net.set_recorder("id=201,pid=201,value=vo,beg=0,size=5000")
    net.set_recorder("id=202,pid=202,value=vo,beg=0,size=5000")
    net.set_recorder("id=203,pid=203,value=vo,beg=0,size=5000")

    net.reset()
    net.run(16000, 1.0 / 16000.0)
    record = dict()
    record[0] = net.get_record(0)
    record[100] = net.get_record(100)
    record[200] = net.get_record(200)
    record[201] = net.get_record(201)
    record[202] = net.get_record(202)
    record[203] = net.get_record(203)

    plot_range = np.asarray(range(0,1000))
    fig, ax = plt.subplots(2, 1, sharex='col')
    fig.suptitle('FFT test')
    ax[0].plot([i * 1.0 / 16000.0 for i in record[0].pc[plot_range]],
               record[0].data[plot_range], '-', label="Input signal")
    ax[0].plot([i * 1.0 / 16000.0 for i in record[100].pc[plot_range]],
               record[100].data[plot_range], '-', label="Cell 100 vo")
    ax[0].grid(True)
    ax[0].legend()

    # plot 2
    ax[1].grid(True)
    ax[1].plot([i * 1.0 / 16000.0 for i in record[200].pc[plot_range]],
               record[200].data[plot_range], '-', label="Cell 200 vo")
    ax[1].plot([i * 1.0 / 16000.0 for i in record[201].pc[plot_range]],
               record[201].data[plot_range], '-', label="Cell 201 vo")
    ax[1].plot([i * 1.0 / 16000.0 for i in record[202].pc[plot_range]],
               record[202].data[plot_range], '-', label="Cell 202 vo")
    ax[1].plot([i * 1.0 / 16000.0 for i in record[203].pc[plot_range]],
               record[203].data[plot_range], '-', label="Cell 203 vo")
    ax[1].legend()

    plt.xlabel("Time [s]")
    plt.show()

    return 0, "Success"


def net_tree_a():
    # Generate wav file
    signal = synacell.signal
    sin1 = signal.func_generator(func_name="sin", freq=500.0, amp=200.0, phase=math.pi/4)
    sin1_valid_on = signal.func_generator(func_name="linear", amp=20000.0)
    sin1_valid_off = signal.func_generator(func_name="linear", amp=0.0)
    sin1_arr = signal.func_to_nparray(func=sin1, t_min=0.0, t_max=1.0)
    sin1_valid_on = signal.func_to_nparray(func=sin1_valid_on, t_min=0.0, t_max=1.0)
    sin1_valid_off = signal.func_to_nparray(func=sin1_valid_off, t_min=0.0, t_max=1.0)
    signal.make_wav(sin1_arr, "./sin1.wav")
    signal.make_wav(sin1_valid_on, "./sin1_valid_on.wav")
    signal.make_wav(sin1_valid_off, "./sin1_valid_off.wav")

    api = synacell.cmodule.SnnAPI
    net = api.new_net()
    # Input layer
    pid = 0
    net.add_part(f"id={pid},type=CellMultiData,selid=0,fid=0,file=./sin1.wav")
    pid_input = pid
    pid += 1
    # 4k layer
    pid_4k = []
    for i in range(4):
        net.add_part(f"id={pid},type=CellValve,ofs={i},opn=1,cls=3")
        net.add_part(f"id={pid + 1},type=SynaBuffer,ciid={pid_input},coid={pid}")
        net.add_part(f"id={pid + 2},type=CellIntegrator")
        net.add_part(f"id={pid + 3},type=SynaBuffer,ciid={pid},coid={pid + 2}")
        pid_4k.append(pid + 2)
        pid += 4

    # 1k layer
    pid_1k = []
    for ipid in pid_4k:
        for j in range(4):
            net.add_part(f"id={pid},type=CellValve,ofs={j*4},opn=4,cls=12")
            net.add_part(f"id={pid + 1},type=SynaBuffer,ciid={ipid},coid={pid}")
            net.add_part(f"id={pid + 2},type=CellIntegrator")
            net.add_part(f"id={pid + 3},type=SynaBuffer,ciid={pid},coid={pid + 2}")
            pid_1k.append(pid + 2)
            pid += 4

    # Inner layer
    out_layer_cnt = 8
    pid_inner = []
    pid_train_kp = []
    pid_sampled = pid_1k
    for i in range(out_layer_cnt):
        net.add_part(f"id={pid},type=CellBuffer")
        pid_inner.append(pid)
        for j in range(len(pid_sampled)):
            net.add_part(f"id={pid + j + 1},type=SynaRCA,ciid={pid_sampled[j]}, coid={pid},kp=0.01")
            pid_train_kp.append(pid + j + 1)
        pid += 1
        pid += len(pid_sampled)

    # Outer layer
    pid_outer = []
    for i in range(out_layer_cnt):
        if i == 4:
            net.add_part(f"id={pid},"
                         f"type=CellMultiData,selid=0,fid=0,file=./sin1_valid_on.wav,validate=1")
        else:
            net.add_part(f"id={pid},"
                         f"type=CellMultiData,selid=0,fid=0,file=./sin1_valid_off.wav,validate=1")
        pid_outer.append(pid)
        for j in range(len(pid_inner)):
            net.add_part(f"id={pid + j + 1},type=SynaRCA,ciid={pid_inner[j]}, coid={pid},kp=0.01")
            pid_train_kp.append(pid + j + 1)
        net.set_recorder(f"id={i},pid={pid},value=vi,beg=0,size=5000")
        pid += 1
        pid += len(pid_inner)

    read_parameters(net, pid_train_kp, 100)
    run = False

    net.connect_syna()
    net.reset()
    net.run(16000, 1.0 / 16000.0)
    record = []
    for i in range(out_layer_cnt):
        record.append(net.get_record(i))

    plot_range = np.asarray(range(0, 5000))
    fig, ax = plt.subplots(2, 1, sharex='col')
    fig.suptitle('DFT test')
    for i in range(out_layer_cnt):
        ax[0].plot([i * 1.0 / 16000.0 for i in record[i].pc[plot_range]],
                   record[i].data[plot_range], '-', label=f"rec {i}")
    ax[0].grid(True)
    ax[0].legend()

    # plot 2
    ax[1].grid(True)
    ax[1].legend()

    plt.xlabel("Time [s]")
    plt.show()

    iter_num = 0
    run_steps = 4000

    dkp = 0.0001
    kp_change = 0.0001
    derr_dkp = dict()
    err_beg = 0
    err_start = 1
    while run:

        percent_inc = 0
        percent_inc_start = 0
        err_prev = err_beg

        save_parameters(net, pid_train_kp, iter_num)
        start_time = time.time()
        # Calculate inigial error
        err_beg = 0
        for i in range(num_of_signals):
            net.set_params(pid_input, f"selid={i}")
            net.reset()
            net.run(run_steps, 1.0 / 16000.0)
            for ipid in pid_outer:
                err_beg += net.get_param(ipid, "error")
        err_beg = err_beg/num_of_signals

        # Print some stat
        if iter_num > 0:
            percent_inc = 100 * (err_beg - err_prev)/err_prev
            percent_inc_start = 100 * (err_beg - err_start) / err_start
        else:
            err_start = err_beg

        print(f"curr_err = {err_beg}, error_change: {percent_inc:.3f}% (iteration) " +
              f"{percent_inc_start:.3f}% (overall)")
        pidit = 0
        icon = "-"

        # Run over train parameters
        for pid in pid_train_kp:
            # Print kp counter
            print("", end="\r")
            print(f"{pidit}/{len(pid_train_kp)}, {icon}", end="")
            pidit += 1
            kp_old = net.get_param(pid, "kp")
            # ------ Move up ------
            err_inc = 0
            net.set_params(pid, "kp=" + str(kp_old + dkp))
            for j in range(num_of_signals):
                net.set_params(0, f"selid={j}")
                net.reset()
                net.run(run_steps, 1.0 / 16000.0)
                for ipid in pid_outer:
                    err_inc += net.get_param(ipid, "error")
            err_inc = err_inc / num_of_signals

            # ------ Move down ------
            err_dec = 0
            net.set_params(pid, "kp=" + str(kp_old - dkp))
            for j in range(num_of_signals):
                net.set_params(0, f"selid={j}")
                net.reset()
                net.run(run_steps, 1.0 / 16000.0)
                for ipid in pid_outer:
                    err_dec += net.get_param(ipid, "error")
            err_dec = err_dec / num_of_signals

            if err_inc <= err_dec and err_inc < err_beg:
                derr_dkp[pid] = (err_beg - err_inc) / dkp
                icon = "\u2191"
            elif err_dec <= err_inc and err_dec < err_beg:
                derr_dkp[pid] = (err_beg - err_inc) / dkp
                icon = "\u2193"
            else:
                derr_dkp[pid] = 0
                icon = "-"
            net.set_params(pid, "kp=" + str(kp_old))

        # Calculate magnitute of change of kp
        vlen = 0
        for pid in pid_train_kp:
            vlen += derr_dkp[pid] * derr_dkp[pid]
        if vlen < 1.0e-18:
            break
        coef = math.sqrt(len(pid_train_kp) * kp_change * kp_change / vlen)

        # Change each kp
        for pid in pid_train_kp:
            new_kp = net.get_param(pid, "kp") + coef * derr_dkp[pid]
            net.set_params(pid, f"kp={new_kp}")

        iter_num += 1
        print("", end="\r")
        print(f"Iteration = {iter_num}, time: {int(time.time() - start_time)}s")

    return 0, "Success"


def save_parameters(net, rpc_li, iteration):
    file = open(f"./saved_parameters_{iteration}.txt", "w")
    for i in rpc_li:
        file.write(net.get_params(i) + "\n")
    file.close()


def read_parameters(net, rpc_li, iteration):
    file = open(f"./saved_parameters_{iteration}.txt", "r")
    for i in rpc_li:
        net.set_params(i, file.readline())
    file.close()

if __name__ == '__main__':
    '''
    1. If the module is ran (not imported) the interpreter sets this at the top of your module:
    ```
    __name__ = "__main__"
    ```
    2. If the module is imported: 
    ```
    import rk
    ```
    The interpreter sets this at the top of your module:
    ```
    __name__ = "rk"
    ```
    '''
    # plot_simple()
    net_tree_a()

