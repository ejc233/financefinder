drop table if exists actions;
drop table if exists params;
create table actions (
  action text primary key ,
  paramNums integer not null
);
create table params(
	actionName text not null,
	paramName text not null,
	foreign key (actionName) references actions(action)
);
insert into actions values ("Show deposits", 1);
insert into actions values ("Show withdrawals", 1);
insert into actions values ("Show all transactions", 1);
insert into actions values ("Average inflow", 3);
insert into actions	values ("Average outflow", 3);
insert into actions values ("Daily average inflow", 3);
insert into actions values ("Daily average outflow", 3);
insert into actions values ("Daily average net", 3);

insert into params values("Show deposits", "AcctList");
insert into params values("Show withdrawals", "AcctList");
insert into params values("Show all tranactions", "AcctList");
insert into params values("Average inflow", "AcctList");
insert into params values("Average inflow", "Final Date");
insert into params values("Average inflow", "Number of Days");
insert into params values("Average outflow", "AcctList");
insert into params values("Average outflow", "Final Date");
insert into params values("Average outflow", "Number of Days");
insert into params values("Daily average outflow", "AcctList");	
insert into params values("Daily average outflow", "Final Date");
insert into params values("Daily average outflow", "Number of Days");
insert into params values("Daily average net", "AcctList");
insert into params values("Daily average net", "Final Date")
insert into params values("Daily average net", "Number of Days")	