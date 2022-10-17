use studentfeedback;
create table Course (
CourseID int ,
CourseName varchar(255) , 
TeacherID int ,
PRIMARY KEY (CourseID),
FOREIGN KEY (TeacherID) REFERENCES Teacher(TeacherID)
);

insert into Course 
Values 
 ('1' ,  'Software Engineering' , '2') ,
 ('2' , 'Artificial Intelligence' , '3' ), 
('3' , 'Introduction to Data Science' , '4') ,
 ('4' ,  'Computer Security' , '6') , 
('5' ,  'KRR' , '7') ,
 ('6' ,  'Web Security' , '5') ,
('7' ,  'Integrated Software Development lab' , '1') ;