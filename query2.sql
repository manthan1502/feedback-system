use studentfeedback;
create table Student(
StudentID int ,
StudentName varchar(255) ,
StudentPwd varchar(255) 
);
alter table Student
add primary key (StudentID);

insert into Student 
Values 
 ('1' ,  'Sameer' , 'Sameer@123') ,
 ('2' , 'Manthan' , 'Manthan@123' ), 
('3' , 'Devang' , 'Devang@123') ,
 ('4' ,  'Pranjal' , 'Pranjal@123') , 
('5' ,  'Priyansh' , 'Priyansh@123') ,
 ('6' ,  'Anshuman' , 'Anshuman@123') ,
('7' ,  'Shivam' , 'Shivam@123') ;

