import tkinter as tk
from tkinter import ttk

class Elementos:

    def __init__(self):

        self.elementos_inicio()
        self.elementos_menu_principal()
        self.elementos_consultar()
        self.elementos_gestion()
        self.elementos_crud()
        self.variables_crud()
        self.variables_inicio()
        self.ventanas_emergentes()

    def elementos_inicio(self):

        self.entry_user = None
        self.entry_password = None
        self.entry_user_admin = None
        self.entry_password_admin = None

    def variables_inicio(self):
        self.usuario_var = tk.StringVar()
        self.contraseña_var = tk.StringVar()
        self.usuario_admin_var = tk.StringVar()
        self.contraseña_admin_var = tk.StringVar()

    def elementos_menu_principal(self):

        self.label_titulo = None
        self.boton_consultar = None
        self.imagen_consultar = None
        self.boton_gestion = None
        self.imagen_gestion = None
        self.boton_inventario = None
        self.imagen_inventario = None
        self.boton_atras = None

    def elementos_consultar(self):
        self.boton_nombre = None
        self.boton_documento = None

    def elementos_gestion(self):
        self.boton_expediente = None
        self.imagen_expediente = None

        self.boton_contribuyente = None
        self.imagen_contribuyente = None

        self.boton_auditor = None
        self.imagen_auditor = None

        self.boton_proceso = None
        self.imagen_proceso = None

        self.boton_prestamo = None
        self.imagen_prestamo = None

    def elementos_crud(self):
        # ETIQUETAS

        self.label_frame = None
        self.label_id = None
        self.label_cedula = None
        self.label_nombre = None
        self.label_tipo = None


        self.label_antiguo_id = None
        self.label_nuevo_id = None

        # CAJAS DE TEXTO
        self.box_id = None
        self.box_cedula = None
        self.box_nombre = None
        self.box_tipo = None

        self.box_antiguo_id = None
        self.box_nuevo_id = None

        # BOTONES
        self.boton_insertar = None
        self.boton_modificar = None
        self.boton_eliminar = None
        self.boton_limpiar_caja_auditores = None
        self.boton_cambiar_id = None
        self.boton_aceptar = None
        self.boton_cancelar = None


        # TABLA
        self.tree = None

    def variables_crud(self):
        self.id_variable = tk.StringVar()
        self.cedula_variable = tk.StringVar()
        self.nombre_variable = tk.StringVar()
        self.tipo_variable = tk.StringVar()

        self.antiguo_id_variable = tk.StringVar()
        self.nuevo_id_variable = tk.StringVar()

    def ventanas_emergentes(self):
        self.ventana_credenciales = None
        self.ventana_credenciales_abierta = False