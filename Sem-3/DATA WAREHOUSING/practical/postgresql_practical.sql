create table category(
cat_code varchar(5) primary key,
cat_name char(20));

create table author_details(
auth_code varchar(5) primary key,
auth_name char(20),
books_number int);

DROP TABLE IF EXISTS book_details;

create table book_details(
book_code varchar(5) primary key,
book_name char(20),
author_code char(5) references author_details(auth_code),
category_code char(5) references category(cat_code),
publishing_year int);

#####################################################
select * from category;
select * from author_details;
select * from book_details;
#####################################################

COPY category FROM 'D:\\Shrey Pandya\\2021 22 backup\\MSU Material\\2021_22\\Statistics\\ODD\\MSc Final\\category.csv' 
DELIMITER ',' csv header;

COPY author_details FROM 'D:\\Shrey Pandya\\2021 22 backup\\MSU Material\\2021_22\\Statistics\\ODD\\MSc Final\\author.csv' 
DELIMITER ',' csv header;

COPY book_details FROM 'D:\\Shrey Pandya\\2021 22 backup\\MSU Material\\2021_22\\Statistics\\ODD\\MSc Final\\books.csv' 
DELIMITER ',' csv header;

#####################################################

select book_name from book_details; 
select book_name from book_details where author_code= 'A9'; 
select * from book_details where author_code= 'A9';
select book_name,publishing_year from book_details where author_code= 'A9'; 

select count(book_name) from book_details where author_code = 'A9';
select book_name,publishing_year from book_details where publishing_year > 1995;

select distinct(author_code) from book_details;

select distinct(count(author_code)) from book_details;
select distinct(author_code) from book_details;
select distinct(author_code) from book_details order by author_code desc;
select distinct(author_code) from book_details order by author_code;

select author_code,count(author_code) from book_details group by author_code;
select author_code,count(*) from book_details group by author_code;

select min(publishing_year) from book_details ;
select book_name,min(publishing_year) from book_details group by book_name;
select author_code,max(publishing_year) from book_details group by author_code;


select author_code,sum(publishing_year) from book_details group by author_code;
select  * from category where cat_name like '%c%';
select  * from category where cat_name like 'C%';
select  * from category where cat_name like '_n%';

select  concat(book_code,'',book_name) as concat_code from book_details;

















