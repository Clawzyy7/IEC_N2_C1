# Sistema de Turnos Médicos — Evaluación 3 POO (INACAP Temuco)

Aplicación de consola multicapa en Python para administrar la atención de una clínica:
especialidades, profesionales, horarios, pacientes, citas, fichas e historial clínico.
Usa **Peewee** (ORM) con MySQL, **Bcrypt** para proteger contraseñas, **Maskpass** para ocultarlas
al escribirlas y **PrettyTable** para mostrar los datos. El acceso requiere **inicio de sesión**.

El diagrama de clases está en la raíz: `diagrama_de_clases_principal_programacion.drawio`.

## Integrantes

- Marco Lefiman
- Javier Inalef
- Matías Campos

Asignatura: Programación Orientada a Objetos · INACAP Temuco · Evaluación N°3 (continuación de la Evaluación N°2).

## Estructura

```
├── datos/
│   ├── conexion.py        Conexión Peewee/MySQL e inicialización de la BD
│   ├── model_base.py      ModelBase: configuración compartida por todos los modelos
│   ├── modelos/           Una clase Peewee por entidad (todas heredan de ModelBase)
│   ├── repositorio/       repo_base.py y un repositorio por entidad (único acceso a la BD)
│   └── sql/               Scripts de creación de tablas y datos iniciales (nombre = fecha y hora)
├── negocio/               Reglas del sistema, hash bcrypt, autenticación y sesión
├── presentacion/          Menús de consola (login, módulos CRUD)
├── auxiliares/            Validaciones, mensajes, configuración (.env), formatos y excepciones
├── .env                   Parámetros de conexión (NO se sube a GitHub)  ·  .env.example
├── README.md
├── main.py                Punto de entrada: arma las capas y lanza el login
└── requirements.txt
```

Regla de capas: **presentación → negocio → repositorio → base de datos**. La presentación nunca
toca un repositorio y solo el repositorio ejecuta consultas.

## Dependencias

`peewee`, `PyMySQL`, `python-dotenv`, `bcrypt`, `maskpass`, `prettytable` (ver `requirements.txt`).

## Persistencia con ORM (Peewee)

- `datos/conexion.py` define la conexión (`db`, `MySQLDatabase`) con los datos del `.env`.
- `datos/model_base.py` define `ModelBase`, que asigna esa base de datos a todos los modelos.
- Cada modelo de `datos/modelos/` hereda de `ModelBase`, por ejemplo `class Paciente(PersonaMixin, ModelBase)`.
- Cada repositorio de `datos/repositorio/` guarda con `save()` (`RepoBase.guardar`), lista (`listar`) y
  tiene sus búsquedas (`buscar_por_rut`, `buscar_por_email`, `listar_por_profesional`, etc.).

## Instalación y ejecución

1. Tener **MySQL** instalado y en ejecución.
2. (Opcional) crear un entorno virtual: `python -m venv venv` y activarlo.
3. Instalar dependencias: `pip install -r requirements.txt`
4. Copiar `.env.example` a `.env` y escribir el usuario y la clave de MySQL
   (`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`).
5. Ejecutar: `python main.py`

### Creación de la base de datos

En el menú de acceso elegir **9. Inicializar base de datos**. Crea la BD (`DB_NAME`) si no existe y
ejecuta en orden los scripts de `datos/sql/` (tablas, estados de cita y especialidades base). Se puede
repetir sin duplicar datos.

### Usuario inicial

No hay un usuario precargado ni contraseñas guardadas en los scripts SQL. El primer usuario se crea desde el
menú de acceso con la opción **2. Crear cuenta** (la contraseña se guarda como hash Bcrypt).
Esa opción **solo aparece mientras no exista ningún usuario**: una vez creado el primero, desaparece del
menú de acceso y las cuentas nuevas se crean con sesión iniciada, desde el módulo **9. Usuarios**.

### Primer uso

1. Opción **9** (inicializar BD). 2. Opción **2** (crear cuenta). 3. Opción **1** (iniciar sesión).
Con la sesión activa aparece el menú principal con los módulos 1 a 9.

## Menú principal

