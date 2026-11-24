-- Catálogos: especialidades médicas y estados de las citas
CREATE TABLE IF NOT EXISTS especialidad (
    id_especialidad INT AUTO_INCREMENT PRIMARY KEY,
    especialidad    VARCHAR(80)  NOT NULL UNIQUE,
    descripcion     VARCHAR(200) NOT NULL DEFAULT '',
    habilitado      TINYINT(1)   NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS estado (
    id_estado   INT AUTO_INCREMENT PRIMARY KEY,
    estado      VARCHAR(80)  NOT NULL UNIQUE,
    descripcion VARCHAR(200) NOT NULL DEFAULT '',
    habilitado  TINYINT(1)   NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
