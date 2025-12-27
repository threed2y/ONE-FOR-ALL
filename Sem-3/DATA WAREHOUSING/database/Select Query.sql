select * from film;
select film_id, title, rental_rate, length from film;
select 
  film_id FilmID, 
  title Title, 
  rental_rate Rental, 
  length Length 
from film;
select 
  film_id "FilmID", 
  title "Title", 
  rental_rate "Rental", 
  length "Length" 
from film;
select * from film 
  where rental_rate < 3;
select film_id, title, rental_rate, length 
  from film 
  where rental_rate < 3;
select film_id, title, rental_rate, length 
  from film 
  where rental_rate < 3 and length >= 100;

select 
  film_id "FilmID", 
  title "Title", 
  rental_rate "Rental", 
  length "Length" 
from film 
where rental_rate < 3 and length >= 100;

select 
  film_id "Film ID", 
  title "Title of Film", 
  rental_rate "Rental", 
  length "Length of Film" 
from film 
where rental_rate < 3 and length >= 100
order by length;

select 
  film_id "Film ID", 
  title "Title of Film", 
  rental_rate "Rental", 
  length "Length of Film" 
from film 
where rental_rate < 3 and length >= 100
order by length desc;

select 
  film_id "Film ID", 
  title "Title of Film", 
  rental_rate "Rental", 
  length "Length of Film" 
from film 
where rental_rate < 3 and length >= 100
order by rental_rate, length desc;

select 
  film_id "Film ID", 
  title "Title of Film", 
  rental_rate "Rental", 
  rental_rate*7 "Weekly Rental",
  length "Length of Film", 
  upper(name) "Language"
from film, language 
where film.language_id = language.language_id;

select rental_rate, count(*) "Number of Films" 
from film 
group by rental_rate 
having rental_rate < 3
order by rental_rate;

select * from film limit 5;