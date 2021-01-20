create table companies
(
	symbol varchar(128) not null
		constraint company_pk
			primary key,
	name text not null,
	available_shares integer default 0,
	last_update timestamp with time zone
);

CREATE TABLE prices
(
	company_symbol varchar PRIMARY KEY,
	price double,
	currency varchar,
	timestamp timestamp with time zone,
	FOREIGN KEY (company_symbol) REFERENCES companies(symbol) ON DELETE CASCADE
);

CREATE TABLE shares_owned_by_user
(
	company_symbol varchar(128),
	username text,
	shares_owned int,
	PRIMARY KEY (company_symbol, username)
);

CREATE TABLE transactions
(
	transaction_id uuid PRIMARY KEY,
	symbol varchar(128),
	username varchar(60),
	transaction_type smallint,
	transaction_at timestamp with time zone,
	amount bigint,
	total bigint,
	currency varchar(4),
	FOREIGN KEY (symbol) REFERENCES companies(symbol),
	FOREIGN KEY (username) REFERENCES users(username)
);

CREATE TABLE users(
	username text PRIMARY KEY,
	password text,
	balance bigint
)