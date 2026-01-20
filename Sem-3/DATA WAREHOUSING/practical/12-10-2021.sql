create table student_info
 (StudID int primary key,
  FirstName varchar(20) not null,
  LastName varchar(20),
  DOB date not null,
  loc varchar(40),
  Hobby varchar(30),
  DreamJob varchar(50)
 )
;
create table student_edu
 (stud_eid char(3) primary key,
  qualification char(2),
  grade_points float(4),
  admission_year_ug int,
  admission_year_pg int,
  prn int not null references student_info(studid)
 )
;
insert into student_info
 values('001','jerry',null,'04-02-00','jam','writing poetries' 
 )
;
 
select * from student_info;