import tkinter as tk
import json
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import ttk
from consultas.consultas_expediente import ConsultasExpediente
from entidades.expediente import Expediente

class ExpedienteCrud:

    def __init__(self,ventana_principal, elementos, interfaz):
        """
                Constructor de la clase ExpedienteCrud.

                Args:
                    ventana_principal: La ventana principal de la interfaz gráfica.
                    elementos: Objeto que contiene los elementos de la interfaz gráfica.
                    interfaz: Objeto que representa la interfaz gráfica en general.
                """
        self.ventana_principal = ventana_principal
        self.elementos = elementos
        self.interfaz = interfaz
        self.consultas_expediente = ConsultasExpediente()
        self.expediente = Expediente()
        self.elementos.ventana_credenciales_abierta = False

    def mostrar_expediente_crud(self):
        """
                        Método para mostrar la interfaz de gestión de expedientes.
                        """
        self.interfaz.estado_actual = "gestion_expedientes_crud"
        print(self.interfaz.estado_actual)

        try:
            altura_pantalla = self.interfaz.window_height
            ancho_pantalla = self.interfaz.window_width

            # ==== TITULO ======
            self.elementos.label_titulo = tk.Label(self.ventana_principal, text="GESTIÓN DE EXPEDIENTE",
                                                   font=("Arial", 30, "bold"), fg="black", bg="#E6F7FF")

            self.elementos.label_titulo.pack(pady=20)  # pady añade un espacio en la parte inferior de la etiqueta
            # ====LABEL IFRAME====
            self.elementos.label_frame = tk.LabelFrame(self.ventana_principal, text="DATOS DEL EXPEDIENTE",
                                                       font=("Arial", 18, "bold"), fg="black", bg="#E6F7FF", bd=5,
                                                       relief=tk.RIDGE)
            self.elementos.label_frame.place(x=30, y=80, width=450, height= 450)

            # =========== ETIQUETA ID_EXPEDIENTE =============
            self.elementos.label_id_expediente = tk.Label(self.elementos.label_frame, text="ID_expediente",
                                                             font=("Arial", 14, "bold"),
                                                             fg="black", bg="#E6F7FF")
            self.elementos.label_id_expediente.place(x=20, y=10)

            # =====CAJA ID_expediente =========
            self.elementos.box_id_expediente = tk.Entry(self.elementos.label_frame,
                                                           textvariable=self.elementos.id_variable_expediente, bd=3,
                                                           font=("Arial", 12), width=12, insertbackground="blue",
                                                           selectbackground="blue",
                                                           relief=tk.RIDGE)
            self.elementos.box_id_expediente.place(x=190, y=10)
            self.elementos.box_id_expediente.delete(0,
                                                       tk.END)

            # ======== ETIQUETA ID_CONTRIBUYENTE ==============
            self.elementos.label_id_contribuyente = tk.Label(self.elementos.label_frame, text="ID_contribuyente",
                                                             font=("Arial", 14, "bold"),
                                                             fg="black", bg="#E6F7FF")
            self.elementos.label_id_contribuyente.place(x=20, y=50)

            # =====CAJA ID_Contribuyente =========
            self.elementos.box_id_contribuyente = tk.Entry(self.elementos.label_frame,
                                                           textvariable=self.elementos.id_variable_contribuyente, bd=3,
                                                           font=("Arial", 12), width=12, insertbackground="blue",
                                                           selectbackground="blue",
                                                           relief=tk.RIDGE)
            self.elementos.box_id_contribuyente.place(x=190, y=50)
            self.elementos.box_id_contribuyente.delete(0,
                                                       tk.END)

            # ===== ETIQUETA ID_Auditor ======
            self.elementos.label_id_auditor = tk.Label(self.elementos.label_frame, text="ID_auditor",
                                                       font=("Arial", 14, "bold"),
                                                       fg="black", bg="#E6F7FF")
            self.elementos.label_id_auditor.place(x=20, y=90)

            # =====CAJA ID_Auditor =========
            self.elementos.box_id_auditor = tk.Entry(self.elementos.label_frame,
                                                     textvariable=self.elementos.id_variable_auditor, bd=3,
                                                     font=("Arial", 12), width=12, insertbackground="blue",
                                                     selectbackground="blue",
                                                     relief=tk.RIDGE)
            self.elementos.box_id_auditor.place(x=190, y=90)
            self.elementos.box_id_auditor.delete(0, tk.END)

            # =====ETIQUETA ID_proceso ======
            self.elementos.label_id_proceso = tk.Label(self.elementos.label_frame, text="ID_proceso",
                                                       font=("Arial", 14, "bold"),
                                                       fg="black", bg="#E6F7FF")
            self.elementos.label_id_proceso.place(x=20, y=130)

            # =====CAJA ID_proceso =========
            self.elementos.box_id_proceso = tk.Entry(self.elementos.label_frame,
                                                     textvariable=self.elementos.id_variable_proceso, bd=3,
                                                     font=("Arial", 12), width=12, insertbackground="blue",
                                                     selectbackground="blue",
                                                     relief=tk.RIDGE)
            self.elementos.box_id_proceso.place(x=190, y=130)
            self.elementos.box_id_proceso.delete(0, tk.END)

            # =====ETIQUETA ID_prestamo ======
            self.elementos.label_id_prestamo = tk.Label(self.elementos.label_frame, text="ID_prestamo",
                                                       font=("Arial", 14, "bold"),
                                                       fg="black", bg="#E6F7FF")
            self.elementos.label_id_prestamo.place(x=20, y=170)
            # =====CAJA ID_prestamo =========
            self.elementos.box_id_prestamo = tk.Entry(self.elementos.label_frame,
                                                     textvariable=self.elementos.id_variable_prestamo, bd=3,
                                                     font=("Arial", 12), width=12, insertbackground="blue",
                                                     selectbackground="blue",
                                                     relief=tk.RIDGE)
            self.elementos.box_id_prestamo.place(x=190, y=170)
            self.elementos.box_id_prestamo.delete(0, tk.END)

            # =====ETIQUETA ID_caja ======
            self.elementos.label_id_caja = tk.Label(self.elementos.label_frame, text="ID_caja",
                                                        font=("Arial", 14, "bold"),
                                                        fg="black", bg="#E6F7FF")
            self.elementos.label_id_caja.place(x=20, y=210)
            # =====CAJA ID_caja =========
            self.elementos.box_id_caja = tk.Entry(self.elementos.label_frame,
                                                      textvariable=self.elementos.id_variable_caja, bd=3,
                                                      font=("Arial", 12), width=12, insertbackground="blue",
                                                      selectbackground="blue",
                                                      relief=tk.RIDGE)
            self.elementos.box_id_caja.place(x=190, y=210)
            self.elementos.box_id_caja.delete(0, tk.END)

            # =====ETIQUETA ESTADO ======
            self.elementos.label_estado = tk.Label(self.elementos.label_frame, text="Estado",
                                                    font=("Arial", 14, "bold"),
                                                    fg="black", bg="#E6F7FF")
            self.elementos.label_estado.place(x=20, y=250)
            # =====CAJA ESTADO =========
            self.elementos.box_estado = tk.Entry(self.elementos.label_frame,
                                                  textvariable=self.elementos.estado_variable, bd=3,
                                                  font=("Arial", 12), width=12, insertbackground="blue",
                                                  selectbackground="blue",
                                                  relief=tk.RIDGE)
            self.elementos.box_estado.place(x=190, y=250)
            self.elementos.box_estado.delete(0, tk.END)

            # =====ETIQUETA año gravable ======
            self.elementos.label_año_gravable = tk.Label(self.elementos.label_frame, text="Año gravable",
                                                   font=("Arial", 14, "bold"),
                                                   fg="black", bg="#E6F7FF")
            self.elementos.label_año_gravable.place(x=20, y=290)
            # =====CAJA año gravable =========
            self.elementos.box_año_gravable = tk.Entry(self.elementos.label_frame,
                                                 textvariable=self.elementos.año_gravable_variable, bd=3,
                                                 font=("Arial", 12), width=12, insertbackground="blue",
                                                 selectbackground="blue",
                                                 relief=tk.RIDGE)
            self.elementos.box_año_gravable.place(x=190, y=290)
            self.elementos.box_año_gravable.delete(0, tk.END)

        except Exception as e:
            # Si ocurre algún error, imprime un mensaje de error
            print("Error al mostrar gestion auditor:", str(e))