| Opción | Módulo | Acciones |
|---|---|---|
| 1 | Especialidades | CRUD |
| 2 | Profesionales | CRUD, buscar por RUT, consultar agenda, agendar hora |
| 3 | Horarios de atención | CRUD (jornadas por profesional y fecha) |
| 4 | Pacientes | CRUD, buscar por RUT, solicitar cita, consultar historial |
| 5 | Citas | Reservar, modificar, cancelar, confirmar, marcar atendida, filtrar |
| 6 | Estados | CRUD, habilitar / deshabilitar |
| 7 | Fichas de pacientes | CRUD, consultar ficha de un paciente, anular |
| 8 | Historial clínico | CRUD |
| 9 | Usuarios | CRUD, buscar por correo, cambiar mi contraseña, deshabilitar |

## Seguridad

- Las contraseñas se piden con Maskpass (no se ven al escribir) y se guardan como **hash Bcrypt**; nunca en texto plano.
- Al iniciar sesión se compara la contraseña con el hash usando `bcrypt.checkpw`. El mensaje de error es el
  mismo si falla el correo o la contraseña, y tras 3 intentos fallidos se vuelve al menú de acceso.
- Sin sesión activa no se puede entrar al menú principal. El registro libre solo existe para el primer usuario. Un usuario no puede deshabilitar su propia cuenta.
- Contraseña: mínimo 8 caracteres, con letras y números.

## Reglas de negocio principales

- RUT chileno validado con módulo 11; correo y teléfono con formato válido; RUT y correo únicos.
- Un profesional no puede tener dos jornadas que se solapen el mismo día; no se registran jornadas en fechas pasadas.
- Citas: `Reservada → Confirmada → Atendida`, y `Reservada/Confirmada → Cancelada`.
- Un paciente tiene una sola ficha (relación 1:1); el historial se valida contra su ficha y su cita.
- Eliminar: baja lógica (`habilitado = 0`) en las tablas que tienen ese campo; borrado real en `cita`,
  `ficha_paciente` e `historial_clinica`.

## Principios de POO aplicados

| Principio | Dónde |
|---|---|
| Abstracción | `NegocioBase`, `RepoBase`, `PresentacionBase` (clases abstractas con `ABC`) |
| Encapsulamiento | Acceso a la BD solo en los repositorios; validación en `auxiliares`; contraseñas solo como hash |
| Herencia | Todos los modelos → `ModelBase`; `Paciente`/`Profesional`/`Usuario` → `PersonaMixin`; `NegocioProfesionales`/`NegocioPacientes` → `NegocioPersona` → `NegocioBase` |
| Polimorfismo | Sobrescritura: `_reglas()`, `_fila()`, `_extras()`, `agregar()` en las hijas. Sobrecarga (argumentos por defecto): `NegocioCitas.reservar()` y `listar_citas()` |

## Métodos del diagrama UML y dónde están

| Clase | Métodos del diagrama | Implementación |
|---|---|---|
| Especialidad | agregar, modificar | `NegocioBase.agregar / modificar` |
| Profesional | consultarAgenda, agendarHora | `NegocioProfesionales.consultar_agenda / agendar_hora` |
| HorarioAtencion | registrarJornada, modificarJornada | `NegocioHorarios.registrar_jornada / modificar_jornada` |
| Paciente | solicitarCita, consultarHistorial | `NegocioPacientes.solicitar_cita / consultar_historial` |
| Cita | reservar, confirmar, cancelar | `NegocioCitas.reservar / confirmar / cancelar` (más `atender`) |
| Estado | obtenerEstado, cambiarEstado | `NegocioEstados.obtener_estado / cambiar_estado` |
| Ficha_paciente | consultar_Ficha, modificar_Ficha, anular_Ficha | `NegocioFichas.consultar_ficha / modificar_ficha / anular_ficha` |
| Historial_clinica | registrar, consultar, modificar | `NegocioHistoriales.registrar_historial / consultar_historial / modificar_historial` |
| Usuario | registrarUsuario, autenticar, cambiarContrasena | `NegocioUsuarios.registrar_usuario / autenticar / cambiar_contrasena` |
