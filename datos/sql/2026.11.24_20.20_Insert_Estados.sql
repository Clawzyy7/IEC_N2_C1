-- Estados de las citas. INSERT IGNORE evita duplicados si se inicializa más de una vez.
INSERT IGNORE INTO estado (estado, descripcion) VALUES
    ('Reservada',  'Cita solicitada, pendiente de confirmación'),
    ('Confirmada', 'Cita confirmada'),
    ('Atendida',   'El paciente fue atendido'),
    ('Cancelada',  'Cita cancelada');
