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

    def elementos_inicio(self):

        self.entry_user = None
        self.entry_password = None

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
        self.label_nombre = None

        # CAJAS DE TEXTO
        self.box_id = None
        self.box_nombre = None

        # BOTONES
        self.boton_guardar = None
        self.boton_modificar = None
        self.boton_eliminar = None

        # TABLA
        self.tree = None

    def variables_crud(self):
        self.id_variable = tk.StringVar()
        self.nombre_variable = tk.StringVar()