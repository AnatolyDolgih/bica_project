from logger import clearLog
import baseMoralScheme as bms
import  virtualTutor as vt

if __name__ == "__main__":
    clearLog()
    tutor = vt.VirtualTutor()
    tutor.start()