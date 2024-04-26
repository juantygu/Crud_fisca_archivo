import tkinter as tk
import json
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import ttk
from entidades.auditor import *
from GUI.elementos import Elementos
from GUI.menu_interfaz.Menu_principal.menu_principal import MenuPrincipal
from GUI.menu_interfaz.Menu_principal.modulo_gestion.gestion import Gestion
from GUI.menu_interfaz.Menu_principal.modulo_gestion.auditor_crud import AuditorCrud


class Interfaz():
    def __init__(self):
        try:

            self.ventana_inicio = tk.Tk()

            # instacia de clase
            self.elementos = Elementos()

            self.ventana_principal = None
            self.crear_ventana_inicio(self.ventana_inicio)

            self.estado_actual = None  # indica el estado actual de la interfaz
            self.window_width = None # ancho de pantalla pc
            self.window_height = None # altura de pantalla pc

            self.user = None
            self.password = None
            self.user_admin = None
            self.password_admin = None
            self.load_config_interfaz()

        except ValueError as error:
            print("Error al mostrar la interfaz,error:{}".format(error))

    def load_config_interfaz(self):
        """
        Carga las credenciales en archivo JSON.
        """
        try:
            with open('D:/pythonProject/Crud_fisca_archivo/config.json') as config_file:
                config = json.load(config_file)
                self.user = config["USUARIO"]
                self.password = config["PASSWORD"]
                self.user_admin = config["USUARIO_ADMIN"]
                self.password_admin = config["PASSWORD_ADMIN"]
        except FileNotFoundError:
            print("No se encontró el archivo de configuración.")
        except KeyError as e:
            print(f"Error: La clave {e} no está presente en el archivo de configuración.")

    def crear_ventana_inicio(self, ventana_inicio):
        self.estado_actual = "inicio"
        print(self.estado_actual)
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
        self.elementos.usuario_var.set(value=usuario_por_defecto)

        self.elementos.entry_user = tk.Entry(ventana_inicio, textvariable=self.elementos.usuario_var)
        self.elementos.entry_user.pack()

        label_password = tk.Label(ventana_inicio, text="Contraseña:")
        label_password.pack()
        self.elementos.contraseña_var.set(value=contrasena_por_defecto)

        self.elementos.entry_password = tk.Entry(ventana_inicio, show="*", textvariable=self.elementos.contraseña_var) # Muestra asteriscos para la contraseña
        self.elementos.entry_password.pack()

        # Crea un botón para iniciar sesión
        login_button = tk.Button(ventana_inicio, text="Iniciar Sesión", command= lambda: self.verificar_credenciales("inicio"))
        login_button.pack()

    def crear_ventana_principal(self):
        # ==========================================VENTANA===========================================================
        self.ventana_principal = tk.Tk()
        self.ventana_principal.title("ARCHIVO DE FISCALIZACIÓN")

        self.window_width = self.ventana_principal.winfo_screenwidth()  # ancho de la ventana requerido gracias a la funcion .winfo_reqwidth()
        self.window_height = self.ventana_principal.winfo_screenheight()  # alto de la ventana requerido gracias a la funcion .winfo_reqheight()
        print("ancho=", self.window_width, "alto=",self.window_height)

        self.ventana_principal.geometry(f"{self.window_width}x{self.window_height}+0+0")
        #self.ventana_principal.minsize(600, 400)
        self.ventana_principal.resizable(width=True, height=True)

        # Centrar la ventana en la pantalla
        #position_right = int(ancho - (window_width // 2))  # posicion de la ventana la funcion winfo_screenwidth() determina el ancho de la pantalla
        #position_down = int(largo - (window_height // 2))  # posicion de la ventana la funcion winfo_screenheight() determina el alto de la pantalla
        #self.ventana_principal.geometry("+{}+{}".format(position_right, position_down))  # los valores position_right, position_down van en los corchetes gracias a la funcion .format

        self.ventana_principal.configure(bg='#E6F7FF')


        # Crear instancia de MenuPrincipal y mostrar el menú principal
        menu_principal = MenuPrincipal(self.ventana_principal, self.elementos, self)
        menu_principal.mostrar_menu_principal()

        self.ventana_principal.mainloop()  # asigno el nuevo mainloo() que sera el hilo principal de la interfaz

    def verificar_credenciales(self,estado_actual):
        #print(estado_actual)

        # Obtiene el usuario y la contraseña ingresados por el usuario
        if estado_actual == "inicio":
            usuario = self.elementos.entry_user.get()
            contrasena = self.elementos.entry_password.get()
            # Verifica las credenciales
            if usuario == self.user and contrasena == self.password:
                # Si las credenciales son correctas, cierra la ventana de inicio de sesión y muestra la ventana principal
                self.ventana_inicio.destroy()
                self.crear_ventana_principal()
            else:
                # Si las credenciales son incorrectas, muestra un mensaje de error
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")

        if estado_actual == "gestion_auditor_crud":
            usuario_admin = self.elementos.entry_user_admin.get()
            contrasena_admin = self.elementos.entry_password_admin.get()

            if usuario_admin == self.user_admin and contrasena_admin == self.password_admin:
                # Si las credenciales son correctas,
                self.elementos.ventana_credenciales.destroy()
                auditor_crud = AuditorCrud(self.ventana_principal, self.elementos, self)
                auditor_crud.cambiar_id_auditor()
            else:
                # Si las credenciales son incorrectas, muestra un mensaje de error
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
                self.elementos.ventana_credenciales.focus_force()

    def atras(self): # CONDICIONES SI SE OPRIME EL BOTON REGRESAR

        # =======ESTADOS MENU PRINCIPAL===========
        if self.estado_actual == "consulta": # si esta en el estado consulta
            self.borrar_estado_anterior("consulta") # borra el estado consulta

            # Crear instancia de MenuPrincipal y mostrar el menú principal
            menu_principal = MenuPrincipal(self.ventana_principal, self.elementos, self)
            menu_principal.mostrar_menu_principal()

        if self.estado_actual == "gestion":
            self.borrar_estado_anterior("gestion")

            # Crear instancia de MenuPrincipal y mostrar el menú principal
            menu_principal = MenuPrincipal(self.ventana_principal, self.elementos, self)
            menu_principal.mostrar_menu_principal()

        if self.estado_actual == "inventario grafico":
            print("inventario grafico")

        # ======== ESTADOS MODULO GESTION ========

        # ======== AUDITOR CRUD ===============
        if self.estado_actual == "gestion_auditor_crud":
            self.borrar_estado_anterior("gestion_auditor_crud")

            # Crear intancia de gestion y mostrar gestion
            gestion = Gestion(self.ventana_principal, self.elementos, self)
            gestion.mostrar_gestion()
        # ======= AUDITOR CRUD ( cambiar_id_auditor ) ==========
        if self.estado_actual == "g_a_c_cambiar_id_auditor":
            self.borrar_estado_anterior("g_a_c_cambiar_id_auditor")

            # NO CAMBIAR DE ESTADO YA QUE ESTA INSTANCIADO LA CLASE AuditorCrud , presenta problemas al instanciarla
            # Crear intancia de auditor_crud y mostrar auditor crud
            #auditor_crud = AuditorCrud(self.ventana_principal, self.elementos, self)
            #auditor_crud.mostrar_auditor_crud()

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
            self.elementos.boton_expediente.destroy()
            self.elementos.boton_contribuyente.destroy()
            self.elementos.boton_auditor.destroy()
            self.elementos.boton_proceso.destroy()
            self.elementos.boton_prestamo.destroy()
            self.elementos.boton_atras.destroy()
        if estado_anterior == "gestion_auditor_crud":
            self.elementos.label_titulo.destroy()
            self.elementos.boton_atras.destroy()
            self.elementos.label_frame.destroy()
            self.elementos.label_id.destroy()
            self.elementos.label_nombre.destroy()
            self.elementos.box_id.destroy()
            self.elementos.box_nombre.destroy()
            self.elementos.boton_insertar.destroy()
            self.elementos.boton_modificar.destroy()
            self.elementos.boton_eliminar.destroy()
            self.elementos.tree.destroy()
            self.elementos.boton_cambiar_id.destroy()

        if estado_anterior == "g_a_c_cambiar_id_auditor": # gestion_auditor_crud
            self.elementos.label_titulo.destroy()
            self.elementos.label_antiguo_id.destroy()
            self.elementos.label_nuevo_id.destroy()
            self.elementos.box_antiguo_id.destroy()
            self.elementos.box_nuevo_id.destroy()
            self.elementos.boton_aceptar.destroy()
            self.elementos.boton_cancelar.destroy()


            # habilitar botones y cajas
            self.elementos.boton_insertar.config(state=tk.NORMAL)
            self.elementos.boton_eliminar.config(state=tk.NORMAL)
            self.elementos.boton_modificar.config(state=tk.NORMAL)
            self.elementos.boton_limpiar_caja_auditores.config(state=tk.NORMAL)
            self.elementos.boton_atras.config(state=tk.NORMAL)

            self.elementos.box_id.config(state=tk.NORMAL)
            self.elementos.box_cedula.config(state=tk.NORMAL)
            self.elementos.box_nombre.config(state=tk.NORMAL)

            self.estado_actual = "gestion_auditor_crud"
            self.elementos.ventana_credenciales_abierta = False
            print(self.estado_actual)




    # ============== FUNCIONES CRUD AUDITOR =====================

#====== BOTON ATRAS =================
    def on_boton_atras(self):
        self.atras()


    def calcular_posiciones_horizontal_botones(self, cantidad_botones, ancho_boton, ancho_pantalla):
        # Calcular el espacio total ocupado por los botones y los espacios entre ellos
        ancho_total_botones = cantidad_botones * ancho_boton
        espacio_entre_botones = (ancho_pantalla - ancho_total_botones) // (cantidad_botones + 1)

        # Calcular las posiciones x de los botones
        posiciones_x = []
        posicion_x_actual = espacio_entre_botones
        for _ in range(cantidad_botones):
            posiciones_x.append(posicion_x_actual)
            posicion_x_actual += ancho_boton + espacio_entre_botones

        return posiciones_x




#ejemplo = Interfaz()
#resultado= ejemplo.calcular_posiciones_horizontal_botones(3,300,1366)
#print(resultado)

#if __name__ == "__main__":
    #gui = Menu()
    #ui.ventana.mainloop()
    #gui.inicio.mainloop()