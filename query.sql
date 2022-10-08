create database db_agenda;
use db_agenda;
create table contactos(
    id_contacto int primary key auto_increment,
    nombre varchar(200) not null,
    telefono varchar(30) not null,
    correo varchar(100) not null
);