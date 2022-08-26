drop database if exists recognization;
create database recognization CHARACTER SET utf8 COLLATE utf8_general_ci;
use recognization;
create table user(
	id int primary key auto_increment,
    nickname varchar(50),
    gender int,
    telephone varchar(11) unique,
    address varchar(100),
    password varchar(100)
)CHARACTER SET utf8 COLLATE utf8_general_ci;

use recognization;
insert into user(id,telephone,password) values(null,'18202275875','123');
select * from user;