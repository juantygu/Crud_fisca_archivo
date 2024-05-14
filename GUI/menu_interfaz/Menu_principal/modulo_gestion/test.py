import tkinter as tk
import json
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import ttk
from consultas.consultas_auditor import ConsultasAuditor
from consultas.consultas_expediente import ConsultasExpediente
from entidades.expediente import Expediente

class Test:

    def obtener_auditores(self):
        self.auditor = ConsultasAuditor()

        mensaje, auditores = self.auditor.mostrar_nombre_id_auditores()
        if auditores:
            print(mensaje)
            dic_auditores = {auditor[0]: auditor[1] for auditor in auditores}
            #print(dic_auditores)
            return dic_auditores
        else:
            print(mensaje)


#auditor = Test()
#result = auditor.obtener_auditores()
#print(result)