create table companies
(
	symbol varchar(128) not null
		constraint company_pk
			primary key,
	name text not null,
	available_shares integer default 0,
	last_update timestamp with time zone
);
