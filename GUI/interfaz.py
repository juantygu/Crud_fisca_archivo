import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import ttk
from entidades.auditor import *

class Menu():
    def __init__(self):
        try:
            self.usuario_por_defecto = "ARCHIVO"
            self.contrasena_por_defecto = "Fisca2024"
            self.inicio = tk.Tk()
            self.inicio.title("Inicio de Sesión")
            self.inicio.geometry("300x150")

            # Centrar la ventana en la pantalla
            self.inicio_width = self.inicio.winfo_screenwidth()  # ancho de la ventana requerido gracias a la funcion .winfo_reqwidth()
            self.inicio_height = self.inicio.winfo_screenheight()  # alto de la ventana requerido gracias a la funcion .winfo_reqheight()
            self.winicio = 300
            self.hinicio = 150
            self.inicio_position_right = int(self.inicio_width / 2 - self.winicio / 2)  # posicion de la ventana la funcion winfo_screenwidth() determina el ancho de la pantalla
            self.inicio_position_down = int(self.inicio_height / 2 - self.hinicio / 2)  # posicion de la ventana la funcion winfo_screenheight() determina el alto de la pantalla
            self.inicio.geometry("+{}+{}".format(self.inicio_position_right,self.inicio_position_down))  # los valores position_right, position_down van en los corchet

            self.crear_elementos() # crea los elemento iniciales

            # Agrega widgets para el usuario y la contraseña
            self.label_user = tk.Label(self.inicio, text="Usuario:")
            self.label_user.pack()
            self.usuario_var = tk.StringVar(value=self.usuario_por_defecto)
            self.entry_user = tk.Entry(self.inicio,textvariable= self.usuario_var )
            self.entry_user.pack()

            self.label_password = tk.Label(self.inicio, text="Contraseña:")
            self.label_password.pack()
            self.contraseña_var = tk.StringVar(value=self.contrasena_por_defecto)
            self.entry_password = tk.Entry(self.inicio, show="*",textvariable=self.contraseña_var)  # Muestra asteriscos para la contraseña
            self.entry_password.pack()

            # Crea un botón para iniciar sesión
            self.login_button = tk.Button(self.inicio, text="Iniciar Sesión", command=self.verificar_credenciales)
            self.login_button.pack()

            # instacia de clase
            self.auditor = Auditor()


        except ValueError as error:
            print("Error al mostrar la interfaz,error:{}".format(error))

    def verificar_credenciales(self):
        # Obtiene el usuario y la contraseña ingresados por el usuario
        self.usuario = self.entry_user.get()
        self.contrasena = self.entry_password.get()

        # Verifica las credenciales (puedes personalizar esto)
        if self.usuario == "ARCHIVO" and self.contrasena == "Fisca2024":
            # Si las credenciales son correctas, cierra la ventana de inicio de sesión y muestra la ventana principal
            self.inicio.destroy()
            self.mostrar_ventana_principal()
        else:
            # Si las credenciales son incorrectas, muestra un mensaje de error
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def crear_elementos(self):
        #======CRUD COMUN =========
        self.label_frame = tk.LabelFrame()
        #TABLA
        self.tree = ttk.Treeview()


        self.label_id = tk.Label()
        self.label_nombre = tk.Label()

        self.box_id = tk.Entry()
        self.id_variable = tk.StringVar()
        self.box_nombre = tk.Entry()
        self.nombre_variable = tk.StringVar()

        self.boton_guardar = tk.Button()
        self.boton_modificar =tk.Button()
        self.boton_eliminar =tk.Button()
        #==== MENU PRINCIPAL====
        self.label_titulo = tk.Label()
        self.boton_consultar = tk.Button()
        self.imagen_consultar = PhotoImage()
        self.boton_registrar_modificar = tk.Button()
        self.imagen_registrar_modificar =PhotoImage()
        self.boton_inventario = tk.Button()
        self.imagen_inventario = PhotoImage()
        self.boton_atras = tk.Button()

        self.estado_actual = None # indica el estado actual de la interfaz
        #===== CONSULTAR ======

        self.boton_nombre = tk.Button()
        self.boton_documento = tk.Button()

        #==== GESTION ===
        self.boton_auditor = tk.Button()
        self.imagen_auditor = PhotoImage()

        # =======GESTION DE AUDITORES=========
        self.boton_reemplazar_auditor = tk.Button()

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
            self.label_titulo.destroy()
            self.boton_consultar.destroy()
            self.boton_registrar_modificar.destroy()
            self.boton_inventario.destroy()
        if estado_anterior =="consulta":
            self.label_titulo.destroy()
            self.boton_atras.destroy()
        if estado_anterior =="gestion":
            self.label_titulo.destroy()
            self.boton_auditor.destroy()
            self.boton_atras.destroy()
        if estado_anterior =="gestion auditor":
            self.label_titulo.destroy()
            self.boton_atras.destroy()
            self.label_frame.destroy()
            self.label_id.destroy()
            self.label_nombre.destroy()
            self.box_id.destroy()
            self.box_nombre.destroy()
            self.boton_guardar.destroy()
            self.boton_modificar.destroy()
            self.boton_eliminar.destroy()
            self.tree.destroy()
            self.boton_reemplazar_auditor.destroy()







    def mostrar_ventana_principal(self):
        # ==========================================VENTANA===========================================================
        self.ventana = tk.Tk()
        self.ventana.title("ARCHIVO DE FISCALIZACIÓN")
        self.ventana.geometry('1080x600')
        self.ventana.minsize(600, 400)
        self.ventana.resizable(width=False, height=False)

        # Centrar la ventana en la pantalla
        self.window_width = self.ventana.winfo_screenwidth()  # ancho de la ventana requerido gracias a la funcion .winfo_reqwidth()
        self.window_height = self.ventana.winfo_screenheight()  # alto de la ventana requerido gracias a la funcion .winfo_reqheight()
        self.wventana = 1080
        self.hventana = 600
        self.position_right = int(self.window_width / 2 - self.wventana / 2)  # posicion de la ventana la funcion winfo_screenwidth() determina el ancho de la pantalla
        self.position_down = int(self.window_height / 2 - self.hventana / 2)  # posicion de la ventana la funcion winfo_screenheight() determina el alto de la pantalla
        self.ventana.geometry("+{}+{}".format(self.position_right,self.position_down))  # los valores position_right, position_down van en los corchetes gracias a la funcion .format
        self.ventana.configure(bg='#E6F7FF')
        self.set_estado_actual("menu principal")
        self.ventana.mainloop()  # asigno el nuevo mainloo() que sera el hilo principal de la interfaz


    def set_estado_actual(self,estado):# esta funcion le indica a la interfaz en que estado debe estar segun la logica del proceso
        if estado == "menu principal": #INDICA EL ESTADO MENU INICIAL
            self.estado_actual = "menu principal"
            # Etiqueta centrada en la parte superior
            self.label_titulo = tk.Label(self.ventana, text="ARCHIVO DE FISCALIZACIÓN", font=("Arial", 30, "bold"),fg="black", bg="#E6F7FF")
            self.label_titulo.pack(pady=20)  # pady añade un espacio en la parte inferior de la etiqueta

            # Botones centrados horizontalmente
            #======BOTON CONSULTAR========
            self.boton_consultar = tk.Button(self.ventana, text="Consultar", font=("Arial", 20, "bold"), fg="black",bg="white", bd=4, relief=tk.GROOVE, width=300, height=150,command=self.on_boton_consultar)
            self.boton_consultar.place(x=50, y=210)
            self.imagen_consultar = PhotoImage(file="D:\pythonProject\Crud_fisca_archivo\imagenes\consultar.png")
            self.imagen_consultar = self.imagen_consultar.subsample(10)  # Ajusta el factor de reducción según sea necesario
            self.boton_consultar.config(image=self.imagen_consultar, compound="bottom")

            #======BOTON REGISTRAR MODIFICAR====
            self.boton_registrar_modificar = tk.Button(self.ventana, text="Gestión", font=("Arial", 20, "bold"), fg="black",bg="white", bd=4, relief=tk.GROOVE, width=300, height=150,command=self.on_boton_registrar_modificar)
            self.boton_registrar_modificar.place(x=390, y=210)
            self.imagen_registrar_modificar = PhotoImage(file="D:\pythonProject\Crud_fisca_archivo\imagenes\egistro.png")
            self.imagen_registrar_modificar = self.imagen_registrar_modificar.subsample(6)  # Ajusta el factor de reducción según sea necesario
            self.boton_registrar_modificar.config(image=self.imagen_registrar_modificar,compound="bottom")

            # ======BOTON INVENTARIO====
            self.boton_inventario = tk.Button(self.ventana, text="Inventario Gráfico", font=("Arial", 20, "bold"),fg="black", bg="white", bd=4, relief=tk.GROOVE, width=300, height=150)
            self.boton_inventario.place(x=730, y=210)
            self.imagen_inventario = PhotoImage(file="D:\pythonProject\Crud_fisca_archivo\imagenes\inventario.png")
            self.imagen_inventario = self.imagen_inventario.subsample(6)  # Ajusta el factor de reducción según sea necesario
            self.boton_inventario.config(image=self.imagen_inventario, compound="bottom")

        if estado == "consulta":
            self.estado_actual = "consulta"
            # Etiqueta centrada en la parte superior
            self.label_titulo = tk.Label(self.ventana, text="Seleccione el tipo de busqueda", font=("Arial", 30, "bold"),fg="black", bg="#E6F7FF")
            self.label_titulo.pack(pady=20)  # pady añade un espacio en la parte inferior de la etiqueta

            self.boton_atras = tk.Button(self.ventana, text="ATRAS", font=("Arial", 12, "bold"),fg="black", bg="white", bd=4, relief=tk.GROOVE, width=15, height=2,command=self.atras)
            self.boton_atras.place(x=900, y=500)

        if estado == "gestion": # menu registrar modificar
            self.estado_actual = "gestion"
            # Boton atras
            self.boton_atras = tk.Button(self.ventana, text="ATRAS", font=("Arial", 12, "bold"), fg="black", bg="white",bd=4, relief=tk.GROOVE, width=15, height=2, command=self.atras)
            self.boton_atras.place(x=900, y=500)

            # Etiqueta centrada en la parte superior
            self.label_titulo = tk.Label(self.ventana, text="QUE DESEA REGISTRAR O MODIFICAR", font=("Arial", 30, "bold"),fg="black", bg="#E6F7FF")
            self.label_titulo.pack(pady=20)  # pady añade un espacio en la parte inferior de la etiqueta
            # boton auditor
            self.boton_auditor = tk.Button(self.ventana, text="Auditor", font=("Arial", 20, "bold"), fg="black",bg="white", bd=4, relief=tk.GROOVE, width=300, height=150,command=self.on_boton_auditor)
            self.boton_auditor.place(x=50, y=210)
            self.imagen_auditor = PhotoImage(file="D:\pythonProject\Crud_fisca_archivo\imagenes\Auditor.png")
            self.imagen_auditor = self.imagen_auditor.subsample(5)  # Ajusta el factor de reducción según sea necesario
            self.boton_auditor.config(image=self.imagen_auditor, compound="bottom")

        if estado == "gestion auditor":
            self.estado_actual = "gestion auditor"
            #titulo
            self.label_titulo = tk.Label(self.ventana, text="GESTIÓN DE AUDITORES", font=("Arial", 30, "bold"),fg="black", bg="#E6F7FF")
            self.label_titulo.pack(pady=20)  # pady añade un espacio en la parte inferior de la etiqueta
            # LABEL IFRAME
            self.label_frame = tk.LabelFrame(self.ventana, text="DATOS DEL AUDITOR", font=("Arial", 20, "bold"),fg="black", bg="#E6F7FF", bd=5, relief=tk.RIDGE)
            self.label_frame.place(x=50, y=100, width=500, height=300)
            #etiqueta id
            self.label_id = tk.Label(self.label_frame, text="ID", font=("Arial", 15, "bold"),fg="black", bg="#E6F7FF")
            self.label_id.place(x=50, y=50)
            # caja id
            self.box_id = tk.Entry(self.label_frame,textvariable=self.id_variable,bd=3, font=("Arial", 12), width=15, insertbackground="blue", selectbackground="blue",relief=tk.RIDGE)
            self.box_id.place(x=140,y=50)
            self.box_id.delete(0, tk.END)  # Borra el contenido actual de la caja de texto self.box_id
            #etiqueta nombre
            self.label_nombre = tk.Label(self.label_frame, text="Nombre", font=("Arial", 15, "bold"),fg="black", bg="#E6F7FF")
            self.label_nombre.place(x=50, y=90)
            #caja nombre
            self.box_nombre = tk.Entry(self.label_frame,textvariable=self.nombre_variable,bd=3, font=("Arial", 12), width=35, insertbackground="blue", selectbackground="blue",relief=tk.RIDGE)
            self.box_nombre.place(x=140,y=90)
            self.box_nombre.delete(0, tk.END)  # Borra el contenido actual de la caja de texto self.box_nombre
            #boton guardar
            self.boton_guardar = tk.Button(self.label_frame, text="Guardar", font=("Arial", 12, "bold"), fg="black",bg="white", bd=4, relief=tk.GROOVE, width=7, height=1,activebackground='blue',command=self.insertar_auditor)
            self.boton_guardar.place(x=50, y=170)
            #boton modificar
            self.boton_modificar = tk.Button(self.label_frame, text="Modificar", font=("Arial", 12, "bold"), fg="black",bg="white", bd=4, relief=tk.GROOVE, width=7, height=1,activebackground='blue',command=self.modificar_auditor)
            self.boton_modificar.place(x=150, y=170)
            #boton eliminar
            self.boton_eliminar = tk.Button(self.label_frame, text="Eliminar", font=("Arial", 12, "bold"), fg="black",bg="white", bd=4, relief=tk.GROOVE, width=7, height=1,activebackground='blue',command=self.eliminar_auditor)
            self.boton_eliminar.place(x=250, y=170)
            # TABLA
            # Crear Treeview
            self.tree = ttk.Treeview(self.ventana, columns=('ID_AUDITOR', 'NOMBRE'), show='headings',height=15)
            self.tree.heading('ID_AUDITOR', text='ID_AUDITOR')
            self.tree.column('ID_AUDITOR', anchor='center')
            self.tree.heading('NOMBRE', text='NOMBRE')
            self.tree.column('NOMBRE', anchor='center')

            self.tree.place(x=600,y=120)
            style = ttk.Style()
            style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
            style.configure("Treeview", rowheight=25, font=('Arial', 10), highlightthickness=2, bd=2)
            # mostrar datos en la tabla
            for row in self.auditor.mostrar_auditores():
                self.tree.insert("","end",values=row)
            # ejecutar la funcion de hacer click y y mostrar el resultado en als cajas
            self.tree.bind("<<TreeviewSelect>>", self.selecionar_registro_auditor)

            # boton reemplazar auditor
            self.boton_reemplazar_auditor = tk.Button(self.ventana, text="Reemplazar Auditor", font=("Arial", 12, "bold"), fg="black", bg="blue",bd=4, relief=tk.GROOVE, width=15, height=2)
            self.boton_reemplazar_auditor.place(x=200, y=450)
            # Boton atras
            self.boton_atras = tk.Button(self.ventana, text="ATRAS", font=("Arial", 12, "bold"), fg="black", bg="white",bd=4, relief=tk.GROOVE, width=15, height=2, command=self.atras)
            self.boton_atras.place(x=900, y=530)



    #============== FUNCIONES CRUD AUDITOR =====================
    def insertar_auditor(self):
        id_auditor = self.box_id.get().strip()
        nombre_auditor = self.box_nombre.get().strip()
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
                self.box_id.delete(0,tk.END)
                self.box_nombre.delete(0, tk.END)

            except DuplicadoError as duplicado_error:
                messagebox.showerror("Error", str(duplicado_error))

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
            self.tree.delete(*self.tree.get_children())

        #obtener los nuevos datos que deseamos mostrar
            auditores = self.auditor.mostrar_auditores()
        #insertar lo nuevos datos  en el tree
            # mostrar datos en la tabla
            for row in self.auditor.mostrar_auditores():
                self.tree.insert("", "end", values=row)
        except ValueError as error:
            print(f"fError al actualizar tabla : {error}")

    def selecionar_registro_auditor(self, event):
        try:
            itemSeleccionado = self.tree.focus()
            if itemSeleccionado:
                #obtener valores
                values = self.tree.item(itemSeleccionado)['values']
                #establecer los valores en los widgests entry
                self.box_id.delete(0, tk.END)
                self.box_id.insert(0, values[0])
                self.box_nombre.delete(0, tk.END)
                self.box_nombre.insert(0, values[1])

        except ValueError as error:
            print(f"fError al seleccionar registro : {error}")

    def modificar_auditor(self):
        id_auditor = self.box_id.get().strip()
        nombre_auditor = self.box_nombre.get().strip()
        # Verificar si ambas cajas de texto tienen un valor
        if id_auditor and nombre_auditor:
            try:
                self.auditor = Auditor()
                self.auditor.modificar_auditor(id_auditor, nombre_auditor)

                messagebox.showinfo("INFORMACIÓN", "los datos fueron Actualizados")
                # actualizamos los campos del tree
                self.actualizar_tree_auditor()

                # LIMPIAR CAMPOS
                self.box_id.delete(0, tk.END)
                self.box_nombre.delete(0, tk.END)

            except ValueError as error:
                print(f"fError al seleccionar registro : {error}")
        else:
            messagebox.showerror("Error", "Ambas cajas de texto deben tener un valor.")

    def eliminar_auditor(self):
        id_auditor = self.box_id.get().strip()
        nombre_auditor = self.box_nombre.get().strip()
        # Verificar si ambas cajas de texto tienen un valor
        if id_auditor and nombre_auditor:
            try:
                #id_auditor = self.box_id.get()
                #nombre_auditor = self.box_nombre.get()

                self.auditor = Auditor()
                self.auditor.eliminar_auditor(id_auditor)
                messagebox.showinfo("INFORMACIÓN", "los datos fueron Elimninados")
                # actualizamos los campos del tree
                self.actualizar_tree_auditor()

                # LIMPIAR CAMPOS
                self.box_id.delete(0, tk.END)
                self.box_nombre.delete(0, tk.END)
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

#===================REGISTRAR MODIFICAR===================
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