CREATE TABLE public.users (
	tg_name varchar NOT NULL,
	"scope" int4 NULL,
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	upd_time time NULL,
	CONSTRAINT users_pk PRIMARY KEY (id),
	CONSTRAINT users_un UNIQUE (tg_name)
);

CREATE TABLE public.grades (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	"name" varchar NOT NULL,
	max_scope int4 NULL,
	CONSTRAINT grades_pk PRIMARY KEY (id),
	CONSTRAINT grades_un UNIQUE (name)
);

insert into grades (name, max_scope) values ('TRAINEE I',150);
insert into grades (name, max_scope) values ('TRAINEE II',300);
insert into grades (name, max_scope) values ('TRAINEE III',450);
insert into grades (name, max_scope) values ('TRAINEE IV',600);
insert into grades (name, max_scope) values ('TRAINEE +',750);
insert into grades (name, max_scope) values ('JUNIOR I',850);
insert into grades (name, max_scope) values ('JUNIOR II',1231);
insert into grades (name, max_scope) values ('JUNIOR III',1613);
insert into grades (name, max_scope) values ('JUNIOR IV',1994);
insert into grades (name, max_scope) values ('JUNIOR +',2375);
insert into grades (name, max_scope) values ('MIDDLE I',2475);
insert into grades (name, max_scope) values ('MIDDLE II',2872);
insert into grades (name, max_scope) values ('MIDDLE III',3269);
insert into grades (name, max_scope) values ('MIDDLE IV',3666);
insert into grades (name, max_scope) values ('MIDDLE +',4063);
insert into grades (name, max_scope) values ('SENIOR I',4163);
insert into grades (name, max_scope) values ('SENIOR II',5786);
insert into grades (name, max_scope) values ('SENIOR III',7409);
insert into grades (name, max_scope) values ('SENIOR IV',9033);
insert into grades (name, max_scope) values ('SENIOR +',10656);
commit;