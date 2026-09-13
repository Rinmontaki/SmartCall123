import customtkinter as ctk

from services.gestor_llamadas import GestorLlamadas


class SmartCallApp(ctk.CTk):
    """
    Ventana principal de SmartCall 123.

    Actúa como capa de presentación y delega toda
    la lógica del sistema a GestorLlamadas.
    """

    ANCHO_VENTANA = 1280
    ALTO_VENTANA = 760

    COLOR_FONDO = "#0B1120"
    COLOR_PANEL = "#111827"
    COLOR_PANEL_SECUNDARIO = "#172033"
    COLOR_BORDE = "#263247"

    COLOR_TEXTO = "#F8FAFC"
    COLOR_TEXTO_SECUNDARIO = "#94A3B8"

    COLOR_P1 = "#EF4444"
    COLOR_P2 = "#F59E0B"
    COLOR_P3 = "#22C55E"

    COLOR_ACCION = "#2563EB"
    COLOR_ACCION_HOVER = "#1D4ED8"

    def __init__(self) -> None:
        super().__init__()

        self.gestor = GestorLlamadas()

        self._configurar_ventana()
        self._configurar_grid()

        self._crear_sidebar()
        self._crear_contenido_principal()

        self.actualizar_dashboard()
    
    def _formatear_cola(self, cola) -> str:
        """
        Convierte los elementos de una cola en una
        representación legible para el dashboard.
        """
    
        elementos = cola.obtener_elementos()
    
        if not elementos:
            return "Sin llamadas"
    
        identificadores = []
    
        for llamada in elementos:
            identificadores.append(
                llamada.id_llamada
            )
    
        return "  →  ".join(
            identificadores
        )

    # ---------------------------------------------------------
    # CONFIGURACIÓN GENERAL
    # ---------------------------------------------------------

    def _configurar_ventana(self) -> None:
        """
        Configura las propiedades generales de la ventana.
        """

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title(
            "SmartCall 123 | Centro de Gestión de Emergencias"
        )

        self.geometry(
            f"{self.ANCHO_VENTANA}x{self.ALTO_VENTANA}"
        )

        self.minsize(
            1100,
            680
        )

        self.configure(
            fg_color=self.COLOR_FONDO
        )

        self._centrar_ventana()

    def _centrar_ventana(self) -> None:
        """
        Centra la ventana principal en la pantalla.
        """

        self.update_idletasks()

        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        posicion_x = (
            ancho_pantalla - self.ANCHO_VENTANA
        ) // 2

        posicion_y = (
            alto_pantalla - self.ALTO_VENTANA
        ) // 2

        self.geometry(
            f"{self.ANCHO_VENTANA}x{self.ALTO_VENTANA}"
            f"+{posicion_x}+{posicion_y}"
        )

    def _configurar_grid(self) -> None:
        """
        Divide la aplicación entre sidebar
        y contenido principal.
        """

        self.grid_columnconfigure(
            0,
            weight=0
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

    # ---------------------------------------------------------
    # SIDEBAR
    # ---------------------------------------------------------

    def _crear_sidebar(self) -> None:
        """
        Construye el menú lateral de navegación.
        """

        self.sidebar = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0,
            fg_color=self.COLOR_PANEL
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        self._crear_marca_sidebar()

        self._crear_boton_menu(
            "Inicio",
            "⌂",
            self.mostrar_inicio
        )

        self._crear_boton_menu(
            "Registrar llamada",
            "+",
            self.registrar_llamada
        )

        self._crear_boton_menu(
            "Atender siguiente",
            "☎",
            self.atender_siguiente
        )

        self._crear_boton_menu(
            "Finalizar atención",
            "✓",
            self.finalizar_atencion
        )

        self._crear_boton_menu(
            "Buscar llamada",
            "⌕",
            self.buscar_llamada
        )

        self._crear_boton_menu(
            "Reclasificar",
            "↕",
            self.reclasificar_llamada
        )

        self._crear_boton_menu(
            "Cancelar llamada",
            "×",
            self.cancelar_llamada
        )

        self._crear_boton_menu(
            "Deshacer",
            "↶",
            self.deshacer_operacion
        )

        self._crear_estado_sidebar()

    def _crear_marca_sidebar(self) -> None:
        """
        Construye el encabezado de marca SmartCall.
        """

        contenedor = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        contenedor.pack(
            fill="x",
            padx=22,
            pady=(28, 35)
        )

        titulo = ctk.CTkLabel(
            contenedor,
            text="SMARTCALL",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            ),
            text_color=self.COLOR_TEXTO
        )

        titulo.pack(
            anchor="w"
        )

        numero = ctk.CTkLabel(
            contenedor,
            text="123",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color=self.COLOR_P1
        )

        numero.pack(
            anchor="w"
        )

        subtitulo = ctk.CTkLabel(
            contenedor,
            text="Emergency Control",
            font=ctk.CTkFont(
                size=11
            ),
            text_color=self.COLOR_TEXTO_SECUNDARIO
        )

        subtitulo.pack(
            anchor="w",
            pady=(3, 0)
        )

    def _crear_boton_menu(
        self,
        texto: str,
        icono: str,
        comando
    ) -> None:
        """
        Crea un botón reutilizable del menú lateral.
        """

        boton = ctk.CTkButton(
            self.sidebar,
            text=f"  {icono}    {texto}",
            command=comando,
            height=42,
            corner_radius=8,
            anchor="w",
            fg_color="transparent",
            hover_color=self.COLOR_PANEL_SECUNDARIO,
            text_color=self.COLOR_TEXTO,
            font=ctk.CTkFont(
                size=13,
                weight="normal"
            )
        )

        boton.pack(
            fill="x",
            padx=14,
            pady=3
        )

    def _crear_estado_sidebar(self) -> None:
        """
        Muestra el estado operativo del sistema.
        """

        estado = ctk.CTkFrame(
            self.sidebar,
            fg_color=self.COLOR_PANEL_SECUNDARIO,
            corner_radius=10
        )

        estado.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=20
        )

        indicador = ctk.CTkLabel(
            estado,
            text="●  SISTEMA OPERATIVO",
            text_color=self.COLOR_P3,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )

        indicador.pack(
            anchor="w",
            padx=15,
            pady=(12, 2)
        )

        descripcion = ctk.CTkLabel(
            estado,
            text="Gestor de llamadas activo",
            text_color=self.COLOR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                size=10
            )
        )

        descripcion.pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

    # ---------------------------------------------------------
    # CONTENIDO PRINCIPAL
    # ---------------------------------------------------------

    def _crear_contenido_principal(self) -> None:
        """
        Construye el dashboard principal.
        """

        self.contenido = ctk.CTkFrame(
            self,
            fg_color=self.COLOR_FONDO,
            corner_radius=0
        )

        self.contenido.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.contenido.grid_columnconfigure(
            0,
            weight=1
        )

        self.contenido.grid_rowconfigure(
            3,
            weight=1
        )

        self._crear_header()
        self._crear_tarjetas_prioridad()
        self._crear_panel_atencion()
        self._crear_panel_colas()

    # ---------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------

    def _crear_header(self) -> None:
        header = ctk.CTkFrame(
            self.contenido,
            fg_color="transparent"
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=32,
            pady=(28, 16)
        )

        titulo = ctk.CTkLabel(
            header,
            text="Centro de control",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            ),
            text_color=self.COLOR_TEXTO
        )

        titulo.pack(
            anchor="w"
        )

        subtitulo = ctk.CTkLabel(
            header,
            text=(
                "Gestión y priorización dinámica "
                "de llamadas de emergencia"
            ),
            font=ctk.CTkFont(
                size=13
            ),
            text_color=self.COLOR_TEXTO_SECUNDARIO
        )

        subtitulo.pack(
            anchor="w",
            pady=(4, 0)
        )

    # ---------------------------------------------------------
    # TARJETAS DE PRIORIDAD
    # ---------------------------------------------------------

    def _crear_tarjetas_prioridad(self) -> None:
        contenedor = ctk.CTkFrame(
            self.contenido,
            fg_color="transparent"
        )

        contenedor.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=32,
            pady=(0, 18)
        )

        for columna in range(3):
            contenedor.grid_columnconfigure(
                columna,
                weight=1
            )

        self.valor_p1 = self._crear_tarjeta(
            contenedor,
            0,
            "P1",
            "CRÍTICA",
            self.COLOR_P1
        )

        self.valor_p2 = self._crear_tarjeta(
            contenedor,
            1,
            "P2",
            "ALTA",
            self.COLOR_P2
        )

        self.valor_p3 = self._crear_tarjeta(
            contenedor,
            2,
            "P3",
            "NORMAL",
            self.COLOR_P3
        )

    def _crear_tarjeta(
        self,
        padre,
        columna: int,
        prioridad: str,
        descripcion: str,
        color: str
    ) -> ctk.CTkLabel:
        tarjeta = ctk.CTkFrame(
            padre,
            height=125,
            corner_radius=12,
            fg_color=self.COLOR_PANEL,
            border_width=1,
            border_color=self.COLOR_BORDE
        )

        tarjeta.grid(
            row=0,
            column=columna,
            sticky="ew",
            padx=(
                0 if columna == 0 else 7,
                0 if columna == 2 else 7
            )
        )

        etiqueta = ctk.CTkLabel(
            tarjeta,
            text=f"{prioridad}  ·  {descripcion}",
            text_color=color,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        etiqueta.pack(
            anchor="w",
            padx=20,
            pady=(17, 0)
        )

        valor = ctk.CTkLabel(
            tarjeta,
            text="0",
            text_color=self.COLOR_TEXTO,
            font=ctk.CTkFont(
                size=34,
                weight="bold"
            )
        )

        valor.pack(
            anchor="w",
            padx=20,
            pady=(5, 2)
        )

        texto = ctk.CTkLabel(
            tarjeta,
            text="llamadas en espera",
            text_color=self.COLOR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                size=11
            )
        )

        texto.pack(
            anchor="w",
            padx=20
        )

        return valor

    # ---------------------------------------------------------
    # LLAMADA ACTUAL
    # ---------------------------------------------------------

    def _crear_panel_atencion(self) -> None:
        panel = ctk.CTkFrame(
            self.contenido,
            fg_color=self.COLOR_PANEL,
            corner_radius=12,
            border_width=1,
            border_color=self.COLOR_BORDE
        )

        panel.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=32,
            pady=(0, 18)
        )

        titulo = ctk.CTkLabel(
            panel,
            text="LLAMADA EN ATENCIÓN",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=self.COLOR_TEXTO_SECUNDARIO
        )

        titulo.pack(
            anchor="w",
            padx=20,
            pady=(17, 5)
        )

        self.label_atencion = ctk.CTkLabel(
            panel,
            text="No existe ninguna llamada en atención",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            text_color=self.COLOR_TEXTO
        )

        self.label_atencion.pack(
            anchor="w",
            padx=20,
            pady=(3, 18)
        )

    # ---------------------------------------------------------
    # COLAS
    # ---------------------------------------------------------

    def _crear_panel_colas(self) -> None:
        panel = ctk.CTkFrame(
            self.contenido,
            fg_color=self.COLOR_PANEL,
            corner_radius=12,
            border_width=1,
            border_color=self.COLOR_BORDE
        )

        panel.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=32,
            pady=(0, 28)
        )

        titulo = ctk.CTkLabel(
            panel,
            text="COLAS DE ESPERA",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=self.COLOR_TEXTO_SECUNDARIO
        )

        titulo.pack(
            anchor="w",
            padx=20,
            pady=(18, 15)
        )

        self.label_cola_p1 = self._crear_fila_cola(
            panel,
            "P1 · CRÍTICA",
            self.COLOR_P1
        )

        self.label_cola_p2 = self._crear_fila_cola(
            panel,
            "P2 · ALTA",
            self.COLOR_P2
        )

        self.label_cola_p3 = self._crear_fila_cola(
            panel,
            "P3 · NORMAL",
            self.COLOR_P3
        )

    def _crear_fila_cola(
        self,
        padre,
        titulo: str,
        color: str
    ) -> ctk.CTkLabel:
        fila = ctk.CTkFrame(
            padre,
            fg_color=self.COLOR_PANEL_SECUNDARIO,
            corner_radius=8
        )

        fila.pack(
            fill="x",
            padx=20,
            pady=5
        )

        etiqueta = ctk.CTkLabel(
            fila,
            text=titulo,
            text_color=color,
            width=120,
            anchor="w",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        )

        etiqueta.pack(
            side="left",
            padx=(15, 10),
            pady=12
        )

        contenido = ctk.CTkLabel(
            fila,
            text="Sin llamadas",
            text_color=self.COLOR_TEXTO_SECUNDARIO,
            anchor="w"
        )

        contenido.pack(
            side="left",
            padx=10
        )

        return contenido

    # ---------------------------------------------------------
    # ACTUALIZACIÓN
    # ---------------------------------------------------------

    def actualizar_dashboard(self) -> None:
        """
        Actualiza la información visual utilizando
        el estado actual del GestorLlamadas.
        """

        self.valor_p1.configure(
            text=str(
                self.gestor.cola_p1.tamano()
            )
        )

        self.valor_p2.configure(
            text=str(
                self.gestor.cola_p2.tamano()
            )
        )

        self.valor_p3.configure(
            text=str(
                self.gestor.cola_p3.tamano()
            )
        )

        llamada = (
            self.gestor.llamada_en_atencion
        )

        if llamada is None:
            self.label_atencion.configure(
                text=(
                    "No existe ninguna llamada "
                    "en atención"
                )
            )

        else:
            prioridad = (
                llamada.prioridad.value
                if llamada.prioridad is not None
                else "-"
            )

            self.label_atencion.configure(
                text=(
                    f"{llamada.id_llamada} · "
                    f"{prioridad} · "
                    f"{llamada.tipo} · "
                    f"{llamada.ubicacion}"
                )
            )

    # ---------------------------------------------------------
    # ACCIONES
    # ---------------------------------------------------------

    def mostrar_inicio(self) -> None:
        self.actualizar_dashboard()

    def registrar_llamada(self) -> None:
        print("Registrar llamada")

    def atender_siguiente(self) -> None:
        try:
            self.gestor.atender_siguiente_llamada()
            self.actualizar_dashboard()

        except RuntimeError as error:
            print(error)

    def finalizar_atencion(self) -> None:
        try:
            self.gestor.finalizar_llamada_actual()
            self.actualizar_dashboard()

        except RuntimeError as error:
            print(error)

    def buscar_llamada(self) -> None:
        print("Buscar llamada")

    def reclasificar_llamada(self) -> None:
        print("Reclasificar llamada")

    def cancelar_llamada(self) -> None:
        print("Cancelar llamada")

    def deshacer_operacion(self) -> None:
        try:
            self.gestor.deshacer_ultima_operacion()
            self.actualizar_dashboard()

        except RuntimeError as error:
            print(error)
    