drop table if exists actions;
create table actions (
  action text primary key ,
  paramNums integer not null
);
create table params(
	actionName text not null,
	paramName text not null,
	foreign key (actionName) references actions(action)
);
