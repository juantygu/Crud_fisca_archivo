import tkinter as tk
import json
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime, date
from consultas.consultas_compuestas import ConsultasCompuestas


class ConsultasPrestamosActivos:
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
        self.altura_pantalla = self.interfaz.window_height
        self.ancho_pantalla = self.interfaz.window_width
        self.opciones_area = ["Fiscalización", "Impuestos", "Tesoreria", "Asesoría externa", "Hacienda", "Alcaldia"]
        self.filtros = {}
        self.fecha_entrega_selected = False
        self.fecha_entrega1_selected = False
        self.fecha_click = False
        self.fecha1_click = False

    def mostrar_consultas_prestamos_activos(self):
        """
                        Método para mostrar la interfaz de consultas prestamos crud.
                        """
        self.interfaz.estado_actual = "Consultas_prestamos_activos"
        print(self.interfaz.estado_actual)

        try:
            # ==== TITULO ======
            self.elementos.label_titulo = tk.Label(self.ventana_principal, text="CONSULTAS PRESTAMOS ACTIVOS",
                                                   font=("Arial", 20, "bold"), fg="black", bg="#E6F7FF")
            self.elementos.label_titulo.pack(pady=20)  # pady añade un espacio en la parte inferior de la etiqueta

            # ====LABEL IFRAME====
            self.elementos.label_frame = tk.LabelFrame(self.ventana_principal, text="FILTROS DE BUSQUEDA",
                                                       font=("Arial", 16, "bold"), fg="black", bg="#E6F7FF", bd=3,
                                                       relief=tk.RIDGE)
            self.elementos.label_frame.place(x=180, y=60, width=1000, height=120)



            # =====ETIQUETA fecha entrega INICIAL =========
            self.elementos.label_fecha_entrega = tk.Label(self.elementos.label_frame, text="Fecha del prestamo inicial",
                                                          font=("Arial", 10, "bold"),
                                                          fg="black", bg="#E6F7FF")
            self.elementos.label_fecha_entrega.place(x=20, y=20)
            #  ========BOX FECHA ENTREGA INICIAL==========
            self.elementos.box_fecha_entrega = DateEntry(self.elementos.label_frame, width=11, background='darkblue',
                                                         foreground='white',
                                                         weekendbackground='salmon', weekendforeground='black',
                                                         borderwidth=2, date_pattern='yyyy-mm-dd')
            self.elementos.box_fecha_entrega.place(x=200, y=20)
            # Borrar cualquier texto presente en el widget (establecer como vacío)
            self.elementos.box_fecha_entrega.delete(0, 'end')
            self.elementos.box_fecha_entrega.configure(showweeknumbers=False)
            # Evento para mantener el DateEntry vacío
            self.elementos.box_fecha_entrega.bind("<<DateEntrySelected>>", self.fecha_selected)
            self.elementos.box_fecha_entrega.bind("<FocusOut>", self.fecha_entrega_focus_out)


            # =====ETIQUETA fecha entrega FINAL =========
            self.elementos.label_fecha_entrega_1 = tk.Label(self.elementos.label_frame, text="Fecha del prestamo final",
                                                          font=("Arial", 10, "bold"),
                                                          fg="black", bg="#E6F7FF")
            self.elementos.label_fecha_entrega_1.place(x=20, y=50)
            #  ========BOX FECHA ENTREGA FINAL ==========
            self.elementos.box_fecha_entrega1 = DateEntry(self.elementos.label_frame, width=11, background='darkblue',
                                                         foreground='white',
                                                         weekendbackground='salmon', weekendforeground='black',
                                                         borderwidth=2, date_pattern='yyyy-mm-dd')
            self.elementos.box_fecha_entrega1.place(x=200, y=50)
            self.elementos.box_fecha_entrega1.delete(0, 'end')
            self.elementos.box_fecha_entrega1.configure(showweeknumbers=False)
            # Evento para mantener el DateEntry vacío
            self.elementos.box_fecha_entrega1.bind("<<DateEntrySelected>>", self.fecha1_selected)
            self.elementos.box_fecha_entrega1.bind("<FocusOut>", self.fecha_entrega1_focus_out)




            # ====== ETIQUETA id prestamo =========
            self.elementos.label_id_prestamo = tk.Label(self.elementos.label_frame, text="ID_prestamo",
                                                        font=("Arial", 10, "bold"),
                                                        fg="black", bg="#E6F7FF")
            self.elementos.label_id_prestamo.place(x=310, y=20)

            # ======BOX ID_PRESTAMO =======
            self.elementos.box_id_prestamo = tk.Entry(self.elementos.label_frame,
                                                      textvariable=self.elementos.id_variable_prestamo, bd=2,
                                                      font=("Arial", 10), width=12, insertbackground="blue",
                                                      selectbackground="blue",
                                                      relief=tk.RIDGE)
            self.elementos.box_id_prestamo.place(x=410, y=20)
            self.elementos.box_id_prestamo.delete(0, tk.END)


            # ==== ETIQUETA AREA ====
            self.elementos.label_area = tk.Label(self.elementos.label_frame, text="Area", font=("Arial", 10, "bold"),
                                                 fg="black", bg="#E6F7FF")
            self.elementos.label_area.place(x=310, y=50)

            # =======combo box area=====
            self.elementos.box_area = ttk.Combobox(self.elementos.label_frame, values=self.opciones_area,
                                                   textvariable=self.elementos.area_variable, font=("Arial", 9),
                                                   width=10)
            self.elementos.box_area.place(x=410, y=50)

            # =========== ETIQUETA ID_EXPEDIENTE =============
            self.elementos.label_id_expediente = tk.Label(self.elementos.label_frame, text="ID_expediente",
                                                          font=("Arial", 10, "bold"),
                                                          fg="black", bg="#E6F7FF")
            self.elementos.label_id_expediente.place(x=520, y=20)

            # =====CAJA ID_expediente =========
            self.elementos.box_id_expediente = tk.Entry(self.elementos.label_frame,
                                                        textvariable=self.elementos.id_variable_expediente, bd=1,
                                                        font=("Arial", 10), width=12, insertbackground="blue",
                                                        selectbackground="blue",
                                                        relief=tk.SOLID)
            self.elementos.box_id_expediente.place(x=665, y=20)
            self.elementos.box_id_expediente.delete(0, tk.END)

            # ======== ETIQUETA ID_CONTRIBUYENTE ==============
            self.elementos.label_id_contribuyente = tk.Label(self.elementos.label_frame, text="NIT/CC contribuyente",
                                                             font=("Arial", 10, "bold"),
                                                             fg="black", bg="#E6F7FF")
            self.elementos.label_id_contribuyente.place(x=520, y=50)

            # =====CAJA ID_Contribuyente =========
            self.elementos.box_id_contribuyente = tk.Entry(self.elementos.label_frame,
                                                           textvariable=self.elementos.id_variable_contribuyente, bd=1,
                                                           font=("Arial", 10), width=12, insertbackground="blue",
                                                           selectbackground="blue",
                                                           relief=tk.SOLID)
            self.elementos.box_id_contribuyente.place(x=665, y=50)
            self.elementos.box_id_contribuyente.delete(0, tk.END)

            # BOTON BUSCAR
            self.elementos.boton_buscar = tk.Button(self.elementos.label_frame, text="BUSCAR",
                                                    font=("Arial", 10, "bold"), fg="black", bg="white",
                                                    bd=3,
                                                    relief=tk.GROOVE, width=7, height=1,
                                                    activebackground='blue', command=self.buscar_prestamos_filtrados)
            self.elementos.boton_buscar.place(x=800, y=25)

            # ====BOTON LIMPIAR CAJA ========
            self.elementos.boton_limpiar_cajas = tk.Button(self.elementos.label_frame, text="LIMPIAR",
                                                           font=("Arial", 10, "bold"), fg="black", bg="white",
                                                           bd=3,
                                                           relief=tk.GROOVE, width=7, height=1,
                                                           activebackground='blue',
                                                           command=self.limpiar_cajas_texto)
            self.elementos.boton_limpiar_cajas.place(x=880, y=25)


            # Boton atras
            self.elementos.boton_atras = tk.Button(self.ventana_principal, text="ATRAS", font=("Arial", 12, "bold"),
                                                   fg="black", bg="white", bd=4, relief=tk.GROOVE, width=15, height=2,
                                                   command=self.interfaz.atras)
            self.elementos.boton_atras.place(x=(self.ancho_pantalla - 250), y=(self.altura_pantalla - 150))

            # ===== TABLA ======
            # Crear Treeview

            style = ttk.Style()
            style.theme_use("alt")
            style.configure('Treeview.Heading', font=('Arial', 8, 'bold'))
            style.configure('Treeview', font=('Arial', 9))

            self.elementos.tree = ttk.Treeview(self.ventana_principal, columns=(
                'Nombre', 'NIT/CC', 'Nombre Auditor', 'Tipo', 'Proceso', 'ID_expe', 'ID_caja','Estado','Año','Id_prestamo',
                'fecha_entrega','Fecha_devolucion','Responsable','Area'),show='headings', height=18)
            self.elementos.tree.heading('Nombre', text='Nombre')
            self.elementos.tree.column('Nombre', width=250, anchor='center')
            self.elementos.tree.heading('NIT/CC', text='NIT/CC')
            self.elementos.tree.column('NIT/CC', width=80, anchor='center')
            self.elementos.tree.heading('Nombre Auditor', text='Nombre Auditor')
            self.elementos.tree.column('Nombre Auditor', width=100, anchor='center')
            self.elementos.tree.heading('Tipo', text='Tipo')
            self.elementos.tree.column('Tipo', width=80, anchor='center')
            self.elementos.tree.heading('Proceso', text='Proceso')
            self.elementos.tree.column('Proceso', width=90, anchor='center')
            self.elementos.tree.heading('ID_expe', text='ID_expe')
            self.elementos.tree.column('ID_expe', width=80, anchor='center')
            self.elementos.tree.heading('ID_caja', text='ID_caja')
            self.elementos.tree.column('ID_caja', width=70, anchor='center')
            self.elementos.tree.heading('Estado', text='Estado')
            self.elementos.tree.column('Estado', width=70, anchor='center')
            self.elementos.tree.heading('Año', text='Año')
            self.elementos.tree.column('Año', width=50, anchor='center')
            self.elementos.tree.heading('Id_prestamo', text='Id_prestamo')
            self.elementos.tree.column('Id_prestamo', width=80, anchor='center')
            self.elementos.tree.heading('fecha_entrega', text='fecha_entrega')
            self.elementos.tree.column('fecha_entrega', width=85, anchor='center')
            self.elementos.tree.heading('Fecha_devolucion', text='Fecha_devolucion')
            self.elementos.tree.column('Fecha_devolucion', width=95, anchor='center')
            self.elementos.tree.heading('Responsable', text='Responsable')
            self.elementos.tree.column('Responsable', width=85, anchor='center')
            self.elementos.tree.heading('Area', text='Area')
            self.elementos.tree.column('Area', width=85, anchor='center')

            self.elementos.tree.place(x=30, y=200)
            #  =======MOSTRAR DATOS  ===========
            self.mostrar_prestamos_activos()

            # Enlace del evento para seleccionar registros
            self.elementos.tree.bind("<<TreeviewSelect>>", self.selecionar_registro_tabla)

            # Crear barras de desplazamiento
            self.elementos.barra_desplazamiento_v = ttk.Scrollbar(self.ventana_principal, orient="vertical",
                                                                  command=self.elementos.tree.yview)
            self.elementos.barra_desplazamiento_v.place(x=1330, y=200, height=379)
            # Configurar el Treeview para usar las Scrollbars
            self.elementos.tree.configure(yscrollcommand=self.elementos.barra_desplazamiento_v.set)
            self.limpiar_cajas_texto()

        except Exception as e:

            # Si ocurre algún error, imprime un mensaje de error
            print("Error al mostrar consultas prestamos crud:", str(e))

    def fecha_selected(self, event):
        self.fecha_entrega_selected = True
        self.elementos.box_fecha_entrega.configure(state='readonly')
        print("fecha seleccionada", self.fecha_entrega_selected)

    def fecha1_selected(self, event):
        self.fecha_entrega1_selected = True
        self.elementos.box_fecha_entrega1.configure(state='readonly')
        print("fecha seleccionada 1",self.fecha_entrega1_selected)

    def fecha_entrega_focus_out(self, event):
        if not self.fecha_entrega_selected :
            self.elementos.box_fecha_entrega.delete(0, 'end')
        self.fecha_entrega_selected = False
        print("fecha seleccionada", self.fecha_entrega_selected)

    def fecha_entrega1_focus_out(self, event):
        if not self.fecha_entrega1_selected :
            self.elementos.box_fecha_entrega1.delete(0, 'end')
        self.fecha_entrega1_selected = False
        print("fecha seleccionada 1", self.fecha_entrega1_selected)

    def limpiar_cajas_texto(self):
        """
                Método para limpiar las cajas de texto en la interfaz gráfica.
                """
        self.elementos.box_fecha_entrega.configure(state='normal')
        self.elementos.box_fecha_entrega1.configure(state='normal')
        self.elementos.box_fecha_entrega.delete(0, 'end')
        self.elementos.box_fecha_entrega1.delete(0, 'end')
        self.elementos.box_id_prestamo.delete(0, tk.END)
        self.elementos.box_area.delete(0, tk.END)
        self.elementos.box_id_expediente.delete(0, tk.END)
        self.elementos.box_id_contribuyente.delete(0, tk.END)
        self.filtros = {}
        self.fecha_entrega_selected = False
        self.fecha_entrega1_selected = False

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

    def buscar_prestamos_filtrados(self):

        """
            Busca préstamos filtrados según los valores proporcionados en las cajas de texto.

            Esta función extrae los valores de las cajas de texto para diferentes campos, los valida y
            los agrega a un diccionario de filtros. Luego, llama a la función de búsqueda con los filtros
            y actualiza una tabla de resultados si se encuentran coincidencias.

            Campos utilizados:
            - fecha_entrega_inicial: Fecha inicial de entrega en formato 'YYYY-MM-DD'.
            - fecha_entrega_final: Fecha final de entrega en formato 'YYYY-MM-DD'.
            - id_prestamo: ID del préstamo, que debe ser un número.
            - area: Área del préstamo, que debe estar en la lista de opciones de área.
            - id_expediente: ID del expediente, que debe empezar por O, I o S.
            - id_contribuyente: ID del contribuyente, que debe ser un número.

            Si alguno de los campos tiene un valor, se procede con la validación y búsqueda; de lo contrario, se muestra un error.
            """

        fecha_entrega_inicial = self.elementos.box_fecha_entrega.get()
        print(fecha_entrega_inicial)
        fecha_entrega_final = self.elementos.box_fecha_entrega1.get()
        id_prestamo = self.elementos.box_id_prestamo.get().strip()
        area = self.elementos.box_area.get().strip()
        id_expediente = self.elementos.box_id_expediente.get().strip()
        id_contribuyente = self.elementos.box_id_contribuyente.get().strip()

        if (fecha_entrega_inicial or fecha_entrega_final or id_prestamo or area or id_expediente or id_contribuyente):

            try:
                # Validar y agregar al diccionario de filtros

                if fecha_entrega_inicial or fecha_entrega_final:
                    if fecha_entrega_inicial:
                        self.filtros['fecha_entrega_inicio'] = fecha_entrega_inicial
                    if fecha_entrega_final:
                        self.filtros['fecha_entrega_fin'] = fecha_entrega_final
                    if fecha_entrega_inicial and fecha_entrega_final:
                        fecha_entrega_inicial_date = datetime.strptime(fecha_entrega_inicial, '%Y-%m-%d').date()
                        fecha_entrega_final_date = datetime.strptime(fecha_entrega_final, '%Y-%m-%d').date()
                        if fecha_entrega_inicial_date > fecha_entrega_final_date:
                            raise ValueError(
                                "La fecha de entrega inicial no puede ser mayor que la fecha de entrega final.")

                if id_prestamo:
                    if not id_prestamo.isdigit():
                        raise ValueError("El id_prestamo debe ser un número.")
                    self.filtros['id_prestamo'] = id_prestamo

                if area:
                    if area not in self.opciones_area:
                        raise ValueError("Área no válida.")
                    self.filtros['area'] = area

                if id_expediente:
                    if id_expediente[0].upper() not in ['O', 'I', 'S']:
                        raise ValueError("ID del expediente debe empezar por O, I o S.")
                    self.filtros['id_expediente'] = id_expediente

                if id_contribuyente:
                    if not id_contribuyente.isdigit():
                        raise ValueError("ID del contribuyente debe comenzar con un número.")
                    self.filtros['id_contribuyente'] = id_contribuyente

                print("filtros",self.filtros)
                # Llamar a la función de búsqueda con los filtros
                mensaje, encabezados, resultados,confirmacion = self.consultas.buscar_prestamos_filtrados(self.filtros)

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

    def mostrar_prestamos_activos(self):
        try:
            #borrar elementos actuales del tree contribuyente
            # devuelve una lista de identificadores de elementos secundarios
            # , y el operador * se utiliza para pasar esos identificadores
            # como argumentos separados a la función delete.
            self.elementos.tree.delete(*self.elementos.tree.get_children())

        #obtener los nuevos datos que deseamos mostrar
            mensaje,encabezados,expedientes,confimacion = self.consultas.buscar_prestamos_activos()
            #print(contribuyentes)
        #insertar lo nuevos datos  en el tree
            # mostrar datos en la tabla
            if expedientes:
                for row in expedientes:
                    self.elementos.tree.insert("", "end", values=row)
            else:
                messagebox.showinfo("Información", "No hay datos disponibles para mostrar.")
                raise ValueError("La tabla expedientes esta vacia")

        except ValueError as error:
            print(f"fError al actualizar tabla : {error}")

