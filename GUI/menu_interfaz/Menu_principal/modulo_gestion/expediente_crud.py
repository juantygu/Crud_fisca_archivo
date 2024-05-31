import tkinter as tk
import json
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import ttk
from consultas.consultas_auditor import ConsultasAuditor
from consultas.consultas_expediente import ConsultasExpediente
from consultas.consultas_proceso import ConsultasProceso
from entidades.expediente import Expediente
import re


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
        self.auditor = ConsultasAuditor()
        self.proceso = ConsultasProceso()
        self.elementos.ventana_credenciales_abierta = False
        self.dic_auditores = {} # Diccionario para almacenar id_auditor: nombre_auditor
        self.dic_procesos = {} # Diccionario para almacenar id_proceso: nombre_proceso

        self.altura_pantalla = self.interfaz.window_height
        self.ancho_pantalla = self.interfaz.window_width

    def mostrar_expediente_crud(self):
        """
                        Método para mostrar la interfaz de gestión de expedientes.
                        """
        self.interfaz.estado_actual = "gestion_expediente_crud"
        print(self.interfaz.estado_actual)
        opciones_estado = ["activo", "auto archivo"]
        try:
            dic_auditores = self.obtener_auditores()  # Obtener el diccionario de auditores
            dic_procesos = self.obtener_procesos() # Obtener el diccionario de procesos
            self.crear_etiqueta_informacion(dic_auditores, dic_procesos)

            if dic_auditores:
                lista_nombres_auditores = list(dic_auditores.keys())  # Obtener solo los nombres de los auditores
            else:
                raise ValueError("error al obtener los auditores.")
            if dic_procesos:
                lista_nombres_procesos = list(dic_procesos.keys())  # Obtener solo los nombres de los procesos
            else :
                raise ValueError("error al obtener los procesos.")

            # ==== TITULO ======
            self.elementos.label_titulo = tk.Label(self.ventana_principal, text="GESTIÓN DE EXPEDIENTES",
                                                   font=("Arial", 25, "bold"), fg="black", bg="#E6F7FF")

            self.elementos.label_titulo.pack(pady=10)  # pady añade un espacio en la parte inferior de la etiqueta
            # ====LABEL IFRAME====
            self.elementos.label_frame = tk.LabelFrame(self.ventana_principal, text="DATOS DEL EXPEDIENTE",
                                                       font=("Arial", 16, "bold"), fg="black", bg="#E6F7FF", bd=5,
                                                       relief=tk.RIDGE)
            self.elementos.label_frame.place(x=30, y=80, width=450, height= 400)

            # =========== ETIQUETA ID_EXPEDIENTE =============
            self.elementos.label_id_expediente = tk.Label(self.elementos.label_frame, text="ID_expediente",
                                                             font=("Arial", 11, "bold"),
                                                             fg="black", bg="#E6F7FF")
            self.elementos.label_id_expediente.place(x=20, y=10)

            # =====CAJA ID_expediente =========
            self.elementos.box_id_expediente = tk.Entry(self.elementos.label_frame,
                                                           textvariable=self.elementos.id_variable_expediente, bd=1,
                                                           font=("Arial", 10), width=12, insertbackground="blue",
                                                           selectbackground="blue",
                                                           relief=tk.SOLID)
            self.elementos.box_id_expediente.place(x=150, y=10)
            self.elementos.box_id_expediente.delete(0, tk.END)

            # ======== ETIQUETA ID_CONTRIBUYENTE ==============
            self.elementos.label_id_contribuyente = tk.Label(self.elementos.label_frame, text="ID_contribuyente",
                                                             font=("Arial", 11, "bold"),
                                                             fg="black", bg="#E6F7FF")
            self.elementos.label_id_contribuyente.place(x=20, y=50)

            # =====CAJA ID_Contribuyente =========
            self.elementos.box_id_contribuyente = tk.Entry(self.elementos.label_frame,
                                                           textvariable=self.elementos.id_variable_contribuyente, bd=1,
                                                           font=("Arial", 10), width=12, insertbackground="blue",
                                                           selectbackground="blue",
                                                           relief=tk.SOLID)
            self.elementos.box_id_contribuyente.place(x=150, y=50)
            self.elementos.box_id_contribuyente.delete(0, tk.END)

            # ===== ETIQUETA ID_Auditor ======
            self.elementos.label_id_auditor = tk.Label(self.elementos.label_frame, text="ID_auditor",
                                                       font=("Arial", 11, "bold"),
                                                       fg="black", bg="#E6F7FF")
            self.elementos.label_id_auditor.place(x=20, y=90)

            # ===== COMBOBOX Auditor =========
            self.elementos.box_id_auditor = ttk.Combobox(self.elementos.label_frame,
                                                              values=lista_nombres_auditores,
                                                              textvariable=self.elementos.id_variable_auditor,
                                                              font=("Arial", 10),
                                                              width=11, style="EstiloCombobox.TCombobox")
            self.elementos.box_id_auditor.place(x=150, y=90)

            # =====ETIQUETA ID_proceso ======
            self.elementos.label_id_proceso = tk.Label(self.elementos.label_frame, text="ID_proceso",
                                                       font=("Arial", 11, "bold"),
                                                       fg="black", bg="#E6F7FF")
            self.elementos.label_id_proceso.place(x=20, y=130)

            # ===== COMBOBOX ID_proceso =========
            self.elementos.box_id_proceso = ttk.Combobox(self.elementos.label_frame,
                                                              values=lista_nombres_procesos,
                                                              textvariable=self.elementos.id_variable_proceso,
                                                              font=("Arial", 10),
                                                              width=11)
            self.elementos.box_id_proceso.place(x=150, y=130)


            # =====ETIQUETA ID_caja ======
            self.elementos.label_id_caja = tk.Label(self.elementos.label_frame, text="ID_caja",
                                                        font=("Arial", 11, "bold"),
                                                        fg="black", bg="#E6F7FF")
            self.elementos.label_id_caja.place(x=20, y=170)
            # =====CAJA ID_caja =========
            self.elementos.box_id_caja = tk.Entry(self.elementos.label_frame,
                                                      textvariable=self.elementos.id_variable_caja, bd=1,
                                                      font=("Arial", 10), width=12, insertbackground="blue",
                                                      selectbackground="blue",
                                                      relief=tk.SOLID)
            self.elementos.box_id_caja.place(x=150, y=170)
            self.elementos.box_id_caja.delete(0, tk.END)

            # =====ETIQUETA ESTADO ======
            self.elementos.label_estado = tk.Label(self.elementos.label_frame, text="Estado",
                                                    font=("Arial", 11, "bold"),
                                                    fg="black", bg="#E6F7FF")
            self.elementos.label_estado.place(x=20, y=210)
            # ===== COMBOBOX ESTADO =========
            self.elementos.box_estado = ttk.Combobox(self.elementos.label_frame,
                                                              values=opciones_estado,
                                                              textvariable=self.elementos.estado_variable,
                                                              font=("Arial", 10),
                                                              width=11)
            self.elementos.box_estado.place(x=150, y=210)

            # =====ETIQUETA año gravable ======
            self.elementos.label_año_gravable = tk.Label(self.elementos.label_frame, text="Años gravables",
                                                   font=("Arial", 11, "bold"),
                                                   fg="black", bg="#E6F7FF")
            self.elementos.label_año_gravable.place(x=20, y=250)
            # =====CAJA año gravable =========
            self.elementos.box_año_gravable = tk.Entry(self.elementos.label_frame,
                                                 textvariable=self.elementos.año_gravable_variable, bd=1,
                                                 font=("Arial", 10), width=6, insertbackground="blue",
                                                 selectbackground="blue",
                                                 relief=tk.SOLID)
            self.elementos.box_año_gravable.place(x=150, y=250)
            self.elementos.box_año_gravable.delete(0, tk.END)
            # =====CAJA año gravable 1 ======
            self.elementos.box_año_gravable_1 = tk.Entry(self.elementos.label_frame,
                                                       textvariable=self.elementos.año_gravable_1_variable, bd=1,
                                                       font=("Arial", 10), width=6, insertbackground="blue",
                                                       selectbackground="blue",
                                                       relief=tk.SOLID)
            self.elementos.box_año_gravable_1.place(x=210, y=250)
            self.elementos.box_año_gravable_1.delete(0, tk.END)
            # =====CAJA año gravable 2 ======
            self.elementos.box_año_gravable_2 = tk.Entry(self.elementos.label_frame,
                                                         textvariable=self.elementos.año_gravable_2_variable, bd=1,
                                                         font=("Arial", 10), width=6, insertbackground="blue",
                                                         selectbackground="blue",
                                                         relief=tk.SOLID)
            self.elementos.box_año_gravable_2.place(x=270, y=250)
            self.elementos.box_año_gravable_2.delete(0, tk.END)
            # =====CAJA año gravable 3 ======
            self.elementos.box_año_gravable_3 = tk.Entry(self.elementos.label_frame,
                                                         textvariable=self.elementos.año_gravable_3_variable, bd=1,
                                                         font=("Arial", 10), width=6, insertbackground="blue",
                                                         selectbackground="blue",
                                                         relief=tk.SOLID)
            self.elementos.box_año_gravable_3.place(x=330, y=250)
            self.elementos.box_año_gravable_3.delete(0, tk.END)
            # =====CAJA año gravable 4 ======
            self.elementos.box_año_gravable_4 = tk.Entry(self.elementos.label_frame,
                                                         textvariable=self.elementos.año_gravable_4_variable, bd=1,
                                                         font=("Arial", 10), width=6, insertbackground="blue",
                                                         selectbackground="blue",
                                                         relief=tk.SOLID)
            self.elementos.box_año_gravable_4.place(x=390, y=250)
            self.elementos.box_año_gravable_4.delete(0, tk.END)


            # ====== BOTON INSERTAR =====
            self.elementos.boton_insertar = tk.Button(self.elementos.label_frame, text="Insertar",
                                                      font=("Arial", 12, "bold"),
                                                      fg="black", bg="white", bd=4, relief=tk.GROOVE, width=7, height=1,
                                                      activebackground='blue',command=self.insertar_expediente)
            self.elementos.boton_insertar.place(x=(450 - 410), y=(400 - 80))
            # ===== BOTON MODIFICAR ====
            self.elementos.boton_modificar = tk.Button(self.elementos.label_frame, text="Modificar",
                                                       font=("Arial", 12, "bold"), fg="black", bg="white", bd=4,
                                                       relief=tk.GROOVE, width=7, height=1, activebackground='blue',
                                                       command=self.modificar_expediente)
            self.elementos.boton_modificar.place(x=(450-310), y=(400-80))
            # ===== BOTON ELIMINAR =====
            self.elementos.boton_eliminar = tk.Button(self.elementos.label_frame, text="Eliminar",
                                                      font=("Arial", 12, "bold"), fg="black", bg="white", bd=4,
                                                      relief=tk.GROOVE, width=7, height=1, activebackground='blue',
                                                      command=self.eliminar_expediente)
            self.elementos.boton_eliminar.place(x=(450-210), y=(400-80))

            # ====BOTON LIMPIAR CAJA ========
            self.elementos.boton_limpiar_cajas = tk.Button(self.elementos.label_frame, text="LIMPIAR",
                                                                    font=("Arial", 12, "bold"), fg="black", bg="white",
                                                                    bd=4,
                                                                    relief=tk.GROOVE, width=7, height=1,
                                                                    activebackground='blue',
                                                                    command= self.limpiar_cajas_texto)
            self.elementos.boton_limpiar_cajas.place(x=(450 - 110), y=(400 - 80))

            # ======BOTON CAMBIAR ID =========

            self.elementos.boton_cambiar_id = tk.Button(self.ventana_principal, text="Cambiar ID_expediente",
                                                        font=("Arial", 12, "bold"), fg="black", bg="red", bd=4,
                                                        relief=tk.GROOVE, width=20, height=1, activebackground='blue',
                                                        command= self.crear_ventana_credenciales_cambiar_id_expediente)
            self.elementos.boton_cambiar_id.place(x=55, y=500)

            # ========= BUSQUEDA POR ID_CONTRIBUYENTE =================
            # ETIQUETA BUSQUEDA
            self.elementos.label_busqueda_id_contribuyente = tk.Label(self.ventana_principal, text="BUSQUEDA POR ID_CONTRIBUYENTE",
                                                       font=("Arial", 11, "bold"),
                                                       fg="black", bg="#E6F7FF")
            self.elementos.label_busqueda_id_contribuyente.place(x=((self.ancho_pantalla / 2)-130), y=80)
            # BOX ID_CONTRIBUYENTE BUSQUEDA
            self.elementos.box_busqueda_id_contribuyente = tk.Entry(self.ventana_principal,
                                                         textvariable=self.elementos.busqueda_id_contribuyente_variable, bd=1,
                                                         font=("Arial", 10), width=12, insertbackground="blue",
                                                         selectbackground="blue",
                                                         relief=tk.SOLID)
            self.elementos.box_busqueda_id_contribuyente.place(x=((self.ancho_pantalla / 2)-130), y=110)
            self.elementos.box_busqueda_id_contribuyente.delete(0, tk.END)
            # BOTON BUSCAR
            self.elementos.boton_buscar = tk.Button(self.ventana_principal, text="BUSCAR",
                                                           font=("Arial", 10, "bold"), fg="black", bg="white",
                                                           bd=3,
                                                           relief=tk.GROOVE, width=7, height=1,
                                                           activebackground='blue',
                                                           command=self.busqueda_por_id_contribuyente)
            self.elementos.boton_buscar.place(x=((self.ancho_pantalla / 2)-30), y=108)


            # ===== TABLA ======
            # Crear Treeview

            style = ttk.Style()
            style.theme_use("alt")
            style.configure('Treeview.Heading', font=('Arial', 12, 'bold'))
            style.configure('Treeview', font=('Arial', 12))

            self.elementos.tree = ttk.Treeview(self.ventana_principal, columns=('ID_expediente', 'ID_contribuyente', 'ID_auditor','ID_proceso','ID_caja','Estado','Año gravable'),
                                               show='headings', height=10)
            self.elementos.tree.heading('ID_expediente', text='ID_expediente')
            self.elementos.tree.column('ID_expediente', width=115, anchor='center')
            self.elementos.tree.heading('ID_contribuyente', text='ID_contribuyente')
            self.elementos.tree.column('ID_contribuyente', width=135, anchor='center')
            self.elementos.tree.heading('ID_auditor', text='ID_auditor')
            self.elementos.tree.column('ID_auditor', width=100, anchor='center')
            self.elementos.tree.heading('ID_proceso', text='ID_proceso')
            self.elementos.tree.column('ID_proceso', width=110, anchor='center')
            self.elementos.tree.heading('ID_caja', text='ID_caja')
            self.elementos.tree.column('ID_caja', width=100, anchor='center')
            self.elementos.tree.heading('Estado', text='Estado')
            self.elementos.tree.column('Estado', width=110, anchor='center')
            self.elementos.tree.heading('Año gravable', text='Año gravable')
            self.elementos.tree.column('Año gravable', width=115, anchor='center')


            self.elementos.tree.place(x=((self.ancho_pantalla / 2)-130), y=150)
            #  =======MOSTRAR DATOS  ===========
            self.actualizar_tree_expediente()
            # Enlace del evento para seleccionar registros
            self.elementos.tree.bind("<<TreeviewSelect>>", self.selecionar_registro_expediente)

            # Boton atras
            self.elementos.boton_atras = tk.Button(self.ventana_principal, text="ATRAS", font=("Arial", 12, "bold"),
                                                   fg="black", bg="white", bd=4, relief=tk.GROOVE, width=15, height=2,
                                                   command=self.interfaz.atras)
            self.elementos.boton_atras.place(x=(self.ancho_pantalla - 250), y=(self.altura_pantalla - 150))

        except ValueError as error:
            # Verificar si el error es debido a un no dígito en id_auditor
            if "error al obtener los auditores." in str(error):
                messagebox.showerror("Error", "error al obtener los auditores.")
            if "error al obtener los procesos." in str(error):
                messagebox.showerror("Error", "error al obtener los procesos.")
        except Exception as e:
            # Si ocurre algún error, imprime un mensaje de error
            print("Error al mostrar gestion auditor:", str(e))

    def obtener_auditores(self):

        mensaje, auditores = self.auditor.mostrar_nombre_id_auditores()
        if auditores:
            #print(mensaje)
            self.dic_auditores= {auditor[0]: auditor[1] for auditor in auditores}
            #print(dic_auditores)
            return self.dic_auditores
        else:
            print(mensaje)
            return None

    def crear_etiqueta_informacion(self,dic_auditores, dic_procesos):
        # ====LABEL INFO====
        self.elementos.label_info = tk.LabelFrame(self.ventana_principal, text="INFORMACIÓN",
                                                   font=("Arial", 16, "bold"), fg="black", bg="#E6F7FF", bd=5,
                                                   relief=tk.RIDGE)
        self.elementos.label_info.place(x=((self.ancho_pantalla / 2)-130), y=415, width=400, height=250)

        # =====INFO AUDITORES =====
        auditores_texto = "\n".join([f"{id_auditor} = {nombre_auditor}" for id_auditor, nombre_auditor in dic_auditores.items()])
        self.elementos.label_info_auditores = tk.Label(self.elementos.label_info, text=auditores_texto, font=("Arial", 10, "bold"),bg="#E6F7FF", justify="left")
        self.elementos.label_info_auditores.place(x=((400/2)-180), y=10)

        # =====INFO PROCESOS =====
        procesos_texto = "\n".join([f"{id_proceso} = {nombre_proceso}" for id_proceso, nombre_proceso in dic_procesos.items()])
        self.elementos.label_info_procesos = tk.Label(self.elementos.label_info, text=procesos_texto, font=("Arial", 10, "bold"), bg="#E6F7FF", justify="left")
        self.elementos.label_info_procesos.place(x=((400 / 2) + 10), y=10)

    def obtener_procesos(self):

        mensaje, procesos = self.proceso.mostrar_nombre_id_procesos()
        if procesos:
            #print(mensaje)
            self.dic_procesos= {proceso[0]: proceso[1] for proceso in procesos}
            #print(dic_procesos)
            return self.dic_procesos
        else:
            print(mensaje)
            return None

    def busqueda_por_id_contribuyente(self):
        """
                        Método para buscar por id_contribuyente.
                        """
        id_contribuyente = self.elementos.box_busqueda_id_contribuyente.get().strip()

        if id_contribuyente:
            try:
                if id_contribuyente[0] not in "0123456789":
                    raise ValueError("ID del contribuyente debe comenzar con un numero.")
                mensaje, contribuyentes = self.consultas_expediente.buscar_por_id_contribuyente(id_contribuyente)

                if contribuyentes:
                    print(mensaje)
                    try:
                        # actualizamos los campos del tree
                        self.elementos.tree.delete(*self.elementos.tree.get_children())

                        # insertar lo nuevos datos  en el tree
                        # mostrar datos en la tabla
                        for row in contribuyentes:
                            self.elementos.tree.insert("", "end", values=row)
                    except Exception as update_error:
                        messagebox.showerror("Error", f"Error al actualizar la tabla: {update_error}")
                        print(f"Error al actualizar la tabla: {update_error}")
                else:
                    messagebox.showinfo("INFORMACIÓN", mensaje)
                    print(mensaje)
            except ValueError as error:
                if "ID del contribuyente debe comenzar con un numero." in str(error):

                    messagebox.showerror("Error", "ID del contribuyente debe comenzar con un numero.")
                    # Borrar el contenido de la caja de texto id_auditor

                # Verificar si el error es debido a la conexión a la base de datos
                elif "Error al conectar a la base de datos" in str(error):
                    messagebox.showerror("Error de conexión", "No se pudo conectar a la base de datos.")
                else:
                    messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Error", "Todas las cajas de texto deben tener un valor.")


    def actualizar_tree_expediente(self):
        """
                Método para actualizar la tabla de expedientes en la interfaz gráfica.
                """
        try:
            #borrar elementos actuales del tree contribuyente
            # devuelve una lista de identificadores de elementos secundarios
            # , y el operador * se utiliza para pasar esos identificadores
            # como argumentos separados a la función delete.
            self.elementos.tree.delete(*self.elementos.tree.get_children())

        #obtener los nuevos datos que deseamos mostrar
            expedientes = self.consultas_expediente.obtener_ultimo_expediente()
            #print(contribuyentes)
        #insertar lo nuevos datos  en el tree
            # mostrar datos en la tabla
            for row in expedientes[1]:
                self.elementos.tree.insert("", "end", values=row)
        except ValueError as error:
            print(f"fError al actualizar tabla : {error}")

    def selecionar_registro_expediente(self, event):
        """
                Método para seleccionar un registro de la tabla de expedientes.

                Args:
                    event: Evento que activa la selección de un registro.
                """
        try:
            itemseleccionado = self.elementos.tree.focus()
            if itemseleccionado:
                self.elementos.box_id_expediente.config(state=tk.NORMAL)
                self.elementos.box_año_gravable.config(state=tk.NORMAL)
                #obtener valores
                values = self.elementos.tree.item(itemseleccionado)['values']
                #establecer los valores en los widgests entry
                self.elementos.box_id_expediente.delete(0, tk.END)
                self.elementos.box_id_expediente.insert(0, values[0])
                self.elementos.box_id_contribuyente.delete(0, tk.END)
                self.elementos.box_id_contribuyente.insert(0, values[1])
                self.elementos.box_id_auditor.delete(0, tk.END)
                self.elementos.box_id_auditor.set(values[2])
                self.elementos.box_id_proceso.delete(0, tk.END)
                self.elementos.box_id_proceso.set(values[3])
                self.elementos.box_id_caja.delete(0, tk.END)
                self.elementos.box_id_caja.insert(0, values[4])
                self.elementos.box_estado.delete(0, tk.END)
                self.elementos.box_estado.set(values[5])
                self.elementos.box_año_gravable.delete(0, tk.END)
                self.elementos.box_año_gravable.insert(0, values[6])

                # Deshabilitar el botón "Insertar" y self.elementos.box_id
                self.elementos.boton_insertar.config(state=tk.DISABLED)
                self.elementos.box_id_expediente.config(state=tk.DISABLED)
                self.elementos.box_año_gravable.config(state=tk.DISABLED)

        except ValueError as error:
            print(f"fError al seleccionar registro : {error}")

    def limpiar_cajas_texto(self):
        """
                Método para limpiar las cajas de texto en la interfaz gráfica.
                """
        # Verificar si el botón "Insertar" y la entrada box_id están deshabilitados
        if self.elementos.boton_insertar['state'] == tk.DISABLED and self.elementos.box_id_expediente['state'] == tk.DISABLED:

            # Habilitar el botón "Insertar" y la entrada box_id
            self.elementos.boton_insertar.config(state=tk.NORMAL)
            self.elementos.box_id_expediente.config(state=tk.NORMAL)
            self.elementos.box_año_gravable.config(state=tk.NORMAL)

        self.elementos.box_id_expediente.delete(0, tk.END)
        self.elementos.box_id_contribuyente.delete(0, tk.END)
        self.elementos.box_id_auditor.delete(0, tk.END)
        self.elementos.box_id_proceso.delete(0, tk.END)
        self.elementos.box_id_caja.delete(0, tk.END)
        self.elementos.box_estado.delete(0, tk.END)
        self.elementos.box_año_gravable.delete(0, tk.END)
        self.elementos.box_año_gravable_1.delete(0, tk.END)
        self.elementos.box_año_gravable_2.delete(0, tk.END)
        self.elementos.box_año_gravable_3.delete(0, tk.END)
        self.elementos.box_año_gravable_4.delete(0, tk.END)
        self.elementos.box_busqueda_id_contribuyente.delete(0, tk.END)

    def verificar_años_gravables(self, años_gravables):
        """
        Verifica si los elementos de la lista de años gravables son válidos.
        Un año es válido si comienza con "20" y tiene exactamente cuatro dígitos.
        Retorna un mensaje y True si todos los elementos son válidos, de lo contrario,
        retorna un mensaje indicando los años inválidos y False.
        """
        pattern = re.compile(r"^20\d{2}$")
        errores = []

        for año in años_gravables:
            if not pattern.match(año):
                if not re.match(r"^\d{4}$", año):
                    errores.append(f"El año '{año}'debe tener exactamente cuatro dígitos")
                elif not re.match(r"^20", año):
                    errores.append(f"El año '{año}' debe empezar con '20' ")
                else:
                    errores.append(f"El año '{año}' tiene un formato inválido")

        if errores:
            return "\n".join(errores), False
        return "Todos los años son válidos", True

    def insertar_expediente(self):
        """
                Método para insertar un nuevo expediente en la base de datos.
                """
        id_expediente = self.elementos.box_id_expediente.get().strip()
        id_contribuyente = self.elementos.box_id_contribuyente.get().strip()
        id_auditor = self.elementos.box_id_auditor.get().strip()
        id_proceso = self.elementos.box_id_proceso.get().strip()
        id_caja = self.elementos.box_id_caja.get().strip()
        estado = self.elementos.box_estado.get().strip()
        años_gravables = [self.elementos.box_año_gravable.get().strip(),
                          self.elementos.box_año_gravable_1.get().strip(),
                          self.elementos.box_año_gravable_2.get().strip(),
                          self.elementos.box_año_gravable_3.get().strip(),
                          self.elementos.box_año_gravable_4.get().strip()]

        # Eliminar años gravables vacíos de la lista
        años_gravables = [año for año in años_gravables if año]

        if id_expediente and id_contribuyente and id_auditor and id_proceso and id_caja and estado and años_gravables:
            try:
                mensaje_ano, confirmacion_ano = self.verificar_años_gravables(años_gravables)

                if id_expediente[0].upper() not in ['O', 'I', 'S']:
                    raise ValueError("ID del expediente debe empezar por O o I o S")
                elif id_contribuyente[0] not in "0123456789":
                    raise ValueError("ID del contribuyente debe comenzar con un numero.")
                elif id_auditor[0].upper() != "A":
                    raise ValueError("ID del auditor debe comenzar con A .")
                elif id_proceso not in "12345":
                    raise ValueError("id_proceso debe ser un numero.")
                elif id_caja[0].upper() not in ['O', 'I', 'S']:
                    raise ValueError("ID caja debe empezar por O o I o S")
                elif estado not in ["activo","auto archivo"]:
                    raise ValueError("el estado debe ser activo o auto archivo")
                elif not confirmacion_ano:
                    raise ValueError(mensaje_ano)

                mensaje, confirmacion = self.expediente.insertar_expediente(id_expediente, id_contribuyente, id_auditor,
                                                                            id_proceso,id_caja, estado, años_gravables)

                if confirmacion:
                    messagebox.showinfo("INFORMACIÓN", "El Expediente fue agregado correctamente")
                    print(mensaje)
                    # actualizamos los campos del tree
                    self.actualizar_tree_expediente()
                    # LIMPIAR CAMPOS
                    self.limpiar_cajas_texto()
                else:
                    messagebox.showinfo("INFORMACIÓN", mensaje)
                    print(mensaje)

            except ValueError as error:
                # Verificar si el error es debido a un no dígito en id_auditor
                if "ID del contribuyente debe comenzar con un numero." in str(error):

                    messagebox.showerror("Error", "ID del contribuyente debe comenzar con un numero.")
                    # Borrar el contenido de la caja de texto id_auditor

                # Verificar si el error es debido a la conexión a la base de datos
                elif "Error al conectar a la base de datos" in str(error):
                    messagebox.showerror("Error de conexión", "No se pudo conectar a la base de datos.")
                else:
                    messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Error", "Todas las cajas de texto deben tener un valor.")

    def eliminar_expediente(self):
        """
                Método para eliminar un expediente de la base de datos.
                """
        id_expediente = self.elementos.box_id_expediente.get().strip()
        año_gravable = [self.elementos.box_año_gravable.get().strip()]

        # Verificar si ambas cajas de texto tienen un valor
        if id_expediente and año_gravable:
            try:
                mensaje_ano, confirmacion_ano = self.verificar_años_gravables(año_gravable)
                if id_expediente[0].upper() not in ['O', 'I', 'S']:
                    raise ValueError("ID del expediente debe empezar por O o I o S")
                elif not confirmacion_ano:
                    raise ValueError(mensaje_ano)

                mensaje , confirmacion = self.expediente.eliminar_expediente_por_ano(id_expediente,año_gravable[0])

                if confirmacion:
                    messagebox.showinfo("INFORMACIÓN", "los datos fueron Elimninados")
                    print(mensaje)
                else:
                    messagebox.showinfo("INFORMACIÓN", mensaje)
                    print(mensaje)

                # actualizamos los campos del tree
                self.actualizar_tree_expediente()
                # LIMPIAR CAMPOS
                self.limpiar_cajas_texto()
            except ValueError as error:
                # Verificar si el error es debido a un no dígito en id_auditor
                if "ID del expediente debe empezar por O o I o S" in str(error):

                    messagebox.showerror("Error", "ID del expediente debe empezar por O o I o S")
                    # Borrar el contenido de la caja de texto id_auditor
                elif "los años deben empezar por 20" in str(error):

                    messagebox.showerror("Error", "los años deben empezar por 20")

                # Verificar si el error es debido a la conexión a la base de datos
                elif "Error al conectar a la base de datos" in str(error):
                    messagebox.showerror("Error de conexión", "No se pudo conectar a la base de datos.")
                else:
                    messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Error", "la caja de texto id_expediente y año gravable debe tener un valor.")

    def modificar_expediente(self):
        """
                Método para eliminar un expediente de la base de datos.
                """
        id_expediente = self.elementos.box_id_expediente.get().strip()
        nuevo_id_contribuyente = self.elementos.box_id_contribuyente.get().strip()
        nuevo_id_auditor = self.elementos.box_id_auditor.get().strip()
        nuevo_id_proceso = self.elementos.box_id_proceso.get().strip()
        nuevo_id_caja = self.elementos.box_id_caja.get().strip()
        nuevo_estado = self.elementos.box_estado.get().strip()
        año_gravable = [self.elementos.box_año_gravable.get().strip()]
        #print(año_gravable[0])


        # Verificar si ambas cajas de texto tienen un valor
        if id_expediente and nuevo_id_contribuyente and nuevo_id_auditor and nuevo_id_proceso and nuevo_id_caja and nuevo_estado and año_gravable:
            try:
                mensaje_ano, confirmacion_ano = self.verificar_años_gravables(año_gravable)
                if id_expediente[0].upper() not in ['O', 'I', 'S']:
                    raise ValueError("ID del expediente debe empezar por O o I o S")
                elif nuevo_id_contribuyente[0] not in "0123456789":
                    raise ValueError("ID del contribuyente debe comenzar con un numero.")
                elif nuevo_id_auditor[0].upper() != "A":
                    raise ValueError("ID del auditor debe comenzar con A .")
                elif nuevo_id_proceso not in "12345":
                    raise ValueError("id_proceso debe ser un numero.")
                elif nuevo_id_caja[0].upper() not in ['O', 'I', 'S']:
                    raise ValueError("ID caja debe empezar por O o I o S")
                elif nuevo_estado not in ["activo","auto archivo"]:
                    raise ValueError("el estado debe ser activo o auto archivo")
                elif not confirmacion_ano:
                    raise ValueError(mensaje_ano)

                mensaje, confirmacion = self.expediente.modificar_datos_expediente(id_expediente, nuevo_id_contribuyente,
                                                                                   nuevo_id_auditor,nuevo_id_proceso,
                                                                                   nuevo_id_caja,nuevo_estado,año_gravable[0])

                if confirmacion:
                    messagebox.showinfo("INFORMACIÓN", "los datos fueron Actualizados")
                    print(mensaje)
                else:
                    messagebox.showinfo("INFORMACIÓN", mensaje)
                    print(mensaje)

                # actualizamos los campos del tree
                self.actualizar_tree_expediente()
                # LIMPIAR CAMPOS
                self.limpiar_cajas_texto()

            except ValueError as error:
                # Verificar si el error es debido a un no dígito en id_auditor
                if "la cedula del auditor debe contener solo números" in str(error):

                    messagebox.showerror("Error", "la cedula del auditor debe contener solo números.")
                    # Borrar el contenido de la caja de texto id_auditor

                # Verificar si el error es debido a la conexión a la base de datos
                elif "Error al conectar a la base de datos" in str(error):
                    messagebox.showerror("Error de conexión", "No se pudo conectar a la base de datos.")
                else:
                    messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Error", "Todas las cajas de texto deben tener un valor.")

    def modificar_id_expediente(self):
        """
                Método para modificar el ID de un expediente en la base de datos.
                """
        id_antiguo = self.elementos.box_antiguo_id.get().strip()
        id_nuevo = self.elementos.box_nuevo_id.get().strip()
        print(id_antiguo, id_nuevo)
        # Verificar si ambas cajas de texto tienen un valor
        if id_antiguo and id_nuevo:
            try:
                if id_antiguo[0].upper() not in ['O', 'I', 'S']:
                    raise ValueError("El antiguo ID debe comenzar por O o I o S.")
                if id_antiguo[0].upper() not in ['O', 'I', 'S']:
                    raise ValueError("El nuevo ID comenzar por O o I o S.")
                mensaje, confirmacion = self.expediente.modificar_id_expediente(id_antiguo, id_nuevo)

                if confirmacion:
                    messagebox.showinfo("INFORMACIÓN", "los datos fueron Actualizados")
                    print(mensaje)
                else:
                    messagebox.showinfo("INFORMACIÓN", mensaje)
                    print(mensaje)

                # actualizamos los campos del tree
                self.actualizar_tree_expediente()
                # LIMPIAR CAMPOS
                self.limpiar_cajas_texto()

            except ValueError as error:
                # Verificar si el error es debido a un no dígito en id_auditor
                if "El antiguo ID debe comenzar por O o I o S." in str(error):

                    messagebox.showerror("Error", "El antiguo ID debe comenzar por O o I o S.")
                    # Borrar el contenido de la caja de texto id_auditor
                elif"El nuevo ID comenzar por O o I o S" in str(error):

                    messagebox.showerror("Error", "El nuevo ID comenzar por O o I o S.")
                    # Borrar el contenido de la caja de texto id_auditor
                # Verificar si el error es debido a la conexión a la base de datos
                elif "Error al conectar a la base de datos" in str(error):
                    messagebox.showerror("Error de conexión", "No se pudo conectar a la base de datos.")
                else:
                    messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Error", "Todas las cajas de texto deben tener un valor.")

    def cambiar_id_expiente(self):
        """
                Método que muestra los elementos para cambiar el id expediente .
                """
        self.interfaz.estado_actual = "g_e_c_cambiar_id_expediente" # gestion_expediente_crud
        print(self.interfaz.estado_actual)

        # desabilitar botones y cajas
        self.elementos.boton_insertar.config(state=tk.DISABLED)
        self.elementos.boton_eliminar.config(state=tk.DISABLED)
        self.elementos.boton_modificar.config(state=tk.DISABLED)
        self.elementos.boton_limpiar_cajas.config(state=tk.DISABLED)
        self.elementos.boton_atras.config(state=tk.DISABLED)

        self.elementos.box_id_expediente.config(state=tk.DISABLED)
        self.elementos.box_id_contribuyente.config(state=tk.DISABLED)
        self.elementos.box_id_auditor.config(state=tk.DISABLED)
        self.elementos.box_id_proceso.config(state=tk.DISABLED)
        self.elementos.box_id_caja.config(state=tk.DISABLED)
        self.elementos.box_estado.config(state=tk.DISABLED)
        self.elementos.box_año_gravable.config(state=tk.DISABLED)
        self.elementos.box_año_gravable_1.config(state=tk.DISABLED)
        self.elementos.box_año_gravable_2.config(state=tk.DISABLED)
        self.elementos.box_año_gravable_3.config(state=tk.DISABLED)
        self.elementos.box_año_gravable_4.config(state=tk.DISABLED)


        # ===== ETIQUETA ANTIGUO_ID =======
        self.elementos.label_antiguo_id = tk.Label(self.ventana_principal, text="ID_antiguo", font=("Arial", 12, "bold"),
                                           fg="black", bg="#E6F7FF")
        self.elementos.label_antiguo_id.place(x=55,y=560)
        # ======CAJA ANTIGUO ID ========
        self.elementos.box_antiguo_id = tk.Entry(self.ventana_principal, textvariable=self.elementos.antiguo_id_variable,
                                             bd=3, font=("Arial", 12), width=10, insertbackground="blue",
                                             selectbackground="blue", relief=tk.RIDGE)
        self.elementos.box_antiguo_id.place(x=55, y=590)
        self.elementos.box_antiguo_id.delete(0, tk.END)

        # ===== ETIQUETA NUEVO_ID =======
        self.elementos.label_nuevo_id = tk.Label(self.ventana_principal, text="ID_nuevo",
                                                   font=("Arial", 12, "bold"),
                                                   fg="black", bg="#E6F7FF")
        self.elementos.label_nuevo_id.place(x=170, y=560)
        # ======CAJA NUEVO ID ========
        self.elementos.box_nuevo_id = tk.Entry(self.ventana_principal, textvariable=self.elementos.nuevo_id_variable,
                                                 bd=3, font=("Arial", 12), width=10, insertbackground="blue",
                                                 selectbackground="blue", relief=tk.RIDGE)
        self.elementos.box_nuevo_id.place(x=170, y=590)
        self.elementos.box_nuevo_id.delete(0, tk.END)

        # ===== BOTON ACEPTAR ======
        self.elementos.boton_aceptar = tk.Button(self.ventana_principal, text="ACEPTAR", font=("Arial", 12, "bold"),
                                               fg="black", bg="white", bd=4, relief=tk.GROOVE, width=9, height=1,
                                               command= self.modificar_id_expediente)
        self.elementos.boton_aceptar.place(x=55, y=630)

        # ====== BOTON CANCELAR =======
        self.elementos.boton_cancelar = tk.Button(self.ventana_principal, text="CANCELAR", font=("Arial", 12, "bold"),
                                                 fg="black", bg="white", bd=4, relief=tk.GROOVE, width=9, height=1,
                                                 command=self.interfaz.atras)
        self.elementos.boton_cancelar.place(x=170, y=630)

    def crear_ventana_credenciales_cambiar_id_expediente(self):
        """
                Método para crear la ventana de credenciales para cambiar el ID del expediente.
                """
        if not self.elementos.ventana_credenciales_abierta or not self.elementos.ventana_credenciales.winfo_exists():

            # desabilitar botones y cajas
            self.elementos.boton_insertar.config(state=tk.DISABLED)
            self.elementos.boton_eliminar.config(state=tk.DISABLED)
            self.elementos.boton_modificar.config(state=tk.DISABLED)
            self.elementos.boton_limpiar_cajas.config(state=tk.DISABLED)
            self.elementos.boton_atras.config(state=tk.DISABLED)

            self.elementos.box_id_expediente.config(state=tk.DISABLED)
            self.elementos.box_id_contribuyente.config(state=tk.DISABLED)
            self.elementos.box_id_auditor.config(state=tk.DISABLED)
            self.elementos.box_id_proceso.config(state=tk.DISABLED)
            self.elementos.box_id_caja.config(state=tk.DISABLED)
            self.elementos.box_estado.config(state=tk.DISABLED)
            self.elementos.box_año_gravable.config(state=tk.DISABLED)
            self.elementos.box_año_gravable_1.config(state=tk.DISABLED)
            self.elementos.box_año_gravable_2.config(state=tk.DISABLED)
            self.elementos.box_año_gravable_3.config(state=tk.DISABLED)
            self.elementos.box_año_gravable_4.config(state=tk.DISABLED)

            self.elementos.ventana_credenciales = tk.Tk()
            self.elementos.ventana_credenciales.title("Acceso administrador")
            self.elementos.ventana_credenciales.geometry("300x150")
            # Centrar la ventana en la pantalla
            inicio_width = self.elementos.ventana_credenciales.winfo_screenwidth()  # ancho de la ventana requerido gracias a la funcion .winfo_reqwidth()
            inicio_height = self.elementos.ventana_credenciales.winfo_screenheight()  # alto de la ventana requerido gracias a la funcion .winfo_reqheight()
            winicio = 300
            hinicio = 150
            inicio_position_right = int(
                inicio_width / 2 - winicio / 2)  # posicion de la ventana la funcion winfo_screenwidth() determina el ancho de la pantalla
            inicio_position_down = int(
                inicio_height / 2 - hinicio / 2)  # posicion de la ventana la funcion winfo_screenheight() determina el alto de la pantalla
            self.elementos.ventana_credenciales.geometry("+{}+{}".format(inicio_position_right,
                                                    inicio_position_down))  # los valores position_right, position_down van en los corchet

            # Agrega widgets para el usuario y la contraseña
            label_user = tk.Label(self.elementos.ventana_credenciales, text="Usuario:")
            label_user.pack()
            usuario_var = tk.StringVar(value=self.interfaz.user_admin)

            self.elementos.entry_user_admin = tk.Entry(self.elementos.ventana_credenciales, textvariable=usuario_var)
            self.elementos.entry_user_admin.pack()

            label_password = tk.Label(self.elementos.ventana_credenciales, text="Contraseña:")
            label_password.pack()
            contraseña_var = tk.StringVar(value=self.interfaz.password_admin)

            self.elementos.entry_password_admin = tk.Entry(self.elementos.ventana_credenciales, show="*",
                                                     textvariable=contraseña_var)  # Muestra asteriscos para la contraseña
            self.elementos.entry_password_admin.pack()

            # Crea un botón para iniciar sesión
            login_button = tk.Button(self.elementos.ventana_credenciales, text="Iniciar Sesión", command=lambda: self.interfaz.verificar_credenciales("gestion_expediente_crud"))
            login_button.pack()
            # Después de crear la ventana, establece la bandera a True
            self.elementos.ventana_credenciales_abierta = True
            self.elementos.ventana_credenciales.protocol("WM_DELETE_WINDOW", self.cerrar_ventana_credenciales_expediente)
        else:
            self.elementos.ventana_credenciales.focus_force()  # Enfoca la ventana existente para mostrarla en la parte delantera

    def cerrar_ventana_credenciales_expediente(self):
        """
                Método para cerrar la ventana de credenciales de auditor.
                """
        # Manejar el cierre de la ventana
        self.elementos.ventana_credenciales.destroy()
        self.elementos.ventana_credenciales_abierta = False  # Establecer la variable a None después de destruir la ventana

        # habilitar botones y cajas
        self.elementos.boton_insertar.config(state=tk.NORMAL)
        self.elementos.boton_eliminar.config(state=tk.NORMAL)
        self.elementos.boton_modificar.config(state=tk.NORMAL)
        self.elementos.boton_limpiar_cajas.config(state=tk.NORMAL)
        self.elementos.boton_atras.config(state=tk.NORMAL)

        self.elementos.box_id_expediente.config(state=tk.NORMAL)
        self.elementos.box_id_contribuyente.config(state=tk.NORMAL)
        self.elementos.box_id_auditor.config(state=tk.NORMAL)
        self.elementos.box_id_proceso.config(state=tk.NORMAL)
        self.elementos.box_id_caja.config(state=tk.NORMAL)
        self.elementos.box_estado.config(state=tk.NORMAL)
        self.elementos.box_año_gravable.config(state=tk.NORMAL)
        self.elementos.box_año_gravable_1.config(state=tk.NORMAL)
        self.elementos.box_año_gravable_2.config(state=tk.NORMAL)
        self.elementos.box_año_gravable_3.config(state=tk.NORMAL)
        self.elementos.box_año_gravable_4.config(state=tk.NORMAL)











