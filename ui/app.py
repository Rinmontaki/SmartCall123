import customtkinter as ctk

from services.gestor_llamadas import GestorLlamadas
from models.llamada import Llamada, Prioridad

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
    
    COLOR_EXITO = "#22C55E"
    COLOR_ADVERTENCIA = "#F59E0B"
    COLOR_ERROR = "#EF4444"
    COLOR_INFO = "#3B82F6"

    def __init__(self) -> None:
        super().__init__()

        self.gestor = GestorLlamadas()

        self._notificacion_actual: ctk.CTkFrame | None = None
        self._temporizador_notificacion: str | None = None

        self._configurar_ventana()
        self._configurar_grid()

        self._crear_sidebar()
        self._crear_contenido_principal()

        self.actualizar_dashboard()
    
    def _formatear_cola(self, cola) -> str:
        """
        Genera una representación visual de las llamadas
        almacenadas en una cola de espera.
        """

        llamadas = cola.obtener_elementos()

        if not llamadas:
            return "Sin llamadas"

        identificadores = [
            llamada.id_llamada
            for llamada in llamadas
        ]

        return "  →  ".join(identificadores)
    
    def _centrar_ventana_secundaria(
        self,
        ventana: ctk.CTkToplevel,
        ancho: int,
        alto: int
    ) -> None:
        """
        Centra una ventana secundaria respecto
        a la ventana principal.
        """

        self.update_idletasks()

        posicion_x = (
            self.winfo_x()
            + (self.winfo_width() - ancho) // 2
        )

        posicion_y = (
            self.winfo_y()
            + (self.winfo_height() - alto) // 2
        )

        ventana.geometry(
            f"{ancho}x{alto}"
            f"+{posicion_x}+{posicion_y}"
        )
    
    def _crear_formulario_registro(
        self,
        ventana: ctk.CTkToplevel
    ) -> None:
        """
        Construye el formulario visual utilizado
        para registrar una llamada.
        """

        contenedor = ctk.CTkScrollableFrame(
            ventana,
            fg_color=self.COLOR_FONDO,
            corner_radius=0
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # -----------------------------------------------------
        # ENCABEZADO
        # -----------------------------------------------------

        titulo = ctk.CTkLabel(
            contenedor,
            text="Registrar nueva llamada",
            text_color=self.COLOR_TEXTO,
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        titulo.pack(
            anchor="w"
        )

        subtitulo = ctk.CTkLabel(
            contenedor,
            text=(
                "Ingrese la información reportada "
                "durante la comunicación con el 123."
            ),
            text_color=self.COLOR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                size=12
            )
        )

        subtitulo.pack(
            anchor="w",
            pady=(3, 22)
        )

        # -----------------------------------------------------
        # TIPO DE EMERGENCIA
        # -----------------------------------------------------

        self._crear_etiqueta_formulario(
            contenedor,
            "Tipo de emergencia"
        )

        tipo_var = ctk.StringVar(
            value="Accidente de tránsito"
        )

        combo_tipo = ctk.CTkComboBox(
            contenedor,
            variable=tipo_var,
            values=[
                "Accidente de tránsito",
                "Emergencia médica",
                "Incendio",
                "Violencia",
                "Robo",
                "Desastre natural",
                "Persona desaparecida",
                "Reporte general",
                "Otro",
            ],
            height=40,
            corner_radius=8,
            state="readonly",
            fg_color=self.COLOR_PANEL,
            border_color=self.COLOR_BORDE,
            button_color=self.COLOR_ACCION,
            button_hover_color=self.COLOR_ACCION_HOVER,
            text_color=self.COLOR_TEXTO
        )

        combo_tipo.pack(
            fill="x",
            pady=(0, 16)
        )

        # -----------------------------------------------------
        # UBICACIÓN
        # -----------------------------------------------------

        self._crear_etiqueta_formulario(
            contenedor,
            "Ubicación"
        )

        entrada_ubicacion = ctk.CTkEntry(
            contenedor,
            placeholder_text=(
                "Dirección, barrio o punto de referencia"
            ),
            height=40,
            corner_radius=8,
            fg_color=self.COLOR_PANEL,
            border_color=self.COLOR_BORDE,
            text_color=self.COLOR_TEXTO
        )

        entrada_ubicacion.pack(
            fill="x",
            pady=(0, 16)
        )

        # -----------------------------------------------------
        # DESCRIPCIÓN
        # -----------------------------------------------------

        self._crear_etiqueta_formulario(
            contenedor,
            "Descripción de la emergencia"
        )

        entrada_descripcion = ctk.CTkTextbox(
            contenedor,
            height=100,
            corner_radius=8,
            fg_color=self.COLOR_PANEL,
            border_width=1,
            border_color=self.COLOR_BORDE,
            text_color=self.COLOR_TEXTO
        )

        entrada_descripcion.pack(
            fill="x",
            pady=(0, 16)
        )

        # -----------------------------------------------------
        # PERSONAS AFECTADAS
        # -----------------------------------------------------

        self._crear_etiqueta_formulario(
            contenedor,
            "Personas afectadas"
        )

        entrada_personas = ctk.CTkEntry(
            contenedor,
            height=40,
            corner_radius=8,
            fg_color=self.COLOR_PANEL,
            border_color=self.COLOR_BORDE,
            text_color=self.COLOR_TEXTO
        )

        entrada_personas.insert(
            0,
            "1"
        )

        entrada_personas.pack(
            fill="x",
            pady=(0, 20)
        )

        # -----------------------------------------------------
        # ESTADO DE LA EMERGENCIA
        # -----------------------------------------------------

        self._crear_etiqueta_formulario(
            contenedor,
            "Evaluación inicial"
        )

        panel_estado = ctk.CTkFrame(
            contenedor,
            fg_color=self.COLOR_PANEL,
            corner_radius=10,
            border_width=1,
            border_color=self.COLOR_BORDE
        )

        panel_estado.pack(
            fill="x",
            pady=(0, 20)
        )

        consciente_var = ctk.BooleanVar(
            value=True
        )

        respira_var = ctk.BooleanVar(
            value=True
        )

        heridos_var = ctk.BooleanVar(
            value=False
        )

        peligro_var = ctk.BooleanVar(
            value=False
        )

        riesgo_var = ctk.BooleanVar(
            value=False
        )

        self._crear_switch_estado(
            panel_estado,
            "La persona está consciente",
            consciente_var
        )

        self._crear_switch_estado(
            panel_estado,
            "La persona respira",
            respira_var
        )

        self._crear_switch_estado(
            panel_estado,
            "Existen personas heridas",
            heridos_var
        )

        self._crear_switch_estado(
            panel_estado,
            "Existe peligro inmediato",
            peligro_var
        )

        self._crear_switch_estado(
            panel_estado,
            "Existe riesgo potencial",
            riesgo_var
        )

        # -----------------------------------------------------
        # MENSAJE DEL FORMULARIO
        # -----------------------------------------------------

        mensaje = ctk.CTkLabel(
            contenedor,
            text="",
            text_color=self.COLOR_P1,
            font=ctk.CTkFont(
                size=11
            )
        )

        mensaje.pack(
            anchor="w",
            pady=(0, 10)
        )

        # -----------------------------------------------------
        # BOTONES
        # -----------------------------------------------------

        botones = ctk.CTkFrame(
            contenedor,
            fg_color="transparent"
        )

        botones.pack(
            fill="x",
            pady=(5, 10)
        )

        boton_cancelar = ctk.CTkButton(
            botones,
            text="Cancelar",
            command=ventana.destroy,
            height=42,
            corner_radius=8,
            fg_color=self.COLOR_PANEL_SECUNDARIO,
            hover_color=self.COLOR_BORDE,
            text_color=self.COLOR_TEXTO
        )

        boton_cancelar.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(0, 5)
        )

        boton_registrar = ctk.CTkButton(
            botones,
            text="Registrar llamada",
            height=42,
            corner_radius=8,
            fg_color=self.COLOR_ACCION,
            hover_color=self.COLOR_ACCION_HOVER,
            text_color=self.COLOR_TEXTO,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=lambda: self._procesar_registro_llamada(
                ventana=ventana,
                tipo=tipo_var.get(),
                ubicacion=entrada_ubicacion.get(),
                descripcion=entrada_descripcion.get(
                    "1.0",
                    "end"
                ),
                personas=entrada_personas.get(),
                consciente=consciente_var.get(),
                respira=respira_var.get(),
                heridos=heridos_var.get(),
                peligro_inmediato=peligro_var.get(),
                riesgo_potencial=riesgo_var.get(),
                mensaje=mensaje
            )
        )

        boton_registrar.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(5, 0)
        )

    def _crear_etiqueta_formulario(
        self,
        padre,
        texto: str
    ) -> None:
        """
        Crea las etiquetas utilizadas sobre
        los campos de los formularios.
        """

        etiqueta = ctk.CTkLabel(
            padre,
            text=texto,
            text_color=self.COLOR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )

        etiqueta.pack(
            anchor="w",
            pady=(0, 6)
        )
    
    def _crear_switch_estado(
        self,
        padre,
        texto: str,
        variable: ctk.BooleanVar
    ) -> None:
        """
        Crea un interruptor utilizado para registrar
        condiciones de la emergencia.
        """

        switch = ctk.CTkSwitch(
            padre,
            text=texto,
            variable=variable,
            onvalue=True,
            offvalue=False,
            progress_color=self.COLOR_ACCION,
            button_color=self.COLOR_TEXTO,
            button_hover_color=self.COLOR_TEXTO_SECUNDARIO,
            text_color=self.COLOR_TEXTO,
            font=ctk.CTkFont(
                size=12
            )
        )

        switch.pack(
            anchor="w",
            padx=18,
            pady=8
        )
    
    def _crear_item_accion_llamada(
        self,
        padre,
        llamada: Llamada,
        comando
    ) -> None:
        """
        Crea una tarjeta seleccionable para una llamada
        utilizada en operaciones como cancelar
        y reclasificar.
        """

        prioridad = (
            llamada.prioridad.value
            if llamada.prioridad is not None
            else "-"
        )

        color = self._obtener_color_prioridad(
            llamada.prioridad
        )

        boton = ctk.CTkButton(
            padre,
            text=(
                f"{llamada.id_llamada}    {prioridad}\n"
                f"{llamada.tipo}"
            ),
            command=comando,
            height=66,
            anchor="w",
            corner_radius=8,
            fg_color=self.COLOR_PANEL_SECUNDARIO,
            hover_color=self.COLOR_BORDE,
            border_width=1,
            border_color=color,
            text_color=self.COLOR_TEXTO,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        )

        boton.pack(
            fill="x",
            padx=3,
            pady=4
        )
        
    def _mostrar_notificacion(
        self,
        titulo: str,
        mensaje: str,
        tipo: str = "info",
        duracion: int = 3500
    ) -> None:
        """
        Muestra una notificación temporal dentro del dashboard.

        Args:
            titulo: Encabezado principal de la notificación.
            mensaje: Información detallada.
            tipo: Puede ser 'exito', 'advertencia',
                'error' o 'info'.
            duracion: Tiempo visible en milisegundos.
        """

        # Cerrar una notificación anterior.
        self._cerrar_notificacion()

        configuraciones = {
            "exito": {
                "color": self.COLOR_EXITO,
                "icono": "✓",
            },
            "advertencia": {
                "color": self.COLOR_ADVERTENCIA,
                "icono": "!",
            },
            "error": {
                "color": self.COLOR_ERROR,
                "icono": "×",
            },
            "info": {
                "color": self.COLOR_INFO,
                "icono": "i",
            },
        }

        configuracion = configuraciones.get(
            tipo,
            configuraciones["info"]
        )

        color = configuracion["color"]
        icono = configuracion["icono"]

        notificacion = ctk.CTkFrame(
            self.contenido,
            width=350,
            height=95,
            corner_radius=12,
            fg_color=self.COLOR_PANEL_SECUNDARIO,
            border_width=1,
            border_color=color
        )

        notificacion.place(
            relx=0.975,
            rely=0.035,
            anchor="ne"
        )

        notificacion.pack_propagate(False)

        # -----------------------------------------------------
        # CONTENEDOR INTERNO
        # -----------------------------------------------------

        contenido = ctk.CTkFrame(
            notificacion,
            fg_color="transparent"
        )

        contenido.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=12
        )

        # -----------------------------------------------------
        # ICONO
        # -----------------------------------------------------

        indicador = ctk.CTkLabel(
            contenido,
            text=icono,
            width=30,
            height=30,
            corner_radius=15,
            fg_color=color,
            text_color="#FFFFFF",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        indicador.pack(
            side="left",
            anchor="n",
            padx=(0, 12)
        )

        # -----------------------------------------------------
        # TEXTO
        # -----------------------------------------------------

        bloque_texto = ctk.CTkFrame(
            contenido,
            fg_color="transparent"
        )

        bloque_texto.pack(
            side="left",
            fill="both",
            expand=True
        )

        label_titulo = ctk.CTkLabel(
            bloque_texto,
            text=titulo,
            anchor="w",
            text_color=self.COLOR_TEXTO,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        label_titulo.pack(
            anchor="w"
        )

        label_mensaje = ctk.CTkLabel(
            bloque_texto,
            text=mensaje,
            anchor="w",
            justify="left",
            wraplength=250,
            text_color=self.COLOR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                size=11
            )
        )

        label_mensaje.pack(
            anchor="w",
            pady=(3, 0)
        )

        self._notificacion_actual = notificacion

        self._temporizador_notificacion = self.after(
            duracion,
            self._cerrar_notificacion
        )
        
    def _cerrar_notificacion(self) -> None:
        """
        Elimina la notificación actualmente visible.
        """

        if self._temporizador_notificacion is not None:
            self.after_cancel(
                self._temporizador_notificacion
            )

            self._temporizador_notificacion = None

        if self._notificacion_actual is not None:
            self._notificacion_actual.destroy()
            self._notificacion_actual = None
    
    def _crear_vista_busqueda(
        self,
        ventana: ctk.CTkToplevel,
        llamadas: list
    ) -> None:
        """
        Construye la ventana de consulta de llamadas.
        """

        contenedor = ctk.CTkFrame(
            ventana,
            fg_color=self.COLOR_FONDO,
            corner_radius=0
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=22
        )

        contenedor.grid_columnconfigure(
            0,
            weight=1
        )

        contenedor.grid_columnconfigure(
            1,
            weight=2
        )

        contenedor.grid_rowconfigure(
            1,
            weight=1
        )

        # -------------------------------------------------
        # ENCABEZADO
        # -------------------------------------------------

        encabezado = ctk.CTkFrame(
            contenedor,
            fg_color="transparent"
        )

        encabezado.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(0, 20)
        )

        titulo = ctk.CTkLabel(
            encabezado,
            text="Consultar llamadas",
            text_color=self.COLOR_TEXTO,
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        titulo.pack(
            anchor="w"
        )

        subtitulo = ctk.CTkLabel(
            encabezado,
            text=(
                "Seleccione una llamada para consultar "
                "su información completa."
            ),
            text_color=self.COLOR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                size=12
            )
        )

        subtitulo.pack(
            anchor="w",
            pady=(3, 0)
        )

        # -------------------------------------------------
        # LISTADO
        # -------------------------------------------------

        panel_lista = ctk.CTkFrame(
            contenedor,
            fg_color=self.COLOR_PANEL,
            corner_radius=12,
            border_width=1,
            border_color=self.COLOR_BORDE
        )

        panel_lista.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        titulo_lista = ctk.CTkLabel(
            panel_lista,
            text="LLAMADAS",
            text_color=self.COLOR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )

        titulo_lista.pack(
            anchor="w",
            padx=16,
            pady=(15, 10)
        )

        lista_scroll = ctk.CTkScrollableFrame(
            panel_lista,
            fg_color="transparent"
        )

        lista_scroll.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=(0, 8)
        )

        # -------------------------------------------------
        # PANEL DE DETALLE
        # -------------------------------------------------

        panel_detalle = ctk.CTkFrame(
            contenedor,
            fg_color=self.COLOR_PANEL,
            corner_radius=12,
            border_width=1,
            border_color=self.COLOR_BORDE
        )

        panel_detalle.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(8, 0)
        )

        self._detalle_llamada_frame = panel_detalle

        self._mostrar_detalle_vacio(
            panel_detalle
        )

        # -------------------------------------------------
        # CREAR ELEMENTOS
        # -------------------------------------------------

        for llamada in llamadas:
            self._crear_item_llamada(
                lista_scroll,
                llamada,
                panel_detalle
            )
    
    def _crear_item_llamada(
        self,
        padre,
        llamada,
        panel_detalle
    ) -> None:
        """
        Crea un elemento seleccionable dentro
        del listado de llamadas.
        """

        prioridad = (
            llamada.prioridad.value
            if llamada.prioridad is not None
            else "-"
        )

        color_prioridad = (
            self._obtener_color_prioridad(
                llamada.prioridad
            )
        )

        boton = ctk.CTkButton(
            padre,
            fg_color=self.COLOR_PANEL_SECUNDARIO,
            hover_color=self.COLOR_BORDE,
            corner_radius=9,
            height=65,
            anchor="w",
            text=(
                f"{llamada.id_llamada}    {prioridad}\n"
                f"{llamada.estado.value}"
            ),
            text_color=self.COLOR_TEXTO,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            border_width=1,
            border_color=color_prioridad,
            command=lambda id_llamada=llamada.id_llamada: (
                self._mostrar_detalle_llamada(
                    panel_detalle,
                    id_llamada
                )
            )
        )

        boton.pack(
            fill="x",
            pady=4,
            padx=3
        )
    
    def _obtener_color_prioridad(
        self,
        prioridad
    ) -> str:
        """
        Retorna el color visual asociado
        a una prioridad.
        """

        if prioridad is None:
            return self.COLOR_BORDE

        if prioridad.value == "P1":
            return self.COLOR_P1

        if prioridad.value == "P2":
            return self.COLOR_P2

        if prioridad.value == "P3":
            return self.COLOR_P3

        return self.COLOR_BORDE

    def _mostrar_detalle_vacio(
        self,
        panel
    ) -> None:
        """
        Muestra el estado inicial del panel
        de detalle.
        """

        for widget in panel.winfo_children():
            widget.destroy()

        contenedor = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )

        contenedor.pack(
            expand=True
        )

        icono = ctk.CTkLabel(
            contenedor,
            text="⌕",
            text_color=self.COLOR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                size=38
            )
        )

        icono.pack()

        texto = ctk.CTkLabel(
            contenedor,
            text="Seleccione una llamada",
            text_color=self.COLOR_TEXTO,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        texto.pack(
            pady=(8, 3)
        )

        descripcion = ctk.CTkLabel(
            contenedor,
            text=(
                "La información completa aparecerá aquí."
            ),
            text_color=self.COLOR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                size=11
            )
        )

        descripcion.pack()
    
    def _mostrar_detalle_llamada(
        self,
        panel,
        id_llamada: str
    ) -> None:
        """
        Muestra toda la información correspondiente
        a una llamada seleccionada.
        """

        llamada = (
            self.gestor
            .obtener_llamada_registrada(
                id_llamada
            )
        )

        if llamada is None:
            self._mostrar_notificacion(
                titulo="Llamada no encontrada",
                mensaje=(
                    "La llamada seleccionada "
                    "ya no está disponible."
                ),
                tipo="error"
            )
            return

        for widget in panel.winfo_children():
            widget.destroy()

        prioridad = (
            llamada.prioridad.value
            if llamada.prioridad is not None
            else "-"
        )

        color_prioridad = (
            self._obtener_color_prioridad(
                llamada.prioridad
            )
        )

        # -------------------------------------------------
        # ENCABEZADO
        # -------------------------------------------------

        encabezado = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )

        encabezado.pack(
            fill="x",
            padx=22,
            pady=(22, 15)
        )

        identificador = ctk.CTkLabel(
            encabezado,
            text=llamada.id_llamada,
            text_color=self.COLOR_TEXTO,
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        )

        identificador.pack(
            side="left"
        )

        prioridad_label = ctk.CTkLabel(
            encabezado,
            text=f"  {prioridad}  ",
            fg_color=color_prioridad,
            text_color="#FFFFFF",
            corner_radius=6,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )

        prioridad_label.pack(
            side="left",
            padx=12
        )

        # -------------------------------------------------
        # ESTADO
        # -------------------------------------------------

        self._crear_dato_detalle(
            panel,
            "Estado",
            llamada.estado.value
        )

        self._crear_dato_detalle(
            panel,
            "Tipo de emergencia",
            llamada.tipo
        )

        self._crear_dato_detalle(
            panel,
            "Ubicación",
            llamada.ubicacion
        )

        self._crear_dato_detalle(
            panel,
            "Personas afectadas",
            str(llamada.personas_afectadas)
        )

        self._crear_dato_detalle(
            panel,
            "Hora de llegada",
            llamada.hora_llegada.strftime(
                "%H:%M:%S"
            )
        )

        # -------------------------------------------------
        # DESCRIPCIÓN
        # -------------------------------------------------

        separador = ctk.CTkFrame(
            panel,
            height=1,
            fg_color=self.COLOR_BORDE
        )

        separador.pack(
            fill="x",
            padx=22,
            pady=12
        )

        titulo_descripcion = ctk.CTkLabel(
            panel,
            text="DESCRIPCIÓN",
            text_color=self.COLOR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            )
        )

        titulo_descripcion.pack(
            anchor="w",
            padx=22
        )

        descripcion = ctk.CTkLabel(
            panel,
            text=llamada.descripcion,
            justify="left",
            wraplength=440,
            text_color=self.COLOR_TEXTO,
            font=ctk.CTkFont(
                size=12
            )
        )

        descripcion.pack(
            anchor="w",
            padx=22,
            pady=(5, 14)
        )

        # -------------------------------------------------
        # EVALUACIÓN INICIAL
        # -------------------------------------------------

        self._crear_dato_detalle(
            panel,
            "Consciente",
            self._texto_booleano(
                llamada.consciente
            )
        )

        self._crear_dato_detalle(
            panel,
            "Respira",
            self._texto_booleano(
                llamada.respira
            )
        )

        self._crear_dato_detalle(
            panel,
            "Heridos",
            self._texto_booleano(
                llamada.heridos
            )
        )

        self._crear_dato_detalle(
            panel,
            "Peligro inmediato",
            self._texto_booleano(
                llamada.peligro_inmediato
            )
        )

        self._crear_dato_detalle(
            panel,
            "Riesgo potencial",
            self._texto_booleano(
                llamada.riesgo_potencial
            )
        )
    
    
    def _mostrar_detalle_accion_vacio(
        self,
        panel,
        texto: str
    ) -> None:
        """
        Muestra un mensaje mientras no se haya
        seleccionado ninguna llamada.
        """

        for widget in panel.winfo_children():
            widget.destroy()

        label = ctk.CTkLabel(
            panel,
            text=texto,
            text_color=self.COLOR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                size=13
            )
        )

        label.pack(
            expand=True
        )
    
    def _crear_vista_cancelacion(
        self,
        ventana: ctk.CTkToplevel,
        llamadas: list[Llamada]
    ) -> None:
        """
        Construye la interfaz utilizada para seleccionar
        y cancelar una llamada.
        """

        contenedor = ctk.CTkFrame(
            ventana,
            fg_color=self.COLOR_FONDO,
            corner_radius=0
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=22
        )

        contenedor.grid_columnconfigure(
            0,
            weight=1
        )

        contenedor.grid_columnconfigure(
            1,
            weight=2
        )

        contenedor.grid_rowconfigure(
            1,
            weight=1
        )

        # Encabezado

        titulo = ctk.CTkLabel(
            contenedor,
            text="Cancelar llamada",
            text_color=self.COLOR_TEXTO,
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        titulo.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w"
        )

        # Lista

        panel_lista = ctk.CTkFrame(
            contenedor,
            fg_color=self.COLOR_PANEL,
            corner_radius=12,
            border_width=1,
            border_color=self.COLOR_BORDE
        )

        panel_lista.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(0, 8),
            pady=(20, 0)
        )

        scroll = ctk.CTkScrollableFrame(
            panel_lista,
            fg_color="transparent"
        )

        scroll.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        # Detalle

        panel_detalle = ctk.CTkFrame(
            contenedor,
            fg_color=self.COLOR_PANEL,
            corner_radius=12,
            border_width=1,
            border_color=self.COLOR_BORDE
        )

        panel_detalle.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(8, 0),
            pady=(20, 0)
        )

        self._mostrar_detalle_accion_vacio(
            panel_detalle,
            "Seleccione una llamada para cancelar"
        )

        for llamada in llamadas:
            self._crear_item_accion_llamada(
                scroll,
                llamada,
                lambda llamada=llamada: (
                    self._mostrar_cancelacion_seleccionada(
                        ventana,
                        panel_detalle,
                        llamada
                    )
                )
            )
    
    def _mostrar_cancelacion_seleccionada(
        self,
        ventana: ctk.CTkToplevel,
        panel,
        llamada: Llamada
    ) -> None:
        """
        Muestra la información de la llamada
        seleccionada antes de cancelarla.
        """

        for widget in panel.winfo_children():
            widget.destroy()

        prioridad = (
            llamada.prioridad.value
            if llamada.prioridad is not None
            else "-"
        )

        color = self._obtener_color_prioridad(
            llamada.prioridad
        )

        titulo = ctk.CTkLabel(
            panel,
            text=llamada.id_llamada,
            text_color=self.COLOR_TEXTO,
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        titulo.pack(
            anchor="w",
            padx=25,
            pady=(28, 5)
        )

        prioridad_label = ctk.CTkLabel(
            panel,
            text=f"  {prioridad}  ",
            fg_color=color,
            text_color="#FFFFFF",
            corner_radius=6,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )

        prioridad_label.pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        self._crear_dato_detalle(
            panel,
            "Tipo",
            llamada.tipo
        )

        self._crear_dato_detalle(
            panel,
            "Ubicación",
            llamada.ubicacion
        )

        self._crear_dato_detalle(
            panel,
            "Estado",
            llamada.estado.value
        )

        advertencia = ctk.CTkLabel(
            panel,
            text=(
                "Esta acción retirará la llamada "
                "de su cola de espera."
            ),
            text_color=self.COLOR_ADVERTENCIA,
            wraplength=380,
            justify="left",
            font=ctk.CTkFont(
                size=12
            )
        )

        advertencia.pack(
            anchor="w",
            padx=25,
            pady=(25, 15)
        )

        boton = ctk.CTkButton(
            panel,
            text="Cancelar llamada",
            command=lambda: self._confirmar_cancelacion(
                ventana,
                llamada.id_llamada
            ),
            height=44,
            corner_radius=8,
            fg_color=self.COLOR_ERROR,
            hover_color="#DC2626",
            text_color="#FFFFFF",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        boton.pack(
            fill="x",
            padx=25,
            pady=(10, 25)
        )
    
    def _confirmar_cancelacion(
        self,
        ventana: ctk.CTkToplevel,
        id_llamada: str
    ) -> None:
        """
        Ejecuta la cancelación mediante GestorLlamadas.
        """

        try:
            llamada = (
                self.gestor
                .cancelar_llamada(
                    id_llamada
                )
            )

            self.actualizar_dashboard()

            ventana.destroy()

            self._mostrar_notificacion(
                titulo="Llamada cancelada",
                mensaje=(
                    f"{llamada.id_llamada} fue retirada "
                    "de la cola de espera."
                ),
                tipo="advertencia"
            )

        except (ValueError, RuntimeError) as error:
            self._mostrar_notificacion(
                titulo="No se pudo cancelar",
                mensaje=str(error),
                tipo="error"
            )
    
    def _crear_dato_detalle(
        self,
        padre,
        etiqueta: str,
        valor: str
    ) -> None:
        """
        Crea una fila de información dentro
        de la ficha de una llamada.
        """

        fila = ctk.CTkFrame(
            padre,
            fg_color="transparent"
        )

        fila.pack(
            fill="x",
            padx=22,
            pady=4
        )

        label = ctk.CTkLabel(
            fila,
            text=etiqueta,
            width=145,
            anchor="w",
            text_color=self.COLOR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                size=11
            )
        )

        label.pack(
            side="left"
        )

        dato = ctk.CTkLabel(
            fila,
            text=valor,
            anchor="w",
            text_color=self.COLOR_TEXTO,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )

        dato.pack(
            side="left",
            fill="x",
            expand=True
        )
    
    def _texto_booleano(
        self,
        valor: bool
    ) -> str:
        """
        Convierte un booleano en texto legible.
        """
        return "Sí" if valor else "No"
    
    def _procesar_registro_llamada(
        self,
        ventana: ctk.CTkToplevel,
        tipo: str,
        ubicacion: str,
        descripcion: str,
        personas: str,
        consciente: bool,
        respira: bool,
        heridos: bool,
        peligro_inmediato: bool,
        riesgo_potencial: bool,
        mensaje: ctk.CTkLabel
    ) -> None:
        """
        Valida los datos del formulario y registra
        la llamada mediante GestorLlamadas.
        """

        ubicacion = ubicacion.strip()
        descripcion = descripcion.strip()

        # -----------------------------------------------------
        # VALIDACIONES
        # -----------------------------------------------------

        if not ubicacion:
            mensaje.configure(
                text="Ingrese la ubicación de la emergencia.",
                text_color=self.COLOR_P1
            )
            return

        if not descripcion:
            mensaje.configure(
                text=(
                    "Ingrese una descripción "
                    "de la emergencia."
                ),
                text_color=self.COLOR_P1
            )
            return

        try:
            personas_afectadas = int(
                personas
            )

        except ValueError:
            mensaje.configure(
                text=(
                    "La cantidad de personas afectadas "
                    "debe ser un número entero."
                ),
                text_color=self.COLOR_P1
            )
            return

        if personas_afectadas < 0:
            mensaje.configure(
                text=(
                    "La cantidad de personas afectadas "
                    "no puede ser negativa."
                ),
                text_color=self.COLOR_P1
            )
            return

        # -----------------------------------------------------
        # REGISTRO
        # -----------------------------------------------------

        try:
            llamada = self.gestor.registrar_llamada(
                tipo=tipo,
                ubicacion=ubicacion,
                descripcion=descripcion,
                personas_afectadas=personas_afectadas,
                consciente=consciente,
                respira=respira,
                heridos=heridos,
                peligro_inmediato=peligro_inmediato,
                riesgo_potencial=riesgo_potencial,
            )

        except ValueError as error:
            mensaje.configure(
                text=str(error),
                text_color=self.COLOR_P1
            )
            return

        # -----------------------------------------------------
        # ACTUALIZAR DASHBOARD
        # -----------------------------------------------------

        self.actualizar_dashboard()

        prioridad = (
            llamada.prioridad.value
            if llamada.prioridad is not None
            else "-"
        )

        ventana.destroy()

        self._mostrar_notificacion(
            titulo="Llamada registrada",
            mensaje=(
                f"{llamada.id_llamada} fue clasificada "
                f"automáticamente como {prioridad}."
            ),
            tipo="exito"
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

    def _crear_vista_reclasificacion(
        self,
        ventana: ctk.CTkToplevel,
        llamadas: list[Llamada]
    ) -> None:
        """
        Construye el selector de llamadas para
        reclasificación.
        """

        contenedor = ctk.CTkFrame(
            ventana,
            fg_color=self.COLOR_FONDO,
            corner_radius=0
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=22
        )

        contenedor.grid_columnconfigure(
            0,
            weight=1
        )

        contenedor.grid_columnconfigure(
            1,
            weight=2
        )

        contenedor.grid_rowconfigure(
            1,
            weight=1
        )

        titulo = ctk.CTkLabel(
            contenedor,
            text="Reclasificar llamada",
            text_color=self.COLOR_TEXTO,
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        titulo.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w"
        )

        panel_lista = ctk.CTkFrame(
            contenedor,
            fg_color=self.COLOR_PANEL,
            corner_radius=12,
            border_width=1,
            border_color=self.COLOR_BORDE
        )

        panel_lista.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(0, 8),
            pady=(20, 0)
        )

        scroll = ctk.CTkScrollableFrame(
            panel_lista,
            fg_color="transparent"
        )

        scroll.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        panel_detalle = ctk.CTkFrame(
            contenedor,
            fg_color=self.COLOR_PANEL,
            corner_radius=12,
            border_width=1,
            border_color=self.COLOR_BORDE
        )

        panel_detalle.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(8, 0),
            pady=(20, 0)
        )

        self._mostrar_detalle_accion_vacio(
            panel_detalle,
            "Seleccione una llamada para reclasificar"
        )

        for llamada in llamadas:
            self._crear_item_accion_llamada(
                scroll,
                llamada,
                lambda llamada=llamada: (
                    self._mostrar_reclasificacion_seleccionada(
                        ventana,
                        panel_detalle,
                        llamada
                    )
                )
            )
    
    def _mostrar_reclasificacion_seleccionada(
        self,
        ventana: ctk.CTkToplevel,
        panel,
        llamada: Llamada
    ) -> None:
        """
        Muestra las opciones disponibles para cambiar
        la prioridad de una llamada.
        """

        for widget in panel.winfo_children():
            widget.destroy()

        prioridad_actual = llamada.prioridad

        if prioridad_actual is None:
            return

        titulo = ctk.CTkLabel(
            panel,
            text=llamada.id_llamada,
            text_color=self.COLOR_TEXTO,
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        titulo.pack(
            anchor="w",
            padx=25,
            pady=(28, 8)
        )

        self._crear_dato_detalle(
            panel,
            "Tipo",
            llamada.tipo
        )

        self._crear_dato_detalle(
            panel,
            "Ubicación",
            llamada.ubicacion
        )

        self._crear_dato_detalle(
            panel,
            "Prioridad actual",
            prioridad_actual.value
        )

        etiqueta = ctk.CTkLabel(
            panel,
            text="NUEVA PRIORIDAD",
            text_color=self.COLOR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )

        etiqueta.pack(
            anchor="w",
            padx=25,
            pady=(28, 8)
        )

        mapa_prioridades = {
            "P1 · CRÍTICA": Prioridad.CRITICA,
            "P2 · ALTA": Prioridad.ALTA,
            "P3 · NORMAL": Prioridad.NORMAL,
        }

        opciones = [
            texto
            for texto, prioridad in mapa_prioridades.items()
            if prioridad != prioridad_actual
        ]

        prioridad_var = ctk.StringVar(
            value=opciones[0]
        )

        selector = ctk.CTkOptionMenu(
            panel,
            values=opciones,
            variable=prioridad_var,
            height=40,
            corner_radius=8,
            fg_color=self.COLOR_ACCION,
            button_color=self.COLOR_ACCION_HOVER,
            button_hover_color=self.COLOR_ACCION,
            text_color="#FFFFFF"
        )

        selector.pack(
            fill="x",
            padx=25,
            pady=(0, 25)
        )

        boton = ctk.CTkButton(
            panel,
            text="Aplicar reclasificación",
            height=44,
            corner_radius=8,
            fg_color=self.COLOR_ACCION,
            hover_color=self.COLOR_ACCION_HOVER,
            text_color="#FFFFFF",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=lambda: self._confirmar_reclasificacion(
                ventana,
                llamada.id_llamada,
                prioridad_var.get(),
                mapa_prioridades
            )
        )

        boton.pack(
            fill="x",
            padx=25
        )
        
    def _confirmar_reclasificacion(
        self,
        ventana: ctk.CTkToplevel,
        id_llamada: str,
        seleccion: str,
        mapa_prioridades: dict[str, Prioridad]
    ) -> None:
        """
        Ejecuta el cambio de prioridad seleccionado.
        """

        nueva_prioridad = mapa_prioridades.get(
            seleccion
        )

        if nueva_prioridad is None:
            self._mostrar_notificacion(
                titulo="Prioridad inválida",
                mensaje=(
                    "Seleccione una prioridad válida."
                ),
                tipo="error"
            )
            return

        llamada_anterior = (
            self.gestor
            .obtener_llamada_registrada(
                id_llamada
            )
        )

        prioridad_anterior = (
            llamada_anterior.prioridad.value
            if (
                llamada_anterior is not None
                and llamada_anterior.prioridad is not None
            )
            else "-"
        )

        try:
            llamada = (
                self.gestor
                .reclasificar_llamada(
                    id_llamada,
                    nueva_prioridad
                )
            )

            self.actualizar_dashboard()

            ventana.destroy()

            self._mostrar_notificacion(
                titulo="Llamada reclasificada",
                mensaje=(
                    f"{llamada.id_llamada}: "
                    f"{prioridad_anterior} → "
                    f"{nueva_prioridad.value}"
                ),
                tipo="info"
            )

        except (ValueError, RuntimeError) as error:
            self._mostrar_notificacion(
                titulo="No se pudo reclasificar",
                mensaje=str(error),
                tipo="error"
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
        Actualiza todos los datos visuales del dashboard
        según el estado actual de GestorLlamadas.
        """

        # -----------------------------------------------------
        # CONTADORES DE PRIORIDAD
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # LLAMADA EN ATENCIÓN
        # -----------------------------------------------------

        llamada = self.gestor.llamada_en_atencion

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
                    f"{llamada.id_llamada}  ·  "
                    f"{prioridad}  ·  "
                    f"{llamada.tipo}  ·  "
                    f"{llamada.ubicacion}"
                )
            )

        # -----------------------------------------------------
        # CONTENIDO REAL DE LAS COLAS
        # -----------------------------------------------------

        self.label_cola_p1.configure(
            text=self._formatear_cola(
                self.gestor.cola_p1
            )
        )

        self.label_cola_p2.configure(
            text=self._formatear_cola(
                self.gestor.cola_p2
            )
        )

        self.label_cola_p3.configure(
            text=self._formatear_cola(
                self.gestor.cola_p3
            )
        )

    # ---------------------------------------------------------
    # ACCIONES
    # ---------------------------------------------------------

    def mostrar_inicio(self) -> None:
        self.actualizar_dashboard()

    def registrar_llamada(self) -> None:
        """
        Abre una ventana modal para registrar
        una nueva llamada de emergencia.
        """

        ventana = ctk.CTkToplevel(self)

        ventana.title(
            "Registrar llamada | SmartCall 123"
        )

        ventana.geometry(
            "650x720"
        )

        ventana.resizable(
            False,
            False
        )

        ventana.configure(
            fg_color=self.COLOR_FONDO
        )

        ventana.transient(self)
        ventana.grab_set()

        self._centrar_ventana_secundaria(
            ventana,
            650,
            720
        )

        self._crear_formulario_registro(
            ventana
        )

    def atender_siguiente(self) -> None:
        """
        Asigna la llamada de mayor prioridad disponible.
        """

        try:
            llamada = (
                self.gestor
                .atender_siguiente_llamada()
            )

            if llamada is None:
                self._mostrar_notificacion(
                    titulo="Sin llamadas pendientes",
                    mensaje=(
                        "Actualmente no existen llamadas "
                        "en las colas de espera."
                    ),
                    tipo="advertencia"
                )
                return

            self.actualizar_dashboard()

            prioridad = (
                llamada.prioridad.value
                if llamada.prioridad is not None
                else "-"
            )

            self._mostrar_notificacion(
                titulo="Llamada en atención",
                mensaje=(
                    f"{llamada.id_llamada} · "
                    f"{prioridad} · {llamada.tipo}"
                ),
                tipo="exito"
            )

        except RuntimeError as error:
            self._mostrar_notificacion(
                titulo="No se puede atender",
                mensaje=str(error),
                tipo="error"
            )

    def finalizar_atencion(self) -> None:
        """
        Finaliza la llamada que se encuentra
        actualmente en atención.
        """

        try:
            llamada = (
                self.gestor
                .finalizar_llamada_actual()
            )

            self.actualizar_dashboard()

            self._mostrar_notificacion(
                titulo="Atención finalizada",
                mensaje=(
                    f"{llamada.id_llamada} fue marcada "
                    "como atendida."
                ),
                tipo="exito"
            )

        except RuntimeError as error:
            self._mostrar_notificacion(
                titulo="No se puede finalizar",
                mensaje=str(error),
                tipo="error"
            )
    
    def buscar_llamada(self) -> None:
        """
        Abre una ventana para consultar las llamadas
        registradas en SmartCall 123.
        """

        llamadas = (
            self.gestor
            .obtener_llamadas_registradas()
        )

        if not llamadas:
            self._mostrar_notificacion(
                titulo="Sin llamadas registradas",
                mensaje=(
                    "Todavía no existen llamadas "
                    "para consultar."
                ),
                tipo="advertencia"
            )
            return

        ventana = ctk.CTkToplevel(self)

        ventana.title(
            "Consultar llamadas | SmartCall 123"
        )

        ventana.geometry(
            "900x620"
        )

        ventana.minsize(
            850,
            580
        )

        ventana.configure(
            fg_color=self.COLOR_FONDO
        )

        ventana.transient(self)
        ventana.grab_set()

        self._centrar_ventana_secundaria(
            ventana,
            900,
            620
        )

        self._crear_vista_busqueda(
            ventana,
            llamadas
        )
        
    def reclasificar_llamada(self) -> None:
        """
        Abre el selector visual para modificar
        la prioridad de una llamada en espera.
        """

        llamadas = (
            self.gestor
            .obtener_llamadas_en_espera()
        )

        if not llamadas:
            self._mostrar_notificacion(
                titulo="Sin llamadas disponibles",
                mensaje=(
                    "No existen llamadas en espera "
                    "para reclasificar."
                ),
                tipo="advertencia"
            )
            return

        ventana = ctk.CTkToplevel(self)

        ventana.title(
            "Reclasificar llamada | SmartCall 123"
        )

        ventana.geometry(
            "820x570"
        )

        ventana.resizable(
            False,
            False
        )

        ventana.configure(
            fg_color=self.COLOR_FONDO
        )

        ventana.transient(self)
        ventana.grab_set()

        self._centrar_ventana_secundaria(
            ventana,
            820,
            570
        )

        self._crear_vista_reclasificacion(
            ventana,
            llamadas
        )

    def cancelar_llamada(self) -> None:
        """
        Abre el selector visual de llamadas
        disponibles para cancelación.
        """

        llamadas = (
            self.gestor
            .obtener_llamadas_en_espera()
        )

        if not llamadas:
            self._mostrar_notificacion(
                titulo="Sin llamadas disponibles",
                mensaje=(
                    "No existen llamadas en espera "
                    "que puedan cancelarse."
                ),
                tipo="advertencia"
            )
            return

        ventana = ctk.CTkToplevel(self)

        ventana.title(
            "Cancelar llamada | SmartCall 123"
        )

        ventana.geometry(
            "820x560"
        )

        ventana.resizable(
            False,
            False
        )

        ventana.configure(
            fg_color=self.COLOR_FONDO
        )

        ventana.transient(self)
        ventana.grab_set()

        self._centrar_ventana_secundaria(
            ventana,
            820,
            560
        )

        self._crear_vista_cancelacion(
            ventana,
            llamadas
        )

    def deshacer_operacion(self) -> None:
        """
        Revierte la última operación utilizando
        la pila LIFO.
        """

        try:
            operacion = (
                self.gestor
                .deshacer_ultima_operacion()
            )

            self.actualizar_dashboard()

            self._mostrar_notificacion(
                titulo="Operación deshecha",
                mensaje=(
                    f"{operacion.tipo.value} · "
                    f"{operacion.id_llamada}"
                ),
                tipo="info"
            )

        except RuntimeError as error:
            self._mostrar_notificacion(
                titulo="No se puede deshacer",
                mensaje=str(error),
                tipo="advertencia"
            )