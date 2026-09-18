from simulador.motor import MotorSimulacao
from simulador.visual import InterfaceSimulador
 
if __name__ == "__main__":
    motor = MotorSimulacao()
    app = InterfaceSimulador(motor)
    app.root.mainloop()