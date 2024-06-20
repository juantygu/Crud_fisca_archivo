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
        self.elementos_menu_consultas()

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

    def elementos_menu_consultas(self):
        self.boton_consulta_prestamo = None
        self.imagen_consulta_prestamo = None
        self.boton_consulta_general = None
        self.imagen_consulta_general = None

    def elementos_consultar(self):
        self.boton_nombre = None
        self.boton_documento = None
        self.boton_buscar =  None
        self.boton_copiar = None
        self.boton_copiar1 = None
        self.boton_copiar2 = None
        self.boton_copiar3 = None
        self.label_busqueda_id_contribuyente = None
        self.box_busqueda_id_contribuyente = None
        self.label_busqueda_id_expediente = None
        self.text_busqueda_id_expediente = None

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

        # ======= AUDITOR CRUD ==========
        self.label_id_auditor = None
        self.label_cedula = None

        self.box_id_auditor = None
        self.box_cedula = None

        # ======== CONTRUBUYENTE CRUD ========
        self.label_id_contribuyente = None
        self.label_tipo = None

        self.box_id_contribuyente = None
        self.box_tipo = None

        # ======== PROCESO CRUD ==========
        self.label_id_proceso = None
        self.box_id_proceso = None

        #======== EXPEDIENTE CRUD ========
        self.label_id_expediente = None
        self.label_id_caja = None
        self.label_estado = None
        self.label_año_gravable = None

        self.box_id_expediente = None
        self.box_id_caja = None
        self.box_estado = None
        self.box_año_gravable = None
        self.box_año_gravable_1 = None
        self.box_año_gravable_2 = None
        self.box_año_gravable_3 = None
        self.box_año_gravable_4 = None

        # ====== PRESTAMO CRUD =========
        self.label_id_prestamo = None
        self.label_fecha_entrega = None
        self.label_fecha_entrega_1 = None
        self.label_fecha_devolucion = None
        self.label_fecha_devolucion1 = None
        self.label_responsable = None
        self.label_area = None
        self.label_ids_encontrados = None
        self.label_ids_no_encontrados = None
        self.label_exp_prestados = None
        self.label_exp_disponibles = None

        self.box_id_prestamo = None
        self.box_fecha_entrega = None
        self.box_fecha_entrega1 = None
        self.box_fecha_devolucion = None
        self.box_fecha_devolucion1 = None
        self.box_responsable = None
        self.box_area = None
        self.text_busqueda_id_expediente_1 = None
        self.text_ids_encontrados = None
        self.text_ids_no_encontrados = None
        self.text_exp_prestados = None
        self.text_exp_disponibles = None

        # ======= CRUD COMUN ============
        self.label_frame = None
        self.label_frame1 = None
        self.label_frame2 = None
        self.label_frame3 = None
        self.label_nombre = None
        self.label_antiguo_id = None
        self.label_nuevo_id = None
        self.label_id = None
        self.label_info = None
        self.label_info_auditores = None
        self.label_info_procesos = None

        self.box_nombre = None
        self.box_antiguo_id = None
        self.box_nuevo_id = None
        self.box_id = None

        self.barra_desplazamiento_v = None
        self.barra_desplazamiento_v1 = None
        self.barra_desplazamiento_v2 = None
        self.barra_desplazamiento_v3 = None
        self.barra_desplazamiento_v5 = None

        # =========BOTONES ============
        self.boton_insertar = None
        self.boton_insertar1 = None
        self.boton_modificar = None
        self.boton_eliminar = None
        self.boton_limpiar_cajas = None
        self.boton_cambiar_id = None
        self.boton_aceptar = None
        self.boton_cancelar = None

        # TABLA
        self.tree = None

    def variables_crud(self):
        self.id_variable = tk.StringVar()
        self.id_variable_auditor = tk.StringVar()
        self.id_variable_contribuyente = tk.StringVar()
        self.id_variable_proceso = tk.StringVar()
        self.id_variable_expediente = tk.StringVar()
        self.id_variable_prestamo = tk.StringVar()
        self.id_variable_caja = tk.StringVar()
        self.estado_variable = tk.StringVar()
        self.año_gravable_variable = tk.StringVar()
        self.año_gravable_1_variable = tk.StringVar()
        self.año_gravable_2_variable = tk.StringVar()
        self.año_gravable_3_variable = tk.StringVar()
        self.año_gravable_4_variable = tk.StringVar()
        self.cedula_variable = tk.StringVar()
        self.nombre_variable = tk.StringVar()
        self.tipo_variable = tk.StringVar()

        self.antiguo_id_variable = tk.StringVar()
        self.nuevo_id_variable = tk.StringVar()

        self.responsable_variable = tk.StringVar()

        self.busqueda_id_contribuyente_variable = tk.StringVar()
        self.area_variable =tk.StringVar()



    def ventanas_emergentes(self):
        self.ventana_credenciales = None
        self.ventana_credenciales_abierta = False