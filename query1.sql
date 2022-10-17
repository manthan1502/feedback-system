-- create database StudentFeedback;
use StudentFeedback;
create table Teacher(
TeacherID int ,
TeacherName varchar(255) ,
TeacherPwd varchar(255) 
);
alter table Teacher
add primary key (TeacherID);

insert into Teacher 
Values 
 ('1' ,  'Mukesh' , 'Mukesh@123') ,
 ('2' ,  'Saurabh' , 'Saurabh@123' ), 
('3' ,  'Poulami' , 'Poulami@123') ,
 ('4' , 'Aloke' , 'Aloke@123') , 
('5' , 'Mohit' , 'Mohit@123') ,
 ('6' , 'Shweta' , 'Shweta@123') ,
('7' , 'Ravi' , 'Ravi@123') ;

