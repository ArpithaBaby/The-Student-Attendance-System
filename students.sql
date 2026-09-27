set SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
start transaction;
set time_zone = "+00:00";

create table STUDENT (ID int not null auto_increment, ROLLNO varchar(20) not null, SNAME varchar(50) not null, SEM int not null, GENDER varchar(50) not null, BRANCH varchar(50) not null, EMAIL varchar(50) not null, NUMBER varchar(12) not null, ADDRESS text not null, primary key(ID));

create table ATTENDENCE (AID int not null, ROLLNO varchar(20) not null, ATTENDANCE int not null, primary key(AID), Foreign Key (AID) references STUDENT(ID));

create table DEPARTMENT (CID int not null, BRANCH varchar(50) not null, primary key(CID), Foreign Key (CID) references STUDENT(ID));

create table TRIG (TID int not null, ROLLNO varchar(50) not null, ACTION varchar(50) not null, TIMESTAMP datetime not null, primary key(TID), Foreign Key (TID) references STUDENT(ID));

create table TEST (ID int not null, NAME varchar(52) not null, EMAIL varchar(50) not null, primary key(ID), Foreign Key (ID) references STUDENT(ID));

create table USER (ID int not null, USERNAME varchar(50) not null, EMAIL varchar(50) not null, PASSWORD varchar(500) not null, primary key(ID), Foreign Key (ID) references STUDENT(ID));

delimiter $$
create trigger DELETE before delete on STUDENT for each row 
insert into TRIG values(null, old.ROLLNO, 'STUDENT DELETED', now());
$$
delimiter ;

delimiter $$
create trigger INSERT after insert on STUDENT for each row 
insert into TRIG values(null, new.ROLLNO, 'STUDENT INSERTED', now());
$$
delimiter ;

delimiter $$
create trigger UPDATE after update on STUDENT for each row 
insert into TRIG values(null, new.ROLLNO, 'STUDENT UPDATED', now());
$$
delimiter ;

COMMIT;


