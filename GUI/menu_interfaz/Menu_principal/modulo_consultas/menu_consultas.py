import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import ttk
from GUI.menu_interfaz.Menu_principal.modulo_consultas.consultas_prestamo_crud import ConsultasPrestamosActivos
from GUI.menu_interfaz.Menu_principal.modulo_consultas.consultas_general_crud import ConsultasGeneral

class MenuConsultas:

    def __init__(self,ventana_principal, elementos, interfaz):
        """
                Inicializa la clase Gestion.

                Parameters:
                - ventana_principal (tk.Tk): La ventana principal de la aplicación.
                - elementos (Elementos): Instancia de la clase Elementos.
                - interfaz (Interfaz): Instancia de la clase Interfaz.

                Returns:
                - None
                """
        self.ventana_principal = ventana_principal
        self.elementos = elementos
        self.interfaz = interfaz

    def mostrar_menu_consultas(self):

        self.interfaz.estado_actual = "Menu_consultas"
        print(self.interfaz.estado_actual)

        altura_pantalla = self.interfaz.window_height
        ancho_pantalla = self.interfaz.window_width
        posicion_x1 = self.interfaz.calcular_posiciones_horizontal_botones(2, 300, ancho_pantalla)
        posicion_y_fila1 = (altura_pantalla / 4)

        try:
            # ======BOTON ATRAS========
            self.elementos.boton_atras = tk.Button(self.ventana_principal, text="ATRAS", font=("Arial", 12, "bold"),
                                                   fg="black", bg="white", bd=4, relief=tk.GROOVE, width=15, height=2,
                                                   command=self.interfaz.atras)
            self.elementos.boton_atras.place(x=(ancho_pantalla - 250), y=(altura_pantalla - 150))

            # Etiqueta centrada en la parte superior
            self.elementos.label_titulo = tk.Label(self.ventana_principal, text="MENÚ CONSULTAS",
                                                   font=("Arial", 30, "bold"), fg="black", bg="#E6F7FF")
            self.elementos.label_titulo.pack(side="top",
                                             pady=20)  # pady añade un espacio en la parte inferior de la etiqueta

            # ======BOTON CONSULTAS_PRESTAMO========
            self.elementos.boton_consulta_prestamo = tk.Button(self.ventana_principal, text="PRESTAMOS ACTIVOS",
                                                        font=("Arial", 20, "bold"),
                                                        fg="black", bg="white", bd=4, relief=tk.GROOVE, width=300,
                                                        height=150,
                                                        command=self.on_boton_consultas_prestamo_crud)
            self.elementos.boton_consulta_prestamo.place(x=posicion_x1[0], y=posicion_y_fila1)
            self.elementos.imagen_consulta_prestamo = PhotoImage(
                file="D:\pythonProject\Crud_fisca_archivo\imagenes\consultas_1.png")
            self.elementos.imagen_consulta_prestamo = self.elementos.imagen_consulta_prestamo.subsample(
                5)  # Ajusta el factor de reducción según sea necesario
            self.elementos.boton_consulta_prestamo.config(image=self.elementos.imagen_consulta_prestamo, compound="bottom")

            # ======BOTON CONSULTA GENERAL========
            self.elementos.boton_consulta_general = tk.Button(self.ventana_principal, text="GENERAL",
                                                           font=("Arial", 20, "bold"),
                                                           fg="black", bg="white", bd=4, relief=tk.GROOVE, width=300,
                                                           height=150,command=self.on_boton_consultas_general_crud
                                                           )
            self.elementos.boton_consulta_general.place(x=posicion_x1[1], y=posicion_y_fila1)
            self.elementos.imagen_consulta_general = PhotoImage(
                file="D:\pythonProject\Crud_fisca_archivo\imagenes\consultas_2.png")
            self.elementos.imagen_consulta_general = self.elementos.imagen_consulta_general.subsample(
                5)  # Ajusta el factor de reducción según sea necesario
            self.elementos.boton_consulta_general.config(image=self.elementos.imagen_consulta_general, compound="bottom")
        except Exception as e:
            # Si ocurre algún error, imprime un mensaje de error
            print("Error al mostrar menú principal:", str(e))

    def on_boton_consultas_prestamo_crud(self):
        """
                Maneja el evento de clic en el botón "consultas_prestamo_crud".

                Parameters:
                - None

                Returns:
                - None
                """
        self.interfaz.borrar_estado_anterior("Menu_consultas")
        consultas_prestamos_crud = ConsultasPrestamosActivos(self.ventana_principal, self.elementos, self.interfaz)
        consultas_prestamos_crud.mostrar_consultas_prestamos_activos()

    def on_boton_consultas_general_crud(self):
        """
                        Maneja el evento de clic en el botón "consultas_general_crud".

                        Parameters:
                        - None

                        Returns:
                        - None
                        """
        self.interfaz.borrar_estado_anterior("Menu_consultas")
        consultas_general_crud = ConsultasGeneral(self.ventana_principal, self.elementos, self.interfaz)
        consultas_general_crud.mostrar_consultas_general()
