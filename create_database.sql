create database TWS;
use TWS;

create table EMPLOYEE (
	EID		varchar(10) not null,
	Name	varchar(10) not null,
	Depart	varchar(20),
	Soncmp	varchar(20),
	Worktype varchar(10),  -- normal or expert;
	primary key (EID)
);

create table TOOL (
	TID		varchar(10) not null,
	Name	varchar(10) not null,
	Tooltype varchar(10),  -- expensive or cheap
	Soncmp	varchar(20),
	Good	boolean default true,
	primary key (TID)
);

create table LEND (
	LID	 varchar(10) not null,
	Lendtime time,
	EID		varchar(10) not null,
	TID		varchar(10) not null,
	foreign key (EID) references EMPLOYEE(EID) ON DELETE CASCADE,
	foreign key (TID) references TOOL(TID) ON DELETE CASCADE,
	primary key (LID, EID, TID)
);

create table LOGIN (
	EID		varchar(10) not null,
	Password varchar(10) not null,
	foreign key (EID) references EMPLOYEE(EID) ON DELETE CASCADE,
	primary key (EID, Password)
);


create table LENDTMP (
	EID		varchar(10) not null,
	Lendtime	time,
	TID		varchar(10) not null,
	primary key (EID, TID, Lendtime));

