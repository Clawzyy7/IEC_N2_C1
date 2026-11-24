-- Personas: profesionales y pacientes
CREATE TABLE IF NOT EXISTS profesional (
    id_profesional  INT AUTO_INCREMENT PRIMARY KEY,
    rut             VARCHAR(12)  NOT NULL UNIQUE,
    nombres         VARCHAR(80)  NOT NULL,
    apellidos       VARCHAR(80)  NOT NULL,
    id_especialidad INT          NOT NULL,
    telefono        VARCHAR(15)  NOT NULL,
    email           VARCHAR(100) NOT NULL,
    habilitado      TINYINT(1)   NOT NULL DEFAULT 1,
    FOREIGN KEY (id_especialidad) REFERENCES especialidad(id_especialidad)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS paciente (
    id_paciente      INT AUTO_INCREMENT PRIMARY KEY,
    rut              VARCHAR(12)  NOT NULL UNIQUE,
    nombres          VARCHAR(80)  NOT NULL,
    apellidos        VARCHAR(80)  NOT NULL,
    fecha_nacimiento DATE         NOT NULL,
    telefono         VARCHAR(15)  NOT NULL,
    email            VARCHAR(100) NOT NULL,
    habilitado       TINYINT(1)   NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
