import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import ttk
from entidades.auditor import *
from GUI.elementos import Elementos



class Menu():
    def __init__(self):
        try:

            self.ventana_inicio = tk.Tk()

            # instacia de clase
            self.auditor = Auditor()
            self.elementos = Elementos()

            self.ventana_principal = None
            self.crear_ventana_inicio(self.ventana_inicio)

            self.estado_actual = None  # indica el estado actual de la interfaz

        except ValueError as error:
            print("Error al mostrar la interfaz,error:{}".format(error))

    def crear_ventana_inicio(self, ventana_inicio):
        usuario_por_defecto = "ARCHIVO"
        contrasena_por_defecto = "Fisca2024"
        ventana_inicio.title("Inicio de Sesión")
        ventana_inicio.geometry("300x150")

        # Centrar la ventana en la pantalla
        inicio_width = ventana_inicio.winfo_screenwidth()  # ancho de la ventana requerido gracias a la funcion .winfo_reqwidth()
        inicio_height = ventana_inicio.winfo_screenheight()  # alto de la ventana requerido gracias a la funcion .winfo_reqheight()
        winicio = 300
        hinicio = 150
        inicio_position_right = int(inicio_width / 2 - winicio / 2)  # posicion de la ventana la funcion winfo_screenwidth() determina el ancho de la pantalla
        inicio_position_down = int(inicio_height / 2 - hinicio / 2)  # posicion de la ventana la funcion winfo_screenheight() determina el alto de la pantalla
        ventana_inicio.geometry("+{}+{}".format(inicio_position_right,inicio_position_down))  # los valores position_right, position_down van en los corchet

        # Agrega widgets para el usuario y la contraseña
        label_user = tk.Label(ventana_inicio, text="Usuario:")
        label_user.pack()
        usuario_var = tk.StringVar(value=usuario_por_defecto)

        self.elementos.entry_user = tk.Entry(ventana_inicio, textvariable=usuario_var)
        self.elementos.entry_user.pack()

        label_password = tk.Label(ventana_inicio, text="Contraseña:")
        label_password.pack()
        contraseña_var = tk.StringVar(value=contrasena_por_defecto)

        self.elementos.entry_password = tk.Entry(ventana_inicio, show="*", textvariable=contraseña_var) # Muestra asteriscos para la contraseña
        self.elementos.entry_password.pack()

        # Crea un botón para iniciar sesión
        login_button = tk.Button(ventana_inicio, text="Iniciar Sesión", command=self.verificar_credenciales)
        login_button.pack()

    def crear_ventana_principal(self):
        # ==========================================VENTANA===========================================================
        self.ventana_principal = tk.Tk()
        self.ventana_principal.title("ARCHIVO DE FISCALIZACIÓN")
        self.ventana_principal.geometry('1080x600')
        self.ventana_principal.minsize(600, 400)
        self.ventana_principal.resizable(width=False, height=False)

        # Centrar la ventana en la pantalla
        window_width = self.ventana_principal.winfo_screenwidth()  # ancho de la ventana requerido gracias a la funcion .winfo_reqwidth()
        window_height = self.ventana_principal.winfo_screenheight()  # alto de la ventana requerido gracias a la funcion .winfo_reqheight()
        wventana = 1080
        hventana = 600
        position_right = int(window_width / 2 - wventana / 2)  # posicion de la ventana la funcion winfo_screenwidth() determina el ancho de la pantalla
        position_down = int(window_height / 2 - hventana / 2)  # posicion de la ventana la funcion winfo_screenheight() determina el alto de la pantalla
        self.ventana_principal.geometry("+{}+{}".format(position_right, position_down))  # los valores position_right, position_down van en los corchetes gracias a la funcion .format
        self.ventana_principal.configure(bg='#E6F7FF')
        self.set_estado_actual("menu principal")
        self.ventana_principal.mainloop()  # asigno el nuevo mainloo() que sera el hilo principal de la interfaz

    def verificar_credenciales(self):
        # Obtiene el usuario y la contraseña ingresados por el usuario

        usuario = self.elementos.entry_user.get()
        contrasena = self.elementos.entry_password.get()

        # Verifica las credenciales (puedes personalizar esto)
        if usuario == "ARCHIVO" and contrasena == "Fisca2024":
            # Si las credenciales son correctas, cierra la ventana de inicio de sesión y muestra la ventana principal
            self.ventana_inicio.destroy()
            self.crear_ventana_principal()
        else:
            # Si las credenciales son incorrectas, muestra un mensaje de error
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")


    def atras(self): # CONDICIONES SI SE OPRIME EL BOTON REGRESAR
        if self.estado_actual == "consulta": # si esta en el estado consulta
            self.borrar_estado_anterior("consulta") # borra el estado consulta
            self.set_estado_actual("menu principal") # pasa al estado menu principal
        if self.estado_actual == "gestion":
            self.borrar_estado_anterior("gestion")
            self.set_estado_actual("menu principal")
        if self.estado_actual == "gestion auditor":
            self.borrar_estado_anterior("gestion auditor")
            self.set_estado_actual("gestion")

    def borrar_estado_anterior(self,estado_anterior): # borra los elementos del estado en el estaba antes de dar click

        if estado_anterior == "menu principal":
            self.elementos.label_titulo.destroy()
            self.elementos.boton_consultar.destroy()
            self.elementos.boton_gestion.destroy()
            self.elementos.boton_inventario.destroy()
        if estado_anterior == "consulta":
            self.elementos.label_titulo.destroy()
            self.elementos.boton_atras.destroy()
        if estado_anterior == "gestion":
            self.elementos.label_titulo.destroy()
            self.elementos.boton_auditor.destroy()
            self.elementos.boton_atras.destroy()
        if estado_anterior == "gestion auditor":
            self.elementos.label_titulo.destroy()
            self.elementos.boton_atras.destroy()
            self.elementos.label_frame.destroy()
            self.elementos.label_id.destroy()
            self.elementos.label_nombre.destroy()
            self.elementos.box_id.destroy()
            self.elementos.box_nombre.destroy()
            self.elementos.boton_guardar.destroy()
            self.elementos.boton_modificar.destroy()
            self.elementos.boton_eliminar.destroy()
            self.elementos.tree.destroy()


    def set_estado_actual(self, estado):# esta funcion le indica a la interfaz en que estado debe estar segun la logica del proceso
        if estado == "menu principal": #INDICA EL ESTADO MENU INICIAL
            self.estado_actual = "menu principal"
            # Etiqueta centrada en la parte superior
            self.elementos.label_titulo = tk.Label(self.ventana_principal, text="ARCHIVO DE FISCALIZACIÓN", font=("Arial", 30, "bold"),fg="black", bg="#E6F7FF")
            self.elementos.label_titulo.pack(pady=20)  # pady añade un espacio en la parte inferior de la etiqueta

            # Botones centrados horizontalmente
            #======BOTON CONSULTAR========
            self.elementos.boton_consultar = tk.Button(self.ventana_principal, text="Consultar", font=("Arial", 20, "bold"), fg="black",bg="white", bd=4, relief=tk.GROOVE, width=300, height=150,command=self.on_boton_consultar)
            self.elementos.boton_consultar.place(x=50, y=210)
            self.elementos.imagen_consultar = PhotoImage(file="D:\pythonProject\Crud_fisca_archivo\imagenes\consultar.png")
            self.elementos.imagen_consultar = self.elementos.imagen_consultar.subsample(10)  # Ajusta el factor de reducción según sea necesario
            self.elementos.boton_consultar.config(image=self.elementos.imagen_consultar, compound="bottom")

            #======BOTON REGISTRAR MODIFICAR====
            self.elementos.boton_gestion = tk.Button(self.ventana_principal, text="Gestión", font=("Arial", 20, "bold"), fg="black",bg="white", bd=4, relief=tk.GROOVE, width=300, height=150,command=self.on_boton_registrar_modificar)
            self.elementos.boton_gestion.place(x=390, y=210)
            self.elementos.imagen_gestion = PhotoImage(file="D:\pythonProject\Crud_fisca_archivo\imagenes\egistro.png")
            self.elementos.imagen_gestion = self.elementos.imagen_gestion.subsample(6)  # Ajusta el factor de reducción según sea necesario
            self.elementos.boton_gestion.config(image= self.elementos.imagen_gestion,compound="bottom")

            # ======BOTON INVENTARIO====
            self.elementos.boton_inventario = tk.Button(self.ventana_principal, text="Inventario Gráfico", font=("Arial", 20, "bold"),fg="black", bg="white", bd=4, relief=tk.GROOVE, width=300, height=150)
            self.elementos.boton_inventario.place(x=730, y=210)
            self.elementos.imagen_inventario = PhotoImage(file="D:\pythonProject\Crud_fisca_archivo\imagenes\inventario.png")
            self.elementos.imagen_inventario = self.elementos.imagen_inventario.subsample(6)  # Ajusta el factor de reducción según sea necesario
            self.elementos.boton_inventario.config(image=self.elementos.imagen_inventario, compound="bottom")

        if estado == "consulta":
            self.estado_actual = "consulta"
            # Etiqueta centrada en la parte superior
            self.elementos.label_titulo = tk.Label(self.ventana_principal, text="Seleccione el tipo de busqueda", font=("Arial", 30, "bold"),fg="black", bg="#E6F7FF")
            self.elementos.label_titulo.pack(pady=20)  # pady añade un espacio en la parte inferior de la etiqueta

            self.elementos.boton_atras = tk.Button(self.ventana_principal, text="ATRAS", font=("Arial", 12, "bold"),fg="black", bg="white", bd=4, relief=tk.GROOVE, width=15, height=2,command=self.atras)
            self.elementos.boton_atras.place(x=900, y=500)

        if estado == "gestion": # menu registrar modificar
            self.estado_actual = "gestion"
            # Boton atras
            self.elementos.boton_atras = tk.Button(self.ventana_principal, text="ATRAS", font=("Arial", 12, "bold"), fg="black", bg="white",bd=4, relief=tk.GROOVE, width=15, height=2, command=self.atras)
            self.elementos.boton_atras.place(x=900, y=500)

            # Etiqueta centrada en la parte superior
            self.elementos.label_titulo = tk.Label(self.ventana_principal, text="QUE DESEA REGISTRAR O MODIFICAR", font=("Arial", 30, "bold"),fg="black", bg="#E6F7FF")
            self.elementos.label_titulo.pack(pady=20)  # pady añade un espacio en la parte inferior de la etiqueta
            # boton auditor
            self.elementos.boton_auditor = tk.Button(self.ventana_principal, text="Auditor", font=("Arial", 20, "bold"), fg="black",bg="white", bd=4, relief=tk.GROOVE, width=300, height=150,command=self.on_boton_auditor)
            self.elementos.boton_auditor.place(x=50, y=210)
            self.elementos.imagen_auditor = PhotoImage(file="D:\pythonProject\Crud_fisca_archivo\imagenes\Auditor.png")
            self.elementos.imagen_auditor = self.elementos.imagen_auditor.subsample(5)  # Ajusta el factor de reducción según sea necesario
            self.elementos.boton_auditor.config(image=self.elementos.imagen_auditor, compound="bottom")

        if estado == "gestion auditor":
            self.estado_actual = "gestion auditor"
            #titulo
            self.elementos.label_titulo = tk.Label(self.ventana_principal, text="GESTIÓN DE AUDITORES", font=("Arial", 30, "bold"),fg="black", bg="#E6F7FF")
            self.elementos.label_titulo.pack(pady=20)  # pady añade un espacio en la parte inferior de la etiqueta
            # LABEL IFRAME
            self.elementos.label_frame = tk.LabelFrame(self.ventana_principal, text="DATOS DEL AUDITOR", font=("Arial", 20, "bold"),fg="black", bg="#E6F7FF", bd=5, relief=tk.RIDGE)
            self.elementos.label_frame.place(x=50, y=100, width=500, height=300)
            #etiqueta id
            self.elementos.label_id = tk.Label(self.elementos.label_frame, text="ID", font=("Arial", 15, "bold"),fg="black", bg="#E6F7FF")
            self.elementos.label_id.place(x=50, y=50)
            # caja id
            self.elementos.box_id = tk.Entry(self.elementos.label_frame,textvariable=self.elementos.id_variable,bd=3, font=("Arial", 12), width=15, insertbackground="blue", selectbackground="blue",relief=tk.RIDGE)
            self.elementos.box_id.place(x=140,y=50)
            self.elementos.box_id.delete(0, tk.END)  # Borra el contenido actual de la caja de texto self.box_id
            #etiqueta nombre
            self.elementos.label_nombre = tk.Label(self.elementos.label_frame, text="Nombre", font=("Arial", 15, "bold"),fg="black", bg="#E6F7FF")
            self.elementos.label_nombre.place(x=50, y=90)
            #caja nombre
            self.elementos.box_nombre = tk.Entry(self.elementos.label_frame, textvariable=self.elementos.nombre_variable,bd=3, font=("Arial", 12), width=35, insertbackground="blue", selectbackground="blue",relief=tk.RIDGE)
            self.elementos.box_nombre.place(x=140,y=90)
            self.elementos.box_nombre.delete(0, tk.END)  # Borra el contenido actual de la caja de texto self.elementos.box_nombre
            #boton guardar
            self.elementos.boton_guardar = tk.Button(self.elementos.label_frame, text="Guardar", font=("Arial", 12, "bold"), fg="black",bg="white", bd=4, relief=tk.GROOVE, width=7, height=1,activebackground='blue',command=self.insertar_auditor)
            self.elementos.boton_guardar.place(x=50, y=170)
            #boton modificar
            self.elementos.boton_modificar = tk.Button(self.elementos.label_frame, text="Modificar", font=("Arial", 12, "bold"), fg="black",bg="white", bd=4, relief=tk.GROOVE, width=7, height=1,activebackground='blue',command=self.modificar_auditor)
            self.elementos.boton_modificar.place(x=150, y=170)
            #boton eliminar
            self.elementos.boton_eliminar = tk.Button(self.elementos.label_frame, text="Eliminar", font=("Arial", 12, "bold"), fg="black",bg="white", bd=4, relief=tk.GROOVE, width=7, height=1,activebackground='blue',command=self.eliminar_auditor)
            self.elementos.boton_eliminar.place(x=250, y=170)
            # TABLA
            # Crear Treeview
            self.elementos.tree = ttk.Treeview(self.ventana_principal, columns=('ID_AUDITOR', 'NOMBRE'), show='headings',height=15)
            self.elementos.tree.heading('ID_AUDITOR', text='ID_AUDITOR')
            self.elementos.tree.column('ID_AUDITOR', anchor='center')
            self.elementos.tree.heading('NOMBRE', text='NOMBRE')
            self.elementos.tree.column('NOMBRE', anchor='center')

            self.elementos.tree.place(x=600,y=120)
            style = ttk.Style()
            style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
            style.configure("Treeview", rowheight=25, font=('Arial', 10), highlightthickness=2, bd=2)
            # mostrar datos en la tabla
            for row in self.auditor.mostrar_auditores():
                self.elementos.tree.insert("","end",values=row)
            # ejecutar la funcion de hacer click y y mostrar el resultado en als cajas
            self.elementos.tree.bind("<<TreeviewSelect>>", self.selecionar_registro_auditor)

            # Boton atras
            self.elementos.boton_atras = tk.Button(self.ventana_principal, text="ATRAS", font=("Arial", 12, "bold"), fg="black", bg="white",bd=4, relief=tk.GROOVE, width=15, height=2, command=self.atras)
            self.elementos.boton_atras.place(x=900, y=530)

    #============== FUNCIONES CRUD AUDITOR =====================
    def insertar_auditor(self):
        id_auditor = self.elementos.box_id.get().strip()
        nombre_auditor = self.elementos.box_nombre.get().strip()
        # Verificar si ambas cajas de texto tienen un valor
        if id_auditor and nombre_auditor:
            try:
                # Convertir id_auditor a cadena y verificar que contenga solo números
                if not str(id_auditor).isdigit():
                    raise ValueError("ID del auditor debe contener solo números.")

                self.auditor = Auditor()
                self.auditor.insertar_auditor(id_auditor, nombre_auditor)

                messagebox.showinfo("INFORMACIÓN","los datos fueron guardados")
                # actualizamos los campos del tree
                self.actualizar_tree_auditor()

                #LIMPIAR CAMPOS
                self.elementos.box_id.delete(0,tk.END)
                self.elementos.box_nombre.delete(0, tk.END)


            except ValueError as error:
                # Verificar si el error es debido a un no dígito en id_auditor
                if "ID del auditor debe ser un número entero" in str(error):

                    messagebox.showerror("Error", "Debe ingresar solo números en el campo ID del auditor.")
                    # Borrar el contenido de la caja de texto id_auditor

                # Verificar si el error es debido a la conexión a la base de datos
                elif "Error al conectar a la base de datos" in str(error):
                    messagebox.showerror("Error de conexión", "No se pudo conectar a la base de datos.")
                else:
                    messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Error", "Ambas cajas de texto deben tener un valor.")
    def actualizar_tree_auditor(self):
        try:
            #borrar elementos actuales del tree auditor
            # devuelve una lista de identificadores de elementos secundarios
            # , y el operador * se utiliza para pasar esos identificadores
            # como argumentos separados a la función delete.
            self.elementos.tree.delete(*self.elementos.tree.get_children())

        #obtener los nuevos datos que deseamos mostrar
            auditores = self.auditor.mostrar_auditores()
        #insertar lo nuevos datos  en el tree
            # mostrar datos en la tabla
            for row in self.auditor.mostrar_auditores():
                self.elementos.tree.insert("", "end", values=row)
        except ValueError as error:
            print(f"fError al actualizar tabla : {error}")

    def selecionar_registro_auditor(self, event):
        try:
            itemSeleccionado = self.elementos.tree.focus()
            if itemSeleccionado:
                #obtener valores
                values = self.elementos.tree.item(itemSeleccionado)['values']
                #establecer los valores en los widgests entry
                self.elementos.box_id.delete(0, tk.END)
                self.elementos.box_id.insert(0, values[0])
                self.elementos.box_nombre.delete(0, tk.END)
                self.elementos.box_nombre.insert(0, values[1])

        except ValueError as error:
            print(f"fError al seleccionar registro : {error}")

    def modificar_auditor(self):
        id_auditor = self.elementos.box_id.get().strip()
        nombre_auditor = self.elementos.box_nombre.get().strip()
        # Verificar si ambas cajas de texto tienen un valor
        if id_auditor and nombre_auditor:
            try:
                self.auditor = Auditor()
                self.auditor.modificar_auditor(id_auditor, nombre_auditor)

                messagebox.showinfo("INFORMACIÓN", "los datos fueron Actualizados")
                # actualizamos los campos del tree
                self.actualizar_tree_auditor()

                # LIMPIAR CAMPOS
                self.elementos.box_id.delete(0, tk.END)
                self.elementos.box_nombre.delete(0, tk.END)

            except ValueError as error:
                print(f"fError al seleccionar registro : {error}")
        else:
            messagebox.showerror("Error", "Ambas cajas de texto deben tener un valor.")

    def eliminar_auditor(self):
        id_auditor = self.elementos.box_id.get().strip()
        nombre_auditor = self.elementos.box_nombre.get().strip()
        # Verificar si ambas cajas de texto tienen un valor
        if id_auditor and nombre_auditor:
            try:
                #id_auditor = self.elementos.box_id.get()
                #nombre_auditor = self.elementos.box_nombre.get()

                self.auditor = Auditor()
                self.auditor.eliminar_auditor(id_auditor)
                messagebox.showinfo("INFORMACIÓN", "los datos fueron Elimninados")
                # actualizamos los campos del tree
                self.actualizar_tree_auditor()

                # LIMPIAR CAMPOS
                self.elementos.box_id.delete(0, tk.END)
                self.elementos.box_nombre.delete(0, tk.END)
            except ValueError as error:
                print(f"fError al seleccionar registro : {error}")
        else:
            messagebox.showerror("Error", "Ambas cajas de texto deben tener un valor.")



#====== BOTON ATRAS =================
    def on_boton_atras(self):
        self.atras()

#==========CONSULTAR==================
    def on_boton_consultar(self):
        self.borrar_estado_anterior("menu principal")
        self.set_estado_actual("consulta")

#================FIN CONSULTAR=============================

#===================REGISTRAR GESTION===================
    def on_boton_registrar_modificar(self):
        self.borrar_estado_anterior("menu principal")
        self.set_estado_actual("gestion")

#================FIN REGISTRAR MODIFICAR =================

#================REGISTAR MODIFICAR AUDITOR ==============
    def on_boton_auditor(self):
        self.borrar_estado_anterior("gestion")
        self.set_estado_actual("gestion auditor")






#if __name__ == "__main__":
    #gui = Menu()
    #ui.ventana.mainloop()
    #gui.inicio.mainloop()