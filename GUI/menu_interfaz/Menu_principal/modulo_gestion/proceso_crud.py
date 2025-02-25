import tkinter as tk
import json
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import ttk
from consultas.consultas_proceso import ConsultasProceso
from entidades.proceso import Proceso


class ProcesoCrud:

    def __init__(self, ventana_principal, elementos, interfaz):
        """
                Constructor de la clase ProcesoCrud .

                Args:
                    ventana_principal: La ventana principal de la interfaz gráfica.
                    elementos: Objeto que contiene los elementos de la interfaz gráfica.
                    interfaz: Objeto que representa la interfaz gráfica en general.
                """
        self.ventana_principal = ventana_principal
        self.elementos = elementos
        self.interfaz = interfaz
        self.consultas_proceso = ConsultasProceso()
        self.proceso = Proceso()
        self.elementos.ventana_credenciales_abierta = False

    def mostrar_proceso_crud(self):
        """
                Método para mostrar la interfaz de gestión de proceso.
                """
        self.interfaz.estado_actual = "gestion_proceso_crud"
        print(self.interfaz.estado_actual)
        opciones_tipo = ["Omisos", "Inexactos","Sancionatorio","Omisos_R","Omisos_AR"]

        try:
            altura_pantalla = self.interfaz.window_height
            ancho_pantalla = self.interfaz.window_width

            # ==== TITULO ======
            self.elementos.label_titulo = tk.Label(self.ventana_principal, text="GESTIÓN DE PROCESOS",
                                                   font=("Arial", 30, "bold"), fg="black", bg="#E6F7FF")

            self.elementos.label_titulo.pack(pady=20)  # pady añade un espacio en la parte inferior de la etiqueta
            # ====LABEL IFRAME====
            self.elementos.label_frame = tk.LabelFrame(self.ventana_principal, text="DATOS DEL PROCESO",
                                                       font=("Arial", 20, "bold"), fg="black", bg="#E6F7FF", bd=5,
                                                       relief=tk.RIDGE)
            self.elementos.label_frame.place(x=55, y=100, width=500, height=300)

            # =====ETIQUETA ID_proceso ======
            self.elementos.label_id_proceso = tk.Label(self.elementos.label_frame, text="ID_proceso", font=("Arial", 12, "bold"),
                                               fg="black", bg="#E6F7FF")
            self.elementos.label_id_proceso.place(x=45, y=30)

            # =====CAJA ID_proceso =========
            self.elementos.box_id_proceso = tk.Entry(self.elementos.label_frame, textvariable=self.elementos.id_variable_proceso, bd=3,
                                             font=("Arial", 12), width=15, insertbackground="blue", selectbackground="blue",
                                             relief=tk.RIDGE)
            self.elementos.box_id_proceso.place(x=145, y=30)
            self.elementos.box_id_proceso.delete(0, tk.END)  # Borra el contenido actual de la caja de texto self.box_id

            # ==== ETIQUETA nombre_proceso ====
            self.elementos.label_tipo = tk.Label(self.elementos.label_frame, text="Tipo", font=("Arial", 12, "bold"),
                                                   fg="black", bg="#E6F7FF")
            self.elementos.label_tipo.place(x=45, y=60)
            # ==== box tipo ====
            self.elementos.box_tipo = ttk.Combobox(self.elementos.label_frame, values=opciones_tipo, state="readonly",
                                                   textvariable=self.elementos.tipo_variable, font=("Arial", 12),
                                                   width=14)
            self.elementos.box_tipo.place(x=145, y=60)
            self.elementos.box_tipo.set('')

            # ====== BOTON INSERTAR =====
            self.elementos.boton_insertar = tk.Button(self.elementos.label_frame, text="Insertar", font=("Arial", 12, "bold"),
                                                     fg="black", bg="white", bd=4, relief=tk.GROOVE, width=7, height=1,
                                                     activebackground='blue', command=self.insertar_proceso)
            self.elementos.boton_insertar.place(x=50, y=170)
            # ===== BOTON MODIFICAR ====
            self.elementos.boton_modificar = tk.Button(self.elementos.label_frame, text="Modificar",
                                                       font=("Arial", 12, "bold"), fg="black", bg="white", bd=4,
                                                       relief=tk.GROOVE, width=7, height=1, activebackground='blue',
                                                       command=self.modificar_proceso)
            self.elementos.boton_modificar.place(x=150, y=170)
            # ===== BOTON ELIMINAR =====
            self.elementos.boton_eliminar = tk.Button(self.elementos.label_frame, text="Eliminar",
                                                      font=("Arial", 12, "bold"), fg="black", bg="white", bd=4,
                                                      relief=tk.GROOVE, width=7, height=1, activebackground='blue',
                                                      command=self.eliminar_proceso)
            self.elementos.boton_eliminar.place(x=250, y=170)

            # ====BOTON LIMPIAR CAJA ========
            self.elementos.boton_limpiar_cajas = tk.Button(self.elementos.label_frame, text="LIMPIAR",
                                                      font=("Arial", 12, "bold"), fg="black", bg="white", bd=4,
                                                      relief=tk.GROOVE, width=7, height=1, activebackground='blue',
                                                      command=self.limpiar_cajas_texto)
            self.elementos.boton_limpiar_cajas.place(x=(500-100), y=(300-90))

            # ======BOTON CAMBIAR ID =========

            self.elementos.boton_cambiar_id = tk.Button(self.ventana_principal, text="Cambiar ID_proceso",
                                                      font=("Arial", 12, "bold"), fg="black", bg="red", bd=4,
                                                      relief=tk.GROOVE, width=15, height=1, activebackground='blue',
                                                      command=self.crear_ventana_credenciales_cambiar_id_proceso)
            self.elementos.boton_cambiar_id.place(x=55,y=450)

            # ===== TABLA ======
            # Crear Treeview

            style = ttk.Style()
            style.theme_use("alt")
            style.configure('Treeview.Heading', font=('Arial', 12, 'bold'))
            style.configure('Treeview', font=('Arial', 12))

            self.elementos.tree = ttk.Treeview(self.ventana_principal, columns=('ID_PROCESO', 'NOMBRE_PROCESO'), show='headings',height=10)
            self.elementos.tree.heading('ID_PROCESO', text='ID_PROCESO')
            self.elementos.tree.column('ID_PROCESO', width=110, anchor='center')
            self.elementos.tree.heading('NOMBRE_PROCESO', text='NOMBRE_PROCESO')
            self.elementos.tree.column('NOMBRE_PROCESO', width=430, anchor='center')

            self.elementos.tree.place(x=((ancho_pantalla/2)-30), y=110)
            #  =======MOSTRAR DATOS  ===========
            self.actualizar_tree_proceso()
            # Enlace del evento para seleccionar registros
            self.elementos.tree.bind("<<TreeviewSelect>>", self.selecionar_registro_proceso)

            # Boton atras
            self.elementos.boton_atras = tk.Button(self.ventana_principal, text="ATRAS", font=("Arial", 12, "bold"),
                                                   fg="black", bg="white", bd=4, relief=tk.GROOVE, width=15, height=2,
                                                   command=self.interfaz.atras)
            self.elementos.boton_atras.place(x=(ancho_pantalla - 250), y=(altura_pantalla - 150))
        except Exception as e:
            # Si ocurre algún error, imprime un mensaje de error
            print("Error al mostrar gestion auditor:", str(e))

    def actualizar_tree_proceso(self):
        """
                Método para actualizar la tabla de procesos en la interfaz gráfica.
                """
        try:
            #borrar elementos actuales del tree contribuyente
            # devuelve una lista de identificadores de elementos secundarios
            # , y el operador * se utiliza para pasar esos identificadores
            # como argumentos separados a la función delete.
            self.elementos.tree.delete(*self.elementos.tree.get_children())

        #obtener los nuevos datos que deseamos mostrar
            mensaje, procesos = self.consultas_proceso.mostrar_procesos()
            #print(contribuyentes)
        #insertar lo nuevos datos  en el tree
            # mostrar datos en la tabla
            if procesos:
                for row in procesos:
                    self.elementos.tree.insert("", "end", values=row)
            else:
                messagebox.showinfo("Información", "No hay datos disponibles para mostrar.")
                raise ValueError("La tabla procesos esta vacia")
        except ValueError as error:
            print(f"fError al actualizar tabla : {error}")

    def selecionar_registro_proceso(self, event):
        """
                Método para seleccionar un registro de la tabla de procesos.

                Args:
                    event: Evento que activa la selección de un registro.
                """
        try:
            itemseleccionado = self.elementos.tree.focus()
            if itemseleccionado:
                self.elementos.box_id_proceso.config(state=tk.NORMAL)
                #obtener valores
                values = self.elementos.tree.item(itemseleccionado)['values']
                #establecer los valores en los widgests entry
                self.elementos.box_id_proceso.delete(0, tk.END)
                self.elementos.box_id_proceso.insert(0, values[0])
                self.elementos.box_tipo.set(values[1])

                # Deshabilitar el botón "Insertar" y self.elementos.box_id
                self.elementos.boton_insertar.config(state=tk.DISABLED)
                self.elementos.box_id_proceso.config(state=tk.DISABLED)

        except ValueError as error:
            print(f"fError al seleccionar registro : {error}")

    def limpiar_cajas_texto(self):
        """
                Método para limpiar las cajas de texto en la interfaz gráfica.
                """
        # Verificar si el botón "Insertar" y la entrada box_id están deshabilitados
        if self.elementos.boton_insertar['state'] == tk.DISABLED and self.elementos.box_id_proceso['state'] == tk.DISABLED:

            # Habilitar el botón "Insertar" y la entrada box_id
            self.elementos.boton_insertar.config(state=tk.NORMAL)
            self.elementos.box_id_proceso.config(state=tk.NORMAL)

        self.elementos.box_id_proceso.delete(0, tk.END)
        self.elementos.box_tipo.delete(0, tk.END)

    def insertar_proceso(self):
        """
                Método para insertar un nuevo proceso en la base de datos.
                """
        id_proceso = self.elementos.box_id_proceso.get().strip()
        nombre_proceso = self.elementos.box_tipo.get().strip()

        if id_proceso and nombre_proceso:
            try:
                # Convertir id_auditor a cadena y verificar que contenga solo números
                if id_proceso[0] not in "0123456789":
                    raise ValueError("ID del contribuyente debe comenzar con un numero.")
                elif nombre_proceso not in ["Omisos", "Inexactos", "Omisos_R", "Omisos_AR", "Sancionatorio"]:
                    raise ValueError("El tipo de contribuyente debe ser uno de la lista'.")

                mensaje, confirmacion = self.proceso.insertar_proceso(id_proceso, nombre_proceso)

                if confirmacion:
                    messagebox.showinfo("INFORMACIÓN", "El Proceso fue agregado correctamente")
                    print(mensaje)
                else:
                    messagebox.showinfo("INFORMACIÓN", mensaje)
                    print(mensaje)

                # actualizamos los campos del tree
                self.actualizar_tree_proceso()
                # LIMPIAR CAMPOS
                self.limpiar_cajas_texto()

            except ValueError as error:
                # Verificar si el error es debido a un no dígito en id_auditor
                if "ID del proceso debe comenzar con un numero." in str(error):

                    messagebox.showerror("Error", "ID del proceso debe comenzar con un numero.")
                    # Borrar el contenido de la caja de texto id_auditor

                # Verificar si el error es debido a la conexión a la base de datos
                elif "Error al conectar a la base de datos" in str(error):
                    messagebox.showerror("Error de conexión", "No se pudo conectar a la base de datos.")
                else:
                    messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Error", "Todas las cajas de texto deben tener un valor.")

    def eliminar_proceso(self):
        """
                Método para eliminar un proceso de la base de datos.
                """
        id_proceso = self.elementos.box_id_proceso.get().strip()
        # Verificar si ambas cajas de texto tienen un valor
        if id_proceso:
            try:
                if id_proceso[0] not in "0123456789":
                    raise ValueError("ID del proceso debe comenzar con un numero.")

                mensaje, confirmacion = self.proceso.eliminar_proceso(id_proceso)

                if confirmacion:
                    messagebox.showinfo("INFORMACIÓN", "los datos fueron Elimninados")
                    print(mensaje)
                else:
                    messagebox.showinfo("INFORMACIÓN", mensaje)
                    print(mensaje)

                # actualizamos los campos del tree
                self.actualizar_tree_proceso()
                # LIMPIAR CAMPOS
                self.limpiar_cajas_texto()
            except ValueError as error:
                # Verificar si el error es debido a un no dígito en id_auditor
                if "ID del proceso debe comenzar con un numero" in str(error):

                    messagebox.showerror("Error", "ID del proceso debe comenzar con un numero")
                    # Borrar el contenido de la caja de texto id_auditor

                # Verificar si el error es debido a la conexión a la base de datos
                elif "Error al conectar a la base de datos" in str(error):
                    messagebox.showerror("Error de conexión", "No se pudo conectar a la base de datos.")
                else:
                    messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Error", "la caja de texto id_proceso debe tener un valor.")

    def modificar_proceso(self):
        """
                Método para modificar los datos de un proceso en la base de datos.
                """
        id_proceso = self.elementos.box_id_proceso.get().strip()
        nuevo_nombre_proceso = self.elementos.box_tipo.get().strip()

        if id_proceso and nuevo_nombre_proceso:
            try:
                # Convertir id_auditor a cadena y verificar que contenga solo números
                if id_proceso[0] not in "0123456789":
                    raise ValueError("ID del contribuyente debe comenzar con un numero.")
                elif nuevo_nombre_proceso not in ["Omisos", "Inexactos","sancionatorio","Omisos_R","Omisos_AR"]:
                    raise ValueError("El tipo de contribuyente debe ser uno de la lista'.")

                mensaje, confirmacion = self.proceso.modificar_datos_proceso(id_proceso, nuevo_nombre_proceso)

                if confirmacion:
                    messagebox.showinfo("INFORMACIÓN", "El Proceso fue modificado correctamente")
                    print(mensaje)
                else:
                    messagebox.showinfo("INFORMACIÓN", mensaje)
                    print(mensaje)

                # actualizamos los campos del tree
                self.actualizar_tree_proceso()
                # LIMPIAR CAMPOS
                self.limpiar_cajas_texto()

            except ValueError as error:
                # Verificar si el error es debido a un no dígito en id_auditor
                if "ID del proceso debe comenzar con un numero." in str(error):

                    messagebox.showerror("Error", "ID del proceso debe comenzar con un numero.")
                    # Borrar el contenido de la caja de texto id_auditor

                # Verificar si el error es debido a la conexión a la base de datos
                elif "Error al conectar a la base de datos" in str(error):
                    messagebox.showerror("Error de conexión", "No se pudo conectar a la base de datos.")
                else:
                    messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Error", "Todas las cajas de texto deben tener un valor.")

    def modificar_id_proceso(self):
        """
                Método para modificar el ID de un proceso en la base de datos.
                """
        id_antiguo = self.elementos.box_antiguo_id.get().strip()
        id_nuevo = self.elementos.box_nuevo_id.get().strip()
        print(id_antiguo, id_nuevo)
        # Verificar si ambas cajas de texto tienen un valor
        if id_antiguo and id_nuevo:
            try:
                if id_antiguo[0] not in "0123456789":
                    raise ValueError("ID antiguo debe comenzar con un numero.")
                if id_nuevo[0] not in "0123456789":
                    raise ValueError("ID nuevo debe comenzar con un numero.")
                mensaje, confirmacion = self.proceso.modificar_id_proceso(id_antiguo, id_nuevo)

                if confirmacion:
                    messagebox.showinfo("INFORMACIÓN", "los datos fueron Actualizados")
                    print(mensaje)
                else:
                    messagebox.showinfo("INFORMACIÓN", mensaje)
                    print(mensaje)

                # actualizamos los campos del tree
                self.actualizar_tree_proceso()
                # LIMPIAR CAMPOS
                self.limpiar_cajas_texto()

            except ValueError as error:
                # Verificar si el error es debido a un no dígito en id_auditor
                if " EL ID antiguo debe comenzar con un numero" in str(error):

                    messagebox.showerror("Error", "EL ID antiguo debe comenzar con un numero.")
                    # Borrar el contenido de la caja de texto id_auditor
                elif"ID nuevo debe comenzar con un numero" in str(error):

                    messagebox.showerror("Error", "ID nuevo debe comenzar con un numero.")
                    # Borrar el contenido de la caja de texto id_auditor
                # Verificar si el error es debido a la conexión a la base de datos
                elif "Error al conectar a la base de datos" in str(error):
                    messagebox.showerror("Error de conexión", "No se pudo conectar a la base de datos.")
                else:
                    messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Error", "Todas las cajas de texto deben tener un valor.")

    def cambiar_id_proceso(self):
        """
                Método para cambiar el ID de un proceso en la interfaz gráfica.
                """
        self.interfaz.estado_actual = "g_p_c_cambiar_id_proceso" # gestion_proceso_crud
        print(self.interfaz.estado_actual)

        # desabilitar botones y cajas
        self.elementos.boton_insertar.config(state=tk.DISABLED)
        self.elementos.boton_eliminar.config(state=tk.DISABLED)
        self.elementos.boton_modificar.config(state=tk.DISABLED)
        self.elementos.boton_limpiar_cajas.config(state=tk.DISABLED)
        self.elementos.boton_atras.config(state=tk.DISABLED)

        self.elementos.box_id_proceso.config(state=tk.DISABLED)
        self.elementos.box_tipo.config(state=tk.DISABLED)

        # ===== ETIQUETA ANTIGUO_ID =======
        self.elementos.label_antiguo_id = tk.Label(self.ventana_principal, text="ID_antiguo", font=("Arial", 12, "bold"),
                                           fg="black", bg="#E6F7FF")
        self.elementos.label_antiguo_id.place(x=55,y=510)
        # ======CAJA ANTIGUO ID ========
        self.elementos.box_antiguo_id = tk.Entry(self.ventana_principal, textvariable=self.elementos.antiguo_id_variable,
                                             bd=3, font=("Arial", 12), width=10, insertbackground="blue",
                                             selectbackground="blue", relief=tk.RIDGE)
        self.elementos.box_antiguo_id.place(x=55, y=540)
        self.elementos.box_antiguo_id.delete(0, tk.END)

        # ===== ETIQUETA NUEVO_ID =======
        self.elementos.label_nuevo_id = tk.Label(self.ventana_principal, text="ID_nuevo",
                                                   font=("Arial", 12, "bold"),
                                                   fg="black", bg="#E6F7FF")
        self.elementos.label_nuevo_id.place(x=170, y=510)
        # ======CAJA NUEVO ID ========
        self.elementos.box_nuevo_id = tk.Entry(self.ventana_principal, textvariable=self.elementos.nuevo_id_variable,
                                                 bd=3, font=("Arial", 12), width=10, insertbackground="blue",
                                                 selectbackground="blue", relief=tk.RIDGE)
        self.elementos.box_nuevo_id.place(x=170, y=540)
        self.elementos.box_nuevo_id.delete(0, tk.END)

        # ===== BOTON ACEPTAR ======
        self.elementos.boton_aceptar = tk.Button(self.ventana_principal, text="ACEPTAR", font=("Arial", 12, "bold"),
                                               fg="black", bg="white", bd=4, relief=tk.GROOVE, width=9, height=1,
                                               command= self.modificar_id_proceso)
        self.elementos.boton_aceptar.place(x=55, y=580)

        # ====== BOTON CANCELAR =======
        self.elementos.boton_cancelar = tk.Button(self.ventana_principal, text="CANCELAR", font=("Arial", 12, "bold"),
                                                 fg="black", bg="white", bd=4, relief=tk.GROOVE, width=9, height=1,
                                                 command=self.interfaz.atras)
        self.elementos.boton_cancelar.place(x=170, y=580)

    def crear_ventana_credenciales_cambiar_id_proceso(self):
        """
                Método para crear la ventana de credenciales para cambiar el ID del proceso.
                """
        if not self.elementos.ventana_credenciales_abierta or not self.elementos.ventana_credenciales.winfo_exists():

            # desabilitar botones y cajas
            self.elementos.boton_insertar.config(state=tk.DISABLED)
            self.elementos.boton_eliminar.config(state=tk.DISABLED)
            self.elementos.boton_modificar.config(state=tk.DISABLED)
            self.elementos.boton_limpiar_cajas.config(state=tk.DISABLED)
            self.elementos.boton_atras.config(state=tk.DISABLED)

            self.elementos.box_id_proceso.config(state=tk.DISABLED)
            self.elementos.box_tipo.config(state=tk.DISABLED)

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
                                                     textvariable=contraseña_var) # Muestra asteriscos para la contraseña
            self.elementos.entry_password_admin.pack()

            # Crea un botón para iniciar sesión
            login_button = tk.Button(self.elementos.ventana_credenciales, text="Iniciar Sesión", command=lambda: self.interfaz.verificar_credenciales("gestion_proceso_crud"))
            login_button.pack()
            # Después de crear la ventana, establece la bandera a True
            self.elementos.ventana_credenciales_abierta = True
            self.elementos.ventana_credenciales.protocol("WM_DELETE_WINDOW", self.cerrar_ventana_credenciales_proceso)
        else:
            self.elementos.ventana_credenciales.focus_force()  # Enfoca la ventana existente para mostrarla en la

    def cerrar_ventana_credenciales_proceso(self):
        """
                Método para cerrar la ventana de credenciales de proceso.
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

        self.elementos.box_id_proceso.config(state=tk.NORMAL)
        self.elementos.box_tipo.config(state=tk.NORMAL)
