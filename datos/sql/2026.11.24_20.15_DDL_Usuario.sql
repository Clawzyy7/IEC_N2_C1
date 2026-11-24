-- Usuarios del sistema. La contraseña NUNCA se guarda en texto plano:
-- password_hash almacena el hash bcrypt (60 caracteres).
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario     INT AUTO_INCREMENT PRIMARY KEY,
    nombres        VARCHAR(80)  NOT NULL,
    apellidos      VARCHAR(80)  NOT NULL,
    email          VARCHAR(100) NOT NULL UNIQUE,
    password_hash  CHAR(60)     NOT NULL,
    habilitado     TINYINT(1)   NOT NULL DEFAULT 1,
    fecha_creacion DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
