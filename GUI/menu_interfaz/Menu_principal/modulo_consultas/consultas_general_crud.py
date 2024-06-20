import tkinter as tk
import json
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime, date
from consultas.consultas_compuestas import ConsultasCompuestas
from consultas.consultas_auditor import ConsultasAuditor
from consultas.consultas_expediente import ConsultasExpediente
from consultas.consultas_proceso import ConsultasProceso
import re

class ConsultasGeneral:

    def __init__(self, ventana_principal, elementos, interfaz):
        """
                Constructor de la clase AuditorCrud.

                Args:
                    ventana_principal: La ventana principal de la interfaz gráfica.
                    elementos: Objeto que contiene los elementos de la interfaz gráfica.
                    interfaz: Objeto que representa la interfaz gráfica en general.
                """
        self.ventana_principal = ventana_principal
        self.elementos = elementos
        self.interfaz = interfaz
        self.consultas = ConsultasCompuestas()
        self.auditor = ConsultasAuditor()
        self.proceso = ConsultasProceso()
        self.altura_pantalla = self.interfaz.window_height
        self.ancho_pantalla = self.interfaz.window_width
        self.opciones_estado = ["activo", "auto archivo"]
        self.opciones_tipo = ["Natural", "Jurídico"]
        self.filtros = {}


    def mostrar_consultas_general(self):
        """
                                Método para mostrar la interfaz de consultas prestamos crud.
                                """
        self.interfaz.estado_actual = "Consultas_general"
        print(self.interfaz.estado_actual)

        try:

            dic_auditores = self.obtener_auditores()  # Obtener el diccionario de auditores
            dic_procesos = self.obtener_procesos()  # Obtener el diccionario de procesos

            if dic_auditores:
                lista_nombres_auditores = [f"{k}: {v}" for k, v in dic_auditores.items()]  # Obtener solo los nombres de los auditores
            else:
                raise ValueError("error al obtener los auditores.")

            if dic_procesos:

                lista_nombres_procesos = [f"{k}: {v}" for k, v in dic_procesos.items()]
            else:
                raise ValueError("error al obtener los procesos.")

            # ==== TITULO ======
            self.elementos.label_titulo = tk.Label(self.ventana_principal, text="CONSULTAS GENERALES",
                                                   font=("Arial", 20, "bold"), fg="black", bg="#E6F7FF")
            self.elementos.label_titulo.pack(pady=20)  # pady añade un espacio en la parte inferior de la etiqueta

            # ====LABEL IFRAME====
            self.elementos.label_frame = tk.LabelFrame(self.ventana_principal, text="FILTROS DE BUSQUEDA",
                                                       font=("Arial", 16, "bold"), fg="black", bg="#E6F7FF", bd=3,
                                                       relief=tk.RIDGE)
            self.elementos.label_frame.place(x=20, y=60, width=1330, height=120)

            # =========== ETIQUETA ID_EXPEDIENTE =============
            self.elementos.label_id_expediente = tk.Label(self.elementos.label_frame, text="ID_expediente",
                                                          font=("Arial", 10, "bold"),
                                                          fg="black", bg="#E6F7FF")
            self.elementos.label_id_expediente.place(x=20, y=20)

            # =====CAJA ID_expediente =========
            self.elementos.box_id_expediente = tk.Entry(self.elementos.label_frame,
                                                        textvariable=self.elementos.id_variable_expediente, bd=1,
                                                        font=("Arial", 10), width=12, insertbackground="blue",
                                                        selectbackground="blue",
                                                        relief=tk.SOLID)
            self.elementos.box_id_expediente.place(x=130, y=20)
            self.elementos.box_id_expediente.delete(0, tk.END)

            # ===== ETIQUETA NOMBRE ======
            self.elementos.label_nombre = tk.Label(self.elementos.label_frame, text="Nombre Cont",
                                                   font=("Arial", 10, "bold"),
                                                   fg="black", bg="#E6F7FF")
            self.elementos.label_nombre.place(x=20, y=50)

            # ====== CAJA NOMBRE ======
            self.elementos.box_nombre = tk.Entry(self.elementos.label_frame,
                                                 textvariable=self.elementos.nombre_variable,
                                                 bd=1, font=("Arial", 10), width=38, insertbackground="blue",
                                                 selectbackground="blue", relief=tk.SOLID)
            self.elementos.box_nombre.place(x=130, y=50)
            self.elementos.box_nombre.delete(0,tk.END)


            # ==== ETIQUETA ESTADO ====
            self.elementos.label_estado = tk.Label(self.elementos.label_frame, text="Estado", font=("Arial", 10, "bold"),
                                                 fg="black", bg="#E6F7FF")
            self.elementos.label_estado.place(x=250, y=20)

            # =======combo box ESTADO=====
            self.elementos.box_estado = ttk.Combobox(self.elementos.label_frame, values=self.opciones_estado,
                                                   textvariable=self.elementos.estado_variable, font=("Arial", 9),
                                                   width=10)
            self.elementos.box_estado.place(x=310, y=20)

            # ===== ETIQUETA ID_Auditor ======
            self.elementos.label_id_auditor = tk.Label(self.elementos.label_frame, text="Nombre Auditor",
                                                       font=("Arial", 10, "bold"),
                                                       fg="black", bg="#E6F7FF")
            self.elementos.label_id_auditor.place(x=440, y=20)

            # ===== COMBOBOX Auditor =========
            self.elementos.box_id_auditor = ttk.Combobox(self.elementos.label_frame,
                                                         values=lista_nombres_auditores,
                                                         textvariable=self.elementos.id_variable_auditor,
                                                         font=("Arial", 10),
                                                         width=11, style="EstiloCombobox.TCombobox")
            self.elementos.box_id_auditor.place(x=600, y=20)



            # ======== ETIQUETA ID_CONTRIBUYENTE ==============
            self.elementos.label_id_contribuyente = tk.Label(self.elementos.label_frame, text="NIT/CC contribuyente",
                                                             font=("Arial", 10, "bold"),
                                                             fg="black", bg="#E6F7FF")
            self.elementos.label_id_contribuyente.place(x=440, y=50)

            # =====CAJA ID_Contribuyente =========
            self.elementos.box_id_contribuyente = tk.Entry(self.elementos.label_frame,
                                                           textvariable=self.elementos.id_variable_contribuyente, bd=1,
                                                           font=("Arial", 10), width=12, insertbackground="blue",
                                                           selectbackground="blue",
                                                           relief=tk.SOLID)
            self.elementos.box_id_contribuyente.place(x=600, y=50)
            self.elementos.box_id_contribuyente.delete(0, tk.END)

            # ==== ETIQUETA TIPO ====
            self.elementos.label_tipo = tk.Label(self.elementos.label_frame, text="Tipo", font=("Arial", 10, "bold"),
                                                 fg="black", bg="#E6F7FF")
            self.elementos.label_tipo.place(x=720, y=20)

            # =======combo box tipo=====
            self.elementos.box_tipo = ttk.Combobox(self.elementos.label_frame, values=self.opciones_tipo,
                                                   textvariable=self.elementos.tipo_variable, font=("Arial", 10),
                                                   width=8)
            self.elementos.box_tipo.place(x=820, y=20)

            # =====ETIQUETA año gravable ======
            self.elementos.label_año_gravable = tk.Label(self.elementos.label_frame, text="Año gravable",
                                                         font=("Arial", 10, "bold"),
                                                         fg="black", bg="#E6F7FF")
            self.elementos.label_año_gravable.place(x=720, y=50)
            # =====CAJA año gravable =========
            self.elementos.box_año_gravable = tk.Entry(self.elementos.label_frame,
                                                       textvariable=self.elementos.año_gravable_variable, bd=1,
                                                       font=("Arial", 10), width=6, insertbackground="blue",
                                                       selectbackground="blue",
                                                       relief=tk.SOLID)
            self.elementos.box_año_gravable.place(x=820, y=50)
            self.elementos.box_año_gravable.delete(0, tk.END)

            # =====ETIQUETA ID_caja ======
            self.elementos.label_id_caja = tk.Label(self.elementos.label_frame, text="ID_caja",
                                                    font=("Arial", 10, "bold"),
                                                    fg="black", bg="#E6F7FF")
            self.elementos.label_id_caja.place(x=930, y=20)
            # =====CAJA ID_caja =========
            self.elementos.box_id_caja = tk.Entry(self.elementos.label_frame,
                                                  textvariable=self.elementos.id_variable_caja, bd=1,
                                                  font=("Arial", 10), width=10, insertbackground="blue",
                                                  selectbackground="blue",
                                                  relief=tk.SOLID)
            self.elementos.box_id_caja.place(x=1000, y=20)
            self.elementos.box_id_caja.delete(0, tk.END)

            # =====ETIQUETA ID_proceso ======
            self.elementos.label_id_proceso = tk.Label(self.elementos.label_frame, text="Proceso",
                                                       font=("Arial", 10, "bold"),
                                                       fg="black", bg="#E6F7FF")
            self.elementos.label_id_proceso.place(x=930, y=50)

            # ===== COMBOBOX ID_proceso =========
            self.elementos.box_id_proceso = ttk.Combobox(self.elementos.label_frame,
                                                         values=lista_nombres_procesos,
                                                         textvariable=self.elementos.id_variable_proceso,
                                                         font=("Arial", 10),
                                                         width=11)
            self.elementos.box_id_proceso.place(x=1000, y=50)



            # BOTON BUSCAR
            self.elementos.boton_buscar = tk.Button(self.elementos.label_frame, text="BUSCAR",
                                                    font=("Arial", 10, "bold"), fg="black", bg="white",
                                                    bd=3,
                                                    relief=tk.GROOVE, width=7, height=1,
                                                    activebackground='blue',command=self.buscar_expedientes_filtrados)
            self.elementos.boton_buscar.place(x=1150, y=25)

            # ====BOTON LIMPIAR CAJA ========
            self.elementos.boton_limpiar_cajas = tk.Button(self.elementos.label_frame, text="LIMPIAR",
                                                           font=("Arial", 10, "bold"), fg="black", bg="white",
                                                           bd=3,
                                                           relief=tk.GROOVE, width=7, height=1,
                                                           activebackground='blue',command=self.limpiar_cajas_texto)
            self.elementos.boton_limpiar_cajas.place(x=1250, y=25)




            # Boton atras
            self.elementos.boton_atras = tk.Button(self.ventana_principal, text="ATRAS", font=("Arial", 12, "bold"),
                                                   fg="black", bg="white", bd=4, relief=tk.GROOVE, width=15, height=2,
                                                   command=self.interfaz.atras)
            self.elementos.boton_atras.place(x=(self.ancho_pantalla - 250), y=(self.altura_pantalla - 150))

            # ===== TABLA ======
            # Crear Treeview

            style = ttk.Style()
            style.theme_use("alt")
            style.configure('Treeview.Heading', font=('Arial', 9, 'bold'))
            style.configure('Treeview', font=('Arial', 10))

            self.elementos.tree = ttk.Treeview(self.ventana_principal, columns=(
                'Nombre', 'NIT/CC', 'Tipo', 'Nombre Auditor', 'Proceso', 'ID_expediente', 'ID_prestamo','ID_caja','Estado',
                'Año gravable'), show='headings', height=18)
            self.elementos.tree.heading('Nombre', text='Nombre')
            self.elementos.tree.column('Nombre', width=350, anchor='center')
            self.elementos.tree.heading('NIT/CC', text='NIT/CC')
            self.elementos.tree.column('NIT/CC', width=90, anchor='center')
            self.elementos.tree.heading('Tipo', text='Tipo')
            self.elementos.tree.column('Tipo', width=80, anchor='center')
            self.elementos.tree.heading('Nombre Auditor', text='Nombre Auditor')
            self.elementos.tree.column('Nombre Auditor', width=247, anchor='center')
            self.elementos.tree.heading('Proceso', text='Proceso')
            self.elementos.tree.column('Proceso', width=100, anchor='center')
            self.elementos.tree.heading('ID_expediente', text='ID_expediente')
            self.elementos.tree.column('ID_expediente', width=100, anchor='center')
            self.elementos.tree.heading('ID_prestamo', text='ID_prestamo')
            self.elementos.tree.column('ID_prestamo', width=90, anchor='center')
            self.elementos.tree.heading('ID_caja', text='ID_caja')
            self.elementos.tree.column('ID_caja', width=70, anchor='center')
            self.elementos.tree.heading('Estado', text='Estado')
            self.elementos.tree.column('Estado', width=90, anchor='center')
            self.elementos.tree.heading('Año gravable', text='Año gravable')
            self.elementos.tree.column('Año gravable', width=80, anchor='center')

            self.elementos.tree.place(x=30, y=200)
            #  =======MOSTRAR DATOS  ===========

            # Enlace del evento para seleccionar registros
            self.elementos.tree.bind("<<TreeviewSelect>>", self.selecionar_registro_tabla)

            # Crear barras de desplazamiento
            self.elementos.barra_desplazamiento_v = ttk.Scrollbar(self.ventana_principal, orient="vertical",
                                                                  command=self.elementos.tree.yview)
            self.elementos.barra_desplazamiento_v.place(x=1330, y=200, height=379)
            # Configurar el Treeview para usar las Scrollbars
            self.elementos.tree.configure(yscrollcommand=self.elementos.barra_desplazamiento_v.set)

        except Exception as e:

            # Si ocurre algún error, imprime un mensaje de error
            print("Error al mostrar consultas prestamos crud:", str(e))


    def selecionar_registro_tabla(self, event):
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

    def obtener_auditores(self):

        """
        Método para obtener la lista de los auditores y su id .

        """

        mensaje, auditores = self.auditor.mostrar_nombre_id_auditores()
        if auditores:
            #print(mensaje)
            self.dic_auditores= {auditor[0]: auditor[1] for auditor in auditores}
            #print(dic_auditores)
            return self.dic_auditores
        else:
            print(mensaje)
            return None

    def obtener_procesos(self):
        """
                Método para obtener la lista de los procesos y su id .

                """

        mensaje, procesos = self.proceso.mostrar_nombre_id_procesos()
        if procesos:
            #print(mensaje)
            self.dic_procesos= {proceso[0]: proceso[1] for proceso in procesos}
            #print(dic_procesos)
            return self.dic_procesos
        else:
            print(mensaje)
            return None

    def limpiar_cajas_texto(self):
        """
                Método para limpiar las cajas de texto en la interfaz gráfica.
                """

        self.elementos.box_id_expediente.delete(0, tk.END)
        self.elementos.box_nombre.delete(0, tk.END)
        self.elementos.box_estado.delete(0, tk.END)
        self.elementos.box_id_auditor.delete(0, tk.END)
        self.elementos.box_id_contribuyente.delete(0, tk.END)
        self.elementos.box_tipo.delete(0, tk.END)
        self.elementos.box_año_gravable.delete(0, tk.END)
        self.elementos.box_id_caja.delete(0, tk.END)
        self.elementos.box_id_proceso.delete(0, tk.END)
        self.filtros = {}

    def buscar_expedientes_filtrados(self):

        """
            Busca expedientes filtrados según los valores proporcionados en las cajas de texto.

            Esta función extrae los valores de las cajas de texto para diferentes campos, los valida y
            los agrega a un diccionario de filtros. Luego, llama a la función de búsqueda con los filtros
            y actualiza una tabla de resultados si se encuentran coincidencias.

            Campos utilizados:
            - id_expediente: ID del expediente que debe empezar por O, I o S.
            - nombre_contribuyente: Nombre del contribuyente.
            - estado: Estado del expediente.
            - auditor: ID del auditor, de donde se extrae el nombre del auditor.
            - id_contribuyente: ID del contribuyente, que debe ser un número.
            - tipo: Tipo del contribuyente.
            - año: Año gravable del expediente.
            - id_caja: ID de la caja.
            - proceso: ID del proceso, de donde se extrae el nombre del proceso.

            Si alguno de los campos tiene un valor, se procede con la validación y búsqueda; de lo contrario, se muestra un error.
            """

        id_expediente = self.elementos.box_id_expediente.get().strip()
        nombre_contribuyente = self.elementos.box_nombre.get().strip()
        estado = self.elementos.box_estado.get().strip()
        auditor = self.elementos.box_id_auditor.get().strip()
        id_contribuyente = self.elementos.box_id_contribuyente.get().strip()
        tipo = self.elementos.box_tipo.get().strip()
        año = self.elementos.box_año_gravable.get().strip()
        id_caja = self.elementos.box_id_caja.get().strip()
        proceso = self.elementos.box_id_proceso.get().strip()

        nombre_auditor = auditor.split(':')[1].strip() if ':' in auditor else None
        nombre_proceso = proceso.split(':')[0].strip() if ':' in proceso else None

        print(f"Nombre Auditor: {nombre_auditor}")
        print(f"Nombre Proceso: {nombre_proceso}")



        if (id_expediente or nombre_contribuyente or estado or nombre_auditor or id_contribuyente or tipo or año or id_caja or nombre_proceso):

            try:
                # Validar y agregar al diccionario de filtros

                if id_expediente:
                    if id_expediente[0].upper() not in ['O', 'I', 'S']:
                        raise ValueError("ID del expediente debe empezar por O, I o S.")
                    self.filtros['id_expediente'] = id_expediente

                if nombre_contribuyente:
                    self.filtros['nombre_contribuyente'] = nombre_contribuyente

                if estado:
                    self.filtros['estado'] = estado

                if nombre_auditor:
                    self.filtros['nombre_auditor'] = nombre_auditor

                if id_contribuyente:
                    if not id_contribuyente.isdigit():
                        raise ValueError("ID del contribuyente debe comenzar con un número.")
                    self.filtros['id_contribuyente'] = id_contribuyente

                if tipo:
                    self.filtros['tipo_contribuyente'] = tipo

                if año:
                    mensaje_ano, confirmacion_ano = self.verificar_años_gravables([año])
                    if not confirmacion_ano:
                        raise ValueError(mensaje_ano)
                    else:
                        self.filtros['año_gravable'] = año

                if id_caja:
                    self.filtros['id_caja'] = id_caja

                if nombre_proceso:
                    self.filtros['id_proceso'] = nombre_proceso

                print("filtros",self.filtros)
                # Llamar a la función de búsqueda con los filtros
                mensaje, encabezados, resultados,confirmacion = self.consultas.buscar_expedientes_filtrados(self.filtros)

                if mensaje:
                    print(mensaje)
                    print(encabezados)
                    print(resultados)
                if confirmacion:
                    try:
                        # actualizamos los campos del tree
                        self.elementos.tree.delete(*self.elementos.tree.get_children())
                        for row in resultados:
                            self.elementos.tree.insert("", "end", values=row)
                        self.filtros = {}
                    except Exception as update_error:
                        messagebox.showerror("Error", f"Error al actualizar la tabla: {update_error}")
                        print(f"Error al actualizar la tabla: {update_error}")
                else:
                    messagebox.showinfo("INFORMACIÓN", "No se encontraron registros")
                    self.filtros = {}
                    self.limpiar_cajas_texto()


            except tk.TclError as e:
                print("Error al obtener datos del cuadro de texto:", str(e))
                messagebox.showerror("Error de interfaz", "Se produjo un error al intentar obtener los datos del cuadro de texto.")
            except ValueError as error:
                messagebox.showerror("Error", str(error))

        else:
            messagebox.showerror("Error", "Todas las cajas de texto deben tener un valor.")
            self.filtros = {}
            self.limpiar_cajas_texto()


    def verificar_años_gravables(self, años_gravables:list):
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
