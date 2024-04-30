import tkinter as tk
from tkinter import PhotoImage
from GUI.menu_interfaz.Menu_principal.consultar import Consultar
from GUI.menu_interfaz.Menu_principal.modulo_gestion.gestion import Gestion


class MenuPrincipal():
    def __init__(self, ventana_principal, elementos, interfaz):
        """
                Inicializa la clase MenuPrincipal.

                Parameters:
                - ventana_principal (tk.Tk): La ventana principal de la aplicación.
                - elementos (Elementos): Instancia de la clase Elementos.
                - interfaz (Interfaz): Instancia de la clase Interfaz.

                Returns:
                - None
                """
        self.ventana_principal = ventana_principal
        self.elementos = elementos
        self.interfaz = interfaz # instancia de la clase menu

    def mostrar_menu_principal(self):
        """
                Muestra el menú principal de la aplicación.

                Parameters:
                - None

                Returns:
                - None
                """
        altura_pantalla = self.interfaz.window_height
        ancho_pantalla = self.interfaz.window_width
        posicion_x = self.interfaz.calcular_posiciones_horizontal_botones(3, 300, ancho_pantalla)
        posicion_y = (altura_pantalla/3)
        #print(posicion_x,posicion_y)

        # Etiqueta centrada en la parte superior
        self.elementos.label_titulo = tk.Label(self.ventana_principal, text="ARCHIVO DE FISCALIZACIÓN",
                                               font=("Arial", 30, "bold"), fg="black", bg="#E6F7FF")
        self.elementos.label_titulo.pack(side="top", pady=20)  # pady añade un espacio en la parte inferior de la etiqueta

        # Botones centrados horizontalmente
        # ======BOTON CONSULTAR========
        self.elementos.boton_consultar = tk.Button(self.ventana_principal, text="Consultar", font=("Arial", 20, "bold"),
                                                   fg="black", bg="white", bd=4, relief=tk.GROOVE, width=300,
                                                   height=150, command=self.on_boton_consultar)
        self.elementos.boton_consultar.place(x=posicion_x[0], y=posicion_y)
        self.elementos.imagen_consultar = PhotoImage(file="D:\pythonProject\Crud_fisca_archivo\imagenes\consultar.png")
        self.elementos.imagen_consultar = self.elementos.imagen_consultar.subsample(10)  # Ajusta el factor de reducción según sea necesario
        self.elementos.boton_consultar.config(image=self.elementos.imagen_consultar, compound="bottom")

        # ======BOTON GESTION====
        self.elementos.boton_gestion = tk.Button(self.ventana_principal, text="Gestión", font=("Arial", 20, "bold"),
                                                 fg="black", bg="white", bd=4, relief=tk.GROOVE, width=300, height=150,
                                                 command=self.on_boton_gestion)
        self.elementos.boton_gestion.place(x=posicion_x[1], y=posicion_y)
        self.elementos.imagen_gestion = PhotoImage(file="D:\pythonProject\Crud_fisca_archivo\imagenes\egistro.png")
        self.elementos.imagen_gestion = self.elementos.imagen_gestion.subsample(6)  # Ajusta el factor de reducción según sea necesario
        self.elementos.boton_gestion.config(image=self.elementos.imagen_gestion, compound="bottom")

        # ======BOTON INVENTARIO====
        self.elementos.boton_inventario = tk.Button(self.ventana_principal, text="Inventario Gráfico",
                                                    font=("Arial", 20, "bold"), fg="black", bg="white", bd=4,
                                                    relief=tk.GROOVE, width=300, height=150)
        self.elementos.boton_inventario.place(x=posicion_x[2], y=posicion_y)
        self.elementos.imagen_inventario = PhotoImage(file="D:\pythonProject\Crud_fisca_archivo\imagenes\inventario.png")
        self.elementos.imagen_inventario = self.elementos.imagen_inventario.subsample(6)  # Ajusta el factor de reducción según sea necesario
        self.elementos.boton_inventario.config(image=self.elementos.imagen_inventario, compound="bottom")
        self.interfaz.estado_actual = "menu principal"
        print(self.interfaz.estado_actual)

    def on_boton_consultar(self):
        """
                Maneja el evento de clic en el botón "Consultar".

                Parameters:
                - None

                Returns:
                - None
                """
        self.interfaz.borrar_estado_anterior("menu principal")
        consultar = Consultar(self.ventana_principal, self.elementos, self.interfaz)
        consultar.mostrar_consultar()

    def on_boton_gestion(self):
        """
                Maneja el evento de clic en el botón "Gestión".

                Parameters:
                - None

                Returns:
                - None
                """
        self.interfaz.borrar_estado_anterior("menu principal")
        gestion = Gestion(self.ventana_principal, self.elementos, self.interfaz)
        gestion.mostrar_gestion()