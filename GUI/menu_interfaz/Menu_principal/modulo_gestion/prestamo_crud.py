import tkinter as tk
import json
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from entidades.prestamo import Prestamo
from consultas.consultas_prestamo import ConsultasPrestamo
from consultas.consultas_proceso import ConsultasProceso
from consultas.consultas_expediente import ConsultasExpediente
import re


class PrestamoCrud:

    def __init__(self,ventana_principal, elementos, interfaz):
        """
                Constructor de la clase ContribuyenteCrud.

                Args:
                    ventana_principal: La ventana principal de la interfaz gráfica.
                    elementos: Objeto que contiene los elementos de la interfaz gráfica.
                    interfaz: Objeto que representa la interfaz gráfica en general.
                """
        self.ventana_principal = ventana_principal
        self.elementos = elementos
        self.interfaz = interfaz
        self.consultas_prestamo = ConsultasPrestamo()
        self.prestamo = Prestamo()
        self.consultas_proceso = ConsultasProceso()
        self.consultas_expediente = ConsultasExpediente()
        self.elementos.ventana_credenciales_abierta = False
        self.altura_pantalla = self.interfaz.window_height
        self.ancho_pantalla = self.interfaz.window_width
        self.dic_procesos = {}  # Diccionario para almacenar id_proceso: nombre_proceso
        self.ids_validos = []
        self.ids_invalidos = []
        self.opciones_area = ["Fiscalización", "Impuestos", "Tesoreria", "Asesoría externa", "Hacienda", "Alcaldia"]

    def mostrar_prestamo_crud(self):
        """
                        Método para mostrar la interfaz de gestión de prestamo.
                        """
        self.interfaz.estado_actual = "gestion_prestamo_crud"
        print(self.interfaz.estado_actual)

        try:
            altura_pantalla = self.interfaz.window_height
            ancho_pantalla = self.interfaz.window_width

            dic_procesos = self.obtener_procesos()  # Obtener el diccionario de procesos
            if dic_procesos:

                lista_nombres_procesos = [f"{k}: {v}" for k, v in dic_procesos.items()]
            else:
                raise ValueError("error al obtener los procesos.")

            # ==== TITULO ======
            self.elementos.label_titulo = tk.Label(self.ventana_principal, text="GESTIÓN DE PRESTAMOS",
                                                   font=("Arial", 15, "bold"), fg="black", bg="#E6F7FF",bd=1)

            self.elementos.label_titulo.pack(pady=20)  # pady añade un espacio en la parte inferior de la etiqueta

            self.mostrar_hacer_prestamo()

            self.mostrar_finalizar_prestamo()

            # ====== ETIQUETA BUSQUEDA EXPEDIENTES =========
            self.elementos.label_busqueda_id_expediente = tk.Label(self.ventana_principal, text="Ingrese los NIT/CC de los contribuyentes que desea buscar",
                                                        font=("Arial", 12, "bold"),
                                                        fg="black", bg="#E6F7FF")
            self.elementos.label_busqueda_id_expediente.place(x=20, y=60)

            # ======= text expedientes=====
            self.elementos.text_busqueda_id_expediente = tk.Text(self.ventana_principal, width=133, height=4
                                                                   , fg='black', font=('Arial', 8))
            self.elementos.text_busqueda_id_expediente.place(x=20, y=90)

            # =====ETIQUETA ID_proceso ======
            self.elementos.label_id_proceso = tk.Label(self.ventana_principal, text="Seleccione el proceso",
                                                       font=("Arial", 11, "bold"),
                                                       fg="black", bg="#E6F7FF")
            self.elementos.label_id_proceso.place(x=20, y=155)

            # ===== COMBOBOX ID_proceso =========
            self.elementos.box_id_proceso = ttk.Combobox(self.ventana_principal,
                                                         values=lista_nombres_procesos,
                                                         textvariable=self.elementos.id_variable_proceso,
                                                         font=("Arial", 10),
                                                         width=11,state='readonly')
            self.elementos.box_id_proceso.place(x=200, y=155)

            # =====ETIQUETA año gravable ======
            self.elementos.label_año_gravable = tk.Label(self.ventana_principal, text="Años gravables",
                                                         font=("Arial", 11, "bold"),
                                                         fg="black", bg="#E6F7FF")
            self.elementos.label_año_gravable.place(x=315, y=155)
            # =====CAJA año gravable =========
            self.elementos.box_año_gravable = tk.Entry(self.ventana_principal,
                                                       textvariable=self.elementos.año_gravable_variable, bd=1,
                                                       font=("Arial", 10), width=6, insertbackground="blue",
                                                       selectbackground="blue",
                                                       relief=tk.SOLID)
            self.elementos.box_año_gravable.place(x=440, y=155)
            self.elementos.box_año_gravable.delete(0, tk.END)
            # =====CAJA año gravable 1 ======
            self.elementos.box_año_gravable_1 = tk.Entry(self.ventana_principal,
                                                         textvariable=self.elementos.año_gravable_1_variable, bd=1,
                                                         font=("Arial", 10), width=6, insertbackground="blue",
                                                         selectbackground="blue",
                                                         relief=tk.SOLID)
            self.elementos.box_año_gravable_1.place(x=490, y=155)
            self.elementos.box_año_gravable_1.delete(0, tk.END)
            # =====CAJA año gravable 2 ======
            self.elementos.box_año_gravable_2 = tk.Entry(self.ventana_principal,
                                                         textvariable=self.elementos.año_gravable_2_variable, bd=1,
                                                         font=("Arial", 10), width=6, insertbackground="blue",
                                                         selectbackground="blue",
                                                         relief=tk.SOLID)
            self.elementos.box_año_gravable_2.place(x=540, y=155)
            self.elementos.box_año_gravable_2.delete(0, tk.END)
            # =====CAJA año gravable 3 ======
            self.elementos.box_año_gravable_3 = tk.Entry(self.ventana_principal,
                                                         textvariable=self.elementos.año_gravable_3_variable, bd=1,
                                                         font=("Arial", 10), width=6, insertbackground="blue",
                                                         selectbackground="blue",
                                                         relief=tk.SOLID)
            self.elementos.box_año_gravable_3.place(x=590, y=155)
            self.elementos.box_año_gravable_3.delete(0, tk.END)
            # =====CAJA año gravable 4 ======
            self.elementos.box_año_gravable_4 = tk.Entry(self.ventana_principal,
                                                         textvariable=self.elementos.año_gravable_4_variable, bd=1,
                                                         font=("Arial", 10), width=6, insertbackground="blue",
                                                         selectbackground="blue",
                                                         relief=tk.SOLID)
            self.elementos.box_año_gravable_4.place(x=640, y=155)
            self.elementos.box_año_gravable_4.delete(0, tk.END)

            # ====== BOTON BUSCAR =====
            self.elementos.boton_buscar = tk.Button(self.ventana_principal, text="Buscar",
                                                       font=("Arial", 10, "bold"),
                                                       fg="black", bg="white", bd=4, relief=tk.GROOVE, width=7,
                                                       height=1,
                                                       activebackground='blue',command=self.buscar_ids_contribuyente)
            self.elementos.boton_buscar.place(x=20, y=185)


            # ====BOTON LIMPIAR CAJA ========
            self.elementos.boton_limpiar_cajas = tk.Button(self.ventana_principal, text="Limpiar",
                                                           font=("Arial", 10, "bold"), fg="black", bg="white", bd=4,
                                                           relief=tk.GROOVE, width=7, height=1, activebackground='blue',
                                                           command=self.limpiar_cajas_busqueda)
            self.elementos.boton_limpiar_cajas.place(x=110, y=185)

            # ===== TABLA ======
            # Crear Treeview

            style = ttk.Style()
            style.theme_use("alt")
            style.configure('Treeview.Heading', font=('Arial', 11, 'bold'))
            style.configure('Treeview', font=('Arial', 9))

            self.elementos.tree = ttk.Treeview(self.ventana_principal, columns=(
            'ID_expediente', 'NIT/CC', 'ID_auditor', 'ID_proceso','ID_prestamo', 'ID_caja', 'Estado', 'Año gravable'),
                                               show='headings', height=10)
            self.elementos.tree.heading('ID_expediente', text='ID_expediente')
            self.elementos.tree.column('ID_expediente', width=115, anchor='center')
            self.elementos.tree.heading('NIT/CC', text='NIT/CC')
            self.elementos.tree.column('NIT/CC', width=130, anchor='center')
            self.elementos.tree.heading('ID_auditor', text='ID_auditor')
            self.elementos.tree.column('ID_auditor', width=90, anchor='center')
            self.elementos.tree.heading('ID_proceso', text='ID_proceso')
            self.elementos.tree.column('ID_proceso', width=90, anchor='center')
            self.elementos.tree.heading('ID_prestamo', text='ID_prestamo')
            self.elementos.tree.column('ID_prestamo', width=100, anchor='center')
            self.elementos.tree.heading('ID_caja', text='ID_caja')
            self.elementos.tree.column('ID_caja', width=75, anchor='center')
            self.elementos.tree.heading('Estado', text='Estado')
            self.elementos.tree.column('Estado', width=85, anchor='center')
            self.elementos.tree.heading('Año gravable', text='Año gravable')
            self.elementos.tree.column('Año gravable', width=100, anchor='center')

            self.elementos.tree.place(x=20, y=230)
            #  =======MOSTRAR DATOS  ===========
            self.actualizar_tree_expediente()
            # Enlace del evento para seleccionar registros
            self.elementos.tree.bind("<<TreeviewSelect>>", self.selecionar_registro_expediente)

            # Crear barras de desplazamiento
            self.elementos.barra_desplazamiento_v = ttk.Scrollbar(self.ventana_principal, orient="vertical", command=self.elementos.tree.yview)
            self.elementos.barra_desplazamiento_v.place(x=808, y=230, height=226)
            # Configurar el Treeview para usar las Scrollbars
            self.elementos.tree.configure(yscrollcommand=self.elementos.barra_desplazamiento_v.set)

            # Boton atras
            self.elementos.boton_atras = tk.Button(self.ventana_principal, text="ATRAS", font=("Arial", 12, "bold"),
                                                   fg="black", bg="white", bd=4, relief=tk.GROOVE, width=15, height=2,
                                                   command=self.interfaz.atras)
            self.elementos.boton_atras.place(x=(self.ancho_pantalla - 250), y=(self.altura_pantalla - 150))

            self.motrar_informacion()

        except ValueError as error:
            if "error al obtener los procesos." in str(error):
                messagebox.showerror("Error", "error al obtener los procesos.")
        except Exception as e:
            # Si ocurre algún error, imprime un mensaje de error
            print("Error al mostrar gestion auditor:", str(e))

    def mostrar_hacer_prestamo(self):

        # ====LABEL IFRAME==============================
        self.elementos.label_frame = tk.LabelFrame(self.ventana_principal, text="HACER UN PRESTAMO",
                                                   font=("Arial", 12, "bold"), fg="black", bg="#E6F7FF", bd=3,
                                                   relief=tk.RIDGE)
        self.elementos.label_frame.place(x=875, y=60, width=470, height=270)

        # ===============CALENDARIOS=========================
        # =====ETIQUETA fecha entrega =========
        self.elementos.label_fecha_entrega = tk.Label(self.elementos.label_frame, text="Fecha del prestamo",
                                                      font=("Arial", 10, "bold"),
                                                      fg="black", bg="#E6F7FF")
        self.elementos.label_fecha_entrega.place(x=20, y=10)
        #  ========BOX FECHA ENTREGA==========
        self.elementos.box_fecha_entrega = DateEntry(self.elementos.label_frame, width=11, background='darkblue',
                                                     foreground='white',
                                                     weekendbackground='salmon', weekendforeground='black',
                                                     borderwidth=2, date_pattern='yyyy-mm-dd')
        self.elementos.box_fecha_entrega.place(x=160, y=10)
        self.elementos.box_fecha_entrega.configure(showweeknumbers=False)

        # ====== ETIQUETA RESPONSABLE =========
        self.elementos.label_responsable = tk.Label(self.elementos.label_frame, text="Responsable",
                                                    font=("Arial", 10, "bold"),
                                                    fg="black", bg="#E6F7FF")
        self.elementos.label_responsable.place(x=20, y=35)
        # ======BOX RESPONSABLE =======
        self.elementos.box_responsable = tk.Entry(self.elementos.label_frame,
                                                  textvariable=self.elementos.responsable_variable, bd=2,
                                                  font=("Arial", 10), width=20, insertbackground="blue",
                                                  selectbackground="blue",
                                                  relief=tk.RIDGE)
        self.elementos.box_responsable.place(x=160, y=35)
        self.elementos.box_responsable.delete(0, tk.END)
        # ==== ETIQUETA AREA ====
        self.elementos.label_area = tk.Label(self.elementos.label_frame, text="Area", font=("Arial", 10, "bold"),
                                             fg="black", bg="#E6F7FF")
        self.elementos.label_area.place(x=20, y=60)

        # =======combo box area=====
        self.elementos.box_area = ttk.Combobox(self.elementos.label_frame, values=self.opciones_area,
                                               textvariable=self.elementos.area_variable, font=("Arial", 10),
                                               width=19)
        self.elementos.box_area.place(x=160, y=60)
        # =====ETIQUETA expedientes =========
        self.elementos.label_id_expediente = tk.Label(self.elementos.label_frame, text="Expedientes",
                                                      font=("Arial", 10, "bold"),
                                                      fg="black", bg="#E6F7FF")
        self.elementos.label_id_expediente.place(x=20, y=90)

        # ======= text expedientes=====
        self.elementos.text_busqueda_id_expediente_1 = tk.Text(self.elementos.label_frame, width=40, height=7,
                                                               fg='black', font=('Arial', 9))
        self.elementos.text_busqueda_id_expediente_1.place(x=160, y=95)

        # ====== BOTON GUARDAR =====
        self.elementos.boton_insertar = tk.Button(self.elementos.label_frame, text="Insertar",
                                                  font=("Arial", 12, "bold"),
                                                  fg="black", bg="white", bd=4, relief=tk.GROOVE, width=7, height=1,
                                                  activebackground='blue',command=self.hacer_un_prestamo)
        self.elementos.boton_insertar.place(x=20, y=150)

    def mostrar_finalizar_prestamo(self):
        # ====LABEL IFRAME 1====
        self.elementos.label_frame1 = tk.LabelFrame(self.ventana_principal, text="FINALIZAR UN PRESTAMO",
                                                    font=("Arial", 12, "bold"), fg="black", bg="#E6F7FF", bd=3,
                                                    relief=tk.RIDGE)
        self.elementos.label_frame1.place(x=875, y=350, width=470, height=107)

        # ===============CALENDARIOS=========================

        # =====ETIQUETA fecha devolucion =========
        self.elementos.label_fecha_devolucion = tk.Label(self.elementos.label_frame1, text="Fecha de devolución",
                                                         font=("Arial", 10, "bold"),
                                                         fg="black", bg="#E6F7FF")
        self.elementos.label_fecha_devolucion.place(x=20, y=15)
        #  ========BOX FECHA DEVOLUCION==========
        self.elementos.box_fecha_devolucion = DateEntry(self.elementos.label_frame1, width=11, background='darkblue',
                                                        foreground='white',
                                                        weekendbackground='salmon', weekendforeground='black',
                                                        borderwidth=2, date_pattern='yyyy-mm-dd')
        self.elementos.box_fecha_devolucion.place(x=170, y=15)
        self.elementos.box_fecha_devolucion.configure(showweeknumbers=False)
        # ====== ETIQUETA id prestamo =========
        self.elementos.label_id_prestamo = tk.Label(self.elementos.label_frame1, text="ID_prestamo",
                                                    font=("Arial", 10, "bold"),
                                                    fg="black", bg="#E6F7FF")
        self.elementos.label_id_prestamo.place(x=20, y=45)

        # ======BOX ID_PRESTAMO =======
        self.elementos.box_id_prestamo = tk.Entry(self.elementos.label_frame1,
                                                  textvariable=self.elementos.id_variable_prestamo, bd=2,
                                                  font=("Arial", 10), width=12, insertbackground="blue",
                                                  selectbackground="blue",
                                                  relief=tk.RIDGE)
        self.elementos.box_id_prestamo.place(x=170, y=45)
        self.elementos.box_id_prestamo.delete(0, tk.END)

        # ====== BOTON GUARDAR =====
        self.elementos.boton_insertar1 = tk.Button(self.elementos.label_frame1, text="Finalizar",
                                                   font=("Arial", 12, "bold"),
                                                   fg="black", bg="white", bd=4, relief=tk.GROOVE, width=7, height=1,
                                                   activebackground='blue', command=self.finalizar_un_prestamo)
        self.elementos.boton_insertar1.place(x=300, y=30)

    def motrar_informacion(self):
        # =============LABEL FRAME3 INFORMACION==============================
        self.elementos.label_frame3 = tk.LabelFrame(self.ventana_principal, text="Información",
                                                    font=("Arial", 12, "bold"), fg="black", bg="#E6F7FF", bd=3,
                                                    relief=tk.RIDGE)
        self.elementos.label_frame3.place(x=20, y=470, width=1000, height=220)

        # ===== label ids encontrados ==========
        self.elementos.label_ids_encontrados = tk.Label(self.elementos.label_frame3, text="NIT/CC Encontrados",
                                                        font=("Arial", 11, "bold"),
                                                        fg="black", bg="#E6F7FF")
        self.elementos.label_ids_encontrados.place(x=30, y=5)

        # ======= text exp encontrados=====
        self.elementos.text_ids_encontrados = tk.Text(self.elementos.label_frame3, width=31, height=10
                                                      , fg='black', font=('Arial', 8))
        self.elementos.text_ids_encontrados.place(x=30, y=30)

        # Crear barras de desplazamiento
        self.elementos.barra_desplazamiento_v1 = ttk.Scrollbar(self.elementos.label_frame3, orient="vertical",
                                                              command=self.elementos.text_ids_encontrados.yview)
        self.elementos.barra_desplazamiento_v1.place(x=220, y=30, height=145)
        # Configurar el Treeview para usar las Scrollbars
        self.elementos.text_ids_encontrados.configure(yscrollcommand=self.elementos.barra_desplazamiento_v1.set)

        # ===== label ids NO encontrados ==========
        self.elementos.label_ids_no_encontrados = tk.Label(self.elementos.label_frame3, text="NIT/CC No Encontrados",
                                                           font=("Arial", 11, "bold"),
                                                           fg="black", bg="#E6F7FF")
        self.elementos.label_ids_no_encontrados.place(x=275, y=5)

        # ======= text exp encontrados=====
        self.elementos.text_ids_no_encontrados = tk.Text(self.elementos.label_frame3, width=31, height=10
                                                         , fg='black', font=('Arial', 8))
        self.elementos.text_ids_no_encontrados.place(x=275, y=30)

        # Crear barras de desplazamiento
        self.elementos.barra_desplazamiento_v2 = ttk.Scrollbar(self.elementos.label_frame3, orient="vertical",
                                                               command=self.elementos.text_ids_no_encontrados.yview)
        self.elementos.barra_desplazamiento_v2.place(x=465, y=30, height=145)
        # Configurar el Treeview para usar las Scrollbars
        self.elementos.text_ids_no_encontrados.configure(yscrollcommand=self.elementos.barra_desplazamiento_v2.set)

        # ===== label EXP prestados ==========
        self.elementos.label_exp_prestados = tk.Label(self.elementos.label_frame3,
                                                      text="Expedientes Prestados",
                                                      font=("Arial", 11, "bold"),
                                                      fg="black", bg="#E6F7FF")
        self.elementos.label_exp_prestados.place(x=520, y=5)

        # ======= text exp encontrados=====
        self.elementos.text_exp_prestados = tk.Text(self.elementos.label_frame3, width=31, height=10
                                                    , fg='black', font=('Arial', 8))
        self.elementos.text_exp_prestados.place(x=520, y=30)

        # Crear barras de desplazamiento
        self.elementos.barra_desplazamiento_v3 = ttk.Scrollbar(self.elementos.label_frame3, orient="vertical",
                                                               command=self.elementos.text_exp_prestados.yview)
        self.elementos.barra_desplazamiento_v3.place(x=710, y=30, height=145)
        # Configurar el Treeview para usar las Scrollbars
        self.elementos.text_exp_prestados.configure(yscrollcommand=self.elementos.barra_desplazamiento_v3.set)

        # ===== label EXP Disponibles ==========
        self.elementos.label_exp_disponibles = tk.Label(self.elementos.label_frame3,
                                                        text="Expedientes Disponibles",
                                                        font=("Arial", 11, "bold"),
                                                        fg="black", bg="#E6F7FF")
        self.elementos.label_exp_disponibles.place(x=765, y=5)

        # ======= text exp encontrados=====
        self.elementos.text_exp_disponibles = tk.Text(self.elementos.label_frame3, width=31, height=10
                                                      , fg='black', font=('Arial', 8))
        self.elementos.text_exp_disponibles.place(x=765, y=30)

        # Crear barras de desplazamiento
        self.elementos.barra_desplazamiento_v4 = ttk.Scrollbar(self.elementos.label_frame3, orient="vertical",
                                                               command=self.elementos.text_exp_disponibles.yview)
        self.elementos.barra_desplazamiento_v4.place(x=955, y=30, height=145)
        # Configurar el Treeview para usar las Scrollbars
        self.elementos.text_exp_disponibles.configure(yscrollcommand=self.elementos.barra_desplazamiento_v4.set)

    def obtener_procesos(self):

        mensaje, procesos = self.consultas_proceso.mostrar_nombre_id_procesos()
        if procesos:
            #print(mensaje)
            self.dic_procesos= {proceso[0]: proceso[1] for proceso in procesos}
            #print(dic_procesos)
            return self.dic_procesos
        else:
            print(mensaje)
            return None

    def extraer_id_proceso(self):
        # Obtener el texto seleccionado del Combobox
        seleccion = self.elementos.id_variable_proceso.get()
        if seleccion:
            # Dividir la cadena seleccionada en clave y valor
            clave, _ = seleccion.split(": ", 1)
            print(f"Clave seleccionada: {clave}")  # También imprimir en la consola para depuración
            return clave

    def actualizar_tree_expediente(self):
        """
                Método para actualizar la tabla de expedientes en la interfaz gráfica.
                """
        try:
            # borrar elementos actuales del tree contribuyente
            # devuelve una lista de identificadores de elementos secundarios
            # , y el operador * se utiliza para pasar esos identificadores
            # como argumentos separados a la función delete.
            self.elementos.tree.delete(*self.elementos.tree.get_children())

            # obtener los nuevos datos que deseamos mostrar
            mensaje, expedientes = self.consultas_expediente.obtener_ultimo_expediente()
            # print(contribuyentes)
            # insertar lo nuevos datos  en el tree
            # mostrar datos en la tabla
            if expedientes:
                for row in expedientes:
                    self.elementos.tree.insert("", "end", values=row)
            else:
                messagebox.showinfo("Información", "No hay datos disponibles para mostrar.")
                raise ValueError("La tabla expedientes esta vacia")
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
                #obtener valores
                values = self.elementos.tree.item(itemseleccionado)['values']


        except ValueError as error:
            print(f"fError al seleccionar registro : {error}")

    def obtener_ids(self):
        try:
            ids_raw = self.elementos.text_busqueda_id_expediente.get("1.0", tk.END).strip()
            # Dividir el texto por comas y quitar espacios en blanco alrededor de cada ID
            lista_ids = [id.strip() for id in ids_raw.split(",") if id.strip()]
            print(lista_ids)

            # Filtrar IDs válidos y recolectar IDs inválidos
            raw_ids_validos = []
            raw_ids_no_validos = []
            for id in lista_ids:
                if 3 <= len(id) <= 10 and id.isdigit():
                    raw_ids_validos.append(id)
                else:
                    raw_ids_no_validos.append(id)

            print("IDs válidos:", raw_ids_validos)
            print("IDs inválidos:", raw_ids_no_validos)
            return raw_ids_validos, raw_ids_no_validos
        except tk.TclError as e:
            print("Error al obtener datos del cuadro de texto:", str(e))
            messagebox.showerror("Error de interfaz","Se produjo un error al intentar obtener los datos del cuadro de texto.")
            return [], []
        except Exception as e:
            print("Error inesperado:", str(e))
            messagebox.showerror("Error inesperado", f"Se produjo un error inesperado: {str(e)}")
            return [], []

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

    def buscar_ids_contribuyente(self):
        try:
            # ========obtener datos============
            self.ids_validos,self.ids_invalidos = self.obtener_ids()
            proceso = self.elementos.box_id_proceso.get().strip()
            id_proceso = proceso.split(':')[0].strip()
            años_gravables = [self.elementos.box_año_gravable.get().strip(),
                              self.elementos.box_año_gravable_1.get().strip(),
                              self.elementos.box_año_gravable_2.get().strip(),
                              self.elementos.box_año_gravable_3.get().strip(),
                              self.elementos.box_año_gravable_4.get().strip()]
            # Eliminar años gravables vacíos de la lista
            años_gravables = [año for año in años_gravables if año]
            # Mostrar alerta si hay IDs inválidos
            if self.ids_invalidos:
                raise ValueError(f"Los siguientes IDs no cumplen con las condiciones de longitud (6-10 dígitos):\n{', '.join(self.ids_invalidos)}")
            # Verificar años gravables
            mensaje, confirmacion = self.verificar_años_gravables(años_gravables)
            if años_gravables and not confirmacion:
                raise ValueError(mensaje)

            # Llamar a la función con los argumentos adecuados
            if self.ids_validos and id_proceso:
                if años_gravables:
                    resultado = self.consultas_expediente.buscar_y_verificar_expedientes(self.ids_validos, id_proceso, años_gravables)
                else:
                    resultado = self.consultas_expediente.buscar_y_verificar_expedientes(self.ids_validos, id_proceso)

                registros = resultado["exp encontrados"]

                if registros:
                    try:
                        # actualizamos los campos del tree
                        self.elementos.tree.delete(*self.elementos.tree.get_children())
                        for row in registros:
                            self.elementos.tree.insert("", "end", values=row)
                    except Exception as update_error:
                        messagebox.showerror("Error", f"Error al actualizar la tabla: {update_error}")
                        print(f"Error al actualizar la tabla: {update_error}")

                    if not resultado["exp encontrados"]:
                        messagebox.showinfo("INFORMACIÓN","No se encontraron resultados")

                    # Mostrar resultados en los cuadros de texto
                    self.elementos.text_ids_encontrados.delete(1.0, tk.END)
                    self.elementos.text_ids_encontrados.insert(tk.END,','.join(resultado.get("ids encontrados", [])))

                    self.elementos.text_ids_no_encontrados.delete(1.0, tk.END)
                    self.elementos.text_ids_no_encontrados.insert(tk.END, ','.join(resultado.get("ids no_encontrados", [])))

                    self.elementos.text_exp_prestados.delete(1.0, tk.END)
                    self.elementos.text_exp_prestados.insert(tk.END, ','.join(resultado.get("exp prestados", [])))

                    self.elementos.text_exp_disponibles.delete(1.0, tk.END)
                    self.elementos.text_exp_disponibles.insert(tk.END, ','.join(resultado.get("exp disponibles", [])))


                else:
                    messagebox.showinfo("INFORMACIÓN", "No se encontraron registros")
            else:
                messagebox.showerror("Error", "Debe estipular almenos un ID y el proceso.")

        except tk.TclError as e:
            print("Error al obtener datos del cuadro de texto:", str(e))
            messagebox.showerror("Error de interfaz","Se produjo un error al intentar obtener los datos del cuadro de texto.")
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def limpiar_cajas_busqueda(self):

        self.elementos.text_busqueda_id_expediente.delete(1.0, tk.END)
        self.elementos.box_año_gravable.delete(0, tk.END)
        self.elementos.box_año_gravable_1.delete(0, tk.END)
        self.elementos.box_año_gravable_2.delete(0, tk.END)
        self.elementos.box_año_gravable_3.delete(0, tk.END)
        self.elementos.box_año_gravable_4.delete(0, tk.END)
        self.elementos.text_ids_encontrados.delete(1.0, tk.END)
        self.elementos.text_ids_no_encontrados.delete(1.0, tk.END)
        self.elementos.text_ids_encontrados.delete(1.0, tk.END)
        self.elementos.text_exp_prestados.delete(1.0, tk.END)
        self.elementos.text_exp_disponibles.delete(1.0, tk.END)

    def limpiar_cajas_hacer_prestamo(self):

        self.elementos.box_responsable.delete(0, tk.END)
        self.elementos.box_area.delete(0, tk.END)
        self.elementos.text_busqueda_id_expediente_1.delete(1.0, tk.END)

    def limpiar_cajas_finalizar_prestamo(self):

        self.elementos.box_id_prestamo.delete(0, tk.END)

    def hacer_un_prestamo(self):

        fecha_entrega = self.elementos.box_fecha_entrega.get()

        responsable = self.elementos.box_responsable.get().strip()
        area = self.elementos.box_area.get().strip()
        expedientes_text = self.elementos.text_busqueda_id_expediente_1.get("1.0", tk.END).strip()

        # Convertir la cadena de expedientes a una lista, asumiendo que están separados por comas
        if expedientes_text:
            expedientes = [exp.strip() for exp in expedientes_text.split(",") if exp.strip()]
        else:
            expedientes = []

        if fecha_entrega and responsable and area and expedientes:
            try:
                if area not  in self.opciones_area:
                    raise ValueError("Area no valida.")

                mensaje_prestamo , confirmacion_prestamo = self.prestamo.insertar_prestamo_vinculacion(fecha_entrega,responsable,area,expedientes)

                if confirmacion_prestamo:
                    print(mensaje_prestamo)
                    mensaje_ultimo_prestamo , ultimo_prestamo = self.consultas_prestamo.obtener_ultimo_prestamo()


                    if ultimo_prestamo:
                        id_prestamo = ultimo_prestamo[0][0]
                        print(mensaje_ultimo_prestamo,ultimo_prestamo)
                        messagebox.showinfo(f"INFORMACIÓN", f"Prestamo Realizado, los expedientes {expedientes} fueron asignados al id_ prestamo = {id_prestamo}")
                        self.limpiar_cajas_hacer_prestamo()
                    else:
                        messagebox.showerror("Error", "No se pudo obtener el último préstamo.")
                else:
                    messagebox.showerror("Error", mensaje_prestamo)

            except ValueError as error:
                if "Area no valida." in str(error):
                    messagebox.showerror("Error", f"El área '{area}' no es válida.")
                elif "Error al conectar a la base de datos" in str(error):
                    messagebox.showerror("Error de conexión", "No se pudo conectar a la base de datos.")
                else:
                    messagebox.showerror("Error", str(error))
            except Exception as error:
                messagebox.showerror("Error inesperado", str(error))
        else:
            messagebox.showerror("Error", "Todas las cajas de texto deben tener un valor.")

    def finalizar_un_prestamo(self):

        fecha_devolucion = self.elementos.box_fecha_devolucion.get()
        id_prestamo = self.elementos.box_id_prestamo.get().strip()

        if fecha_devolucion and id_prestamo:
            try:

                # Verificar si id_prestamo es un número entero válido
                if id_prestamo.isdigit():
                    id_prestamo = int(id_prestamo)  # Convertir el string a un entero
                    print("El ID de préstamo es válido:", id_prestamo)
                    mensaje_finalizacion , confirmacion_finalizacion = self.prestamo.finalizar_prestamo(id_prestamo,fecha_devolucion)
                    if confirmacion_finalizacion:
                        messagebox.showinfo("INFORMACIÓN", "El prestamo finalizado.")
                        self.limpiar_cajas_finalizar_prestamo()
                    else:
                        messagebox.showerror("INFORMACIÓN", "No se finalizó el prestamo.")
                else:
                    print("El ID de préstamo no es un número válido:", id_prestamo)
                    raise ValueError("ID Prestamo no es un digito.")

            except ValueError as e:
                if "Area no valida." in str(e):
                    messagebox.showerror("Error", "El ID de préstamo debe ser un número entero.")
                else:
                    messagebox.showerror("Error", str(e))

        else:
            messagebox.showerror("Error", "Todas las cajas de texto deben tener un valor.")















