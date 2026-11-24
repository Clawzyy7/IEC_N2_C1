-- Atención: horarios, citas, fichas e historial clínico
CREATE TABLE IF NOT EXISTS horario_atencion (
    id_horario      INT AUTO_INCREMENT PRIMARY KEY,
    id_profesional  INT        NOT NULL,
    fecha           DATE       NOT NULL,
    hora_inicio     TIME       NOT NULL,
    hora_fin        TIME       NOT NULL,
    duracion_bloque INT        NOT NULL,
    habilitado      TINYINT(1) NOT NULL DEFAULT 1,
    FOREIGN KEY (id_profesional) REFERENCES profesional(id_profesional)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS cita (
    id_cita        INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente    INT          NOT NULL,
    id_profesional INT          NOT NULL,
    id_estado      INT          NOT NULL,
    observaciones  VARCHAR(255) NOT NULL DEFAULT '',
    fecha_registro DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_paciente)    REFERENCES paciente(id_paciente),
    FOREIGN KEY (id_profesional) REFERENCES profesional(id_profesional),
    FOREIGN KEY (id_estado)      REFERENCES estado(id_estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ficha_paciente (
    id_ficha    INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT          NOT NULL UNIQUE,
    motivo      VARCHAR(255) NOT NULL,
    diagnostico VARCHAR(500) NOT NULL DEFAULT '',
    tratamiento VARCHAR(500) NOT NULL DEFAULT '',
    FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS historial_clinica (
    id_historial        INT AUTO_INCREMENT PRIMARY KEY,
    id_ficha            INT          NOT NULL,
    id_paciente         INT          NOT NULL,
    id_cita             INT          NOT NULL,
    motivo              VARCHAR(255) NOT NULL,
    diagnostico         VARCHAR(500) NOT NULL DEFAULT '',
    tratamiento         VARCHAR(500) NOT NULL DEFAULT '',
    observaciones       VARCHAR(255) NOT NULL DEFAULT '',
    fecha_actualizacion DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_ficha)    REFERENCES ficha_paciente(id_ficha),
    FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente),
    FOREIGN KEY (id_cita)     REFERENCES cita(id_cita)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
