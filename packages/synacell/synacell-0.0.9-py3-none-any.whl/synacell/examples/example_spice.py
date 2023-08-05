import synacell.cmodule
import synacell.signal as signal
import matplotlib.pyplot as plt
import ltspice
import os
from shutil import copy2
import pkg_resources


def generate_spice_input(spice_filename=""):
    """
    Generates PWL file for loading in spice.
    """
    if spice_filename in ["SynaRCA-ode1", "SynaRCA-ode2"]:
        # Generate wav file
        sin1 = signal.func_generator(func_name="sin", freq=133.0, amp=30.0, phase=0.0)
        sin1_arr = signal.func_to_nparray(func=sin1, t_min=0.0, t_max=1.0)
        signal.make_wav(sin1_arr, "./SynaRCA.wav")

        # Get CellValve output
        api = synacell.cmodule.SnnAPI
        net = api.new_net()
        net.add_part("id=0,type=CellData,file=./SynaRCA.wav")
        net.add_part("id=1000,type=SynaBuffer,ciid=0,coid=1")
        net.add_part("id=1,type=CellValve,ofs=10,opn=7,cls=14")
        net.connect_syna()
        net.set_recorder("id=0,pid=1,value=vo,beg=0,size=16000")
        net.reset()
        net.run(16000, 1.0 / 16000.0)
        rec = net.get_record(0)

        # Generate pwl file
        rec.print_pwl(file_name=f'./{spice_filename}.pwl')

        plt.plot([i * 1.0 / 16000.0 for i in rec.pc], rec.data, label="CellValve_vo")
        plt.grid(True)
        plt.title("Input generated with synacell")
        plt.xlabel("Time [s]")
        plt.legend()
        plt.show()


def run_spice_simulation(spice_filename=""):

    if spice_filename in ["SynaRCA-ode1", "SynaRCA-ode2"]:
        # Run file through RPC synapse
        api = synacell.cmodule.SnnAPI
        net = api.new_net()
        if os.path.isfile("./SynaRCA.wav") is False:
            print("There is no SynaRCA.wav file")
            return
        net.add_part("id=0,type=CellData,file=./SynaRCA.wav")
        net.add_part("id=1000,type=SynaBuffer,ciid=0,coid=1")
        net.add_part("id=1,type=CellValve,ofs=10,opn=7,cls=14")
        if spice_filename == "SynaRCA-ode1":
            net.add_part("id=1001,type=SynaRCA,ciid=1,coid=2")
        elif spice_filename == "SynaRCA-ode2":
            net.add_part("id=1001,type=SynaRCA,cs=100.0e-9,ciid=1,coid=2")
        net.add_part("id=2,type=CellBuffer")
        net.connect_syna()
        net.set_recorder("id=0,pid=2,value=vi,beg=0,size=16000")
        net.reset()
        net.run(16000, 1.0 / 16000.0)
        rec = net.get_record(0)

        # Copy spice model .raw and .asc in working dir
        if os.path.isfile(f"./{spice_filename}.raw") is False:
            fname = pkg_resources.resource_filename('synacell', f'examples/{spice_filename}.raw')
            copy2(fname, './')
        if os.path.isfile("./SynaRCA-ode1.asc") is False:
            fname = pkg_resources.resource_filename('synacell', f'examples/{spice_filename}.asc')
            copy2(fname, './')
        if os.path.isfile(f"./{spice_filename}.raw") is False:
            print(f"There is no LTSpice file: '{spice_filename}.raw'")
            return

        # Run spice model
        spc = ltspice.Ltspice(f'{spice_filename}.raw')
        spc.parse()
        time = spc.getTime()
        vi = spc.getData('v(vi)')
        vo = spc.getData('v(vo)')

        plt.plot([i * 1.0 / 16000.0 for i in rec.pc[0:300]], rec.data[0:300], '.-',
                 label="SynaRCA[vo]")
        plt.plot(spc.getTime()[0:300], spc.getData('v(vo)')[0:300], '.--',
                 label="LTSpice[vo]")
        plt.grid(True)
        plt.xlabel("Time [s]")
        plt.legend()
        plt.show()


def run_spice(spice_filename=""):
    if spice_filename == "SynaRCA":
        generate_spice_input("SynaRCA-ode1")
        run_spice_simulation("SynaRCA-ode1")
        run_spice_simulation("SynaRCA-ode2")
    elif spice_filename in ["SynaRCA-ode1", "SynaRCA-ode2"]:
        generate_spice_input(spice_filename)
        run_spice_simulation(spice_filename)
    else:
        print(f"Spice filename '{spice_filename}' not recognized")


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
    run_spice("SynaRCA")
