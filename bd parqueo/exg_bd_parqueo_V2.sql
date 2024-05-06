
/*----------------------------- BD_EXG_PARQUEO_v2 ---------------------------------------*/

CREATE TABLE piso(
    id INT NOT NULL,
    sigla_piso VARCHAR(10) NOT NULL,
    descripcion VARCHAR(250),
    PRIMARY KEY(id)
)engine = innodb;

CREATE TABLE lugar(
    id int NOT null auto_increment,
    nro_lugar varchar(4) not null,
    descripcion VARCHAR(250),
    estado char(1) not null CHECK (estado IN ('D','O', 'I')),-- disponible, ocupado, inactivo
    id_piso int not null,
    foreign key (id_piso) references piso(id),
    PRIMARY KEY(id)
)engine = innodb;

CREATE TABLE rol(
    id INT NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(250) NOT NULL,
    PRIMARY KEY(id)
)engine = innodb;

CREATE TABLE personal(
    id int NOT null auto_increment,
    nombres varchar(50) not null,
	apellido_p varchar(50) not null,
	apellido_m varchar(50),
    nro_ci varchar(15) not null unique,
	telefono varchar(15) not null,
	direccion varchar(250),
	estado char(1) not null CHECK (estado IN ('A','I')),
    PRIMARY KEY(id)
)engine=innodb;

CREATE TABLE usuario(
    id int NOT null auto_increment,
    usuario varchar(50) not null UNIQUE,
    password varchar(130) not null,
    estado char(1) not null CHECK (estado IN ('A','I')),
    id_personal int not null,
    id_rol int not null,
    foreign key (id_personal) references personal(id),
    foreign key (id_rol) references rol(id),
    PRIMARY KEY(id)
)engine = innodb;

CREATE TABLE encargado (
    id INT NOT NULL PRIMARY KEY,
	observacion varchar(250),
	estado char(1) not null CHECK (estado IN ('A','I')),
    FOREIGN KEY (id) REFERENCES personal(id)
) engine=InnoDB;

CREATE TABLE modelo_marca(
    id INT NOT NULL auto_increment,
    modelo VARCHAR(15) NOT NULL,
    marca VARCHAR(15) NOT NULL,
    PRIMARY KEY(id)
)engine = innodb;

CREATE TABLE vehiculo(
    id int NOT null auto_increment,
    placa varchar(10) not null UNIQUE,
	color varchar(20) not null,
	id_modelo_marca int not null,
	FOREIGN KEY (id_modelo_marca) REFERENCES modelo_marca(id),
    PRIMARY KEY(id)
)engine=innodb;

CREATE TABLE servicio_visitante(
    id int NOT null auto_increment,
	nombre varchar(30) not null,
    precio NUMERIC(10, 2) not null,
	descripcion varchar(250) not null,
	estado char(1) not null CHECK (estado IN ('A','I')),
    PRIMARY KEY(id)
)engine=innodb;

CREATE TABLE ticket(
    id int NOT null auto_increment,
	hora_ingreso datetime not null,
	hora_salida datetime,
	estado char(1) not null CHECK (estado IN ('A','I')),
	id_lugar int not null,
	id_vehiculo int not null,
	id_encargado int not null,
	FOREIGN KEY (id_lugar) REFERENCES lugar(id),
	FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id),
	FOREIGN KEY (id_encargado) REFERENCES encargado(id),
    PRIMARY KEY(id)
)engine=innodb;

CREATE TABLE pago_ticket_visitante(
    id int NOT null auto_increment,
    monto NUMERIC(10, 2),
	observacion varchar(250),
	fecha_registro datetime,
	estado char(1) not null CHECK (estado IN ('P','R','A')), -- Pendiente, Realizado, Anulado
	id_servicio_visitante int,
	id_ticket int not null,
	FOREIGN KEY (id_servicio_visitante) REFERENCES servicio_visitante(id),
	FOREIGN KEY (id_ticket) REFERENCES ticket(id),
    PRIMARY KEY(id)
)engine=innodb;

CREATE TABLE cliente(
    id int NOT null auto_increment,
    nombres varchar(50) not null,
	apellido_p varchar(50) not null,
	apellido_m varchar(50),
	nro_ci varchar(10) not null unique,
	email varchar(150),
	telefono varchar(15) not null,
	direccion varchar(250),
	estado_contrato char(1) not null CHECK (estado_contrato IN ('A','I')),
    PRIMARY KEY(id)
)engine=innodb;

CREATE TABLE vehiculo_cliente(
    estado char(1) not null CHECK (estado IN ('A','I')),
	id_vehiculo int not null,
	id_cliente int not null,
	FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id),
	FOREIGN KEY (id_cliente) REFERENCES cliente(id),
    PRIMARY KEY(id_vehiculo,id_cliente)
)engine=innodb;

CREATE TABLE servicio_abonado(
    id int NOT null auto_increment,
	nombre varchar(30) not null,
    precio NUMERIC(10, 2) not null,
	descripcion varchar(250) not null,
	estado char(1) not null CHECK (estado IN ('A','I')),
    PRIMARY KEY(id)
)engine=innodb;


CREATE TABLE contrato(
    id int NOT null auto_increment,
    fecha_inicio date not null,
	fecha_fin date not null,
	estado char(1) not null CHECK (estado IN ('A','I','E')),-- activo, inactivo, esperas
	fecha_registro datetime not null,
	id_servicio_abonado int not null,
	id_cliente int not null,
	FOREIGN KEY (id_servicio_abonado) REFERENCES servicio_abonado(id),
	FOREIGN KEY (id_cliente) REFERENCES cliente(id),
    PRIMARY KEY(id)
)engine=innodb;

CREATE TABLE pago_contrato(
    id int NOT null auto_increment,
    monto NUMERIC(10, 2) not null,
	observacion varchar(250),
	fecha_registro datetime,
	estado char(1) not null CHECK (estado IN ('P','R','A')), -- Pendiente, Realizado, Anulado
	id_contrato int not null,
	FOREIGN KEY (id_contrato) REFERENCES contrato(id),
    PRIMARY KEY(id)
)engine=innodb;










