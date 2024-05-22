create database OnlineRecipe;
use OnlineRecipe;
create table recipies(
r_id int primary key auto_increment,
r_name varchar(50) NOT NULL,
ingredients TEXT NOT NULL,
instructions TEXT NOT NULL,
cook_time varchar(50) NOT NULL,
serve_size int NOT NULL,
user_id int references users(id) on delete cascade,
category varchar(20) NOT NULL);

create table users(
id int primary key auto_increment,
username varchar(60) NOT NULL,
email varchar(100) NOT NULL,
password TEXT NOT NULL);

create table comments(
c_id int primary key auto_increment,
recipie_id int references recipies(r_id) on delete cascade,
user_id int references users(id) on delete cascade,
comment TEXT NOT NULL,
date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

insert into users (username,email,password) values ('abcd','abcd@gmail.com',1234);
insert into recipies (r_name,ingredients,instructions,cook_time,serve_size,user_id,category) values ('Chicken roast','500 gm of chicken with bones cut into medium-sized pieces
4 large onions sliced long
4 green chillies slit lengthwise
1 to mato chopped
4 tbsp of curd
1/2 tsp of turmeric powder
2 tsp of red chilli powder
3 tbsp of oil
1 tsp of cloves + cinnamon + peeled cardamom crushed together
A pinch of red food colour optional
1 tsp of chicken masala
1 strand of curry leaves
1/4 tsp of fennel seeds
2 tsp of coriander powder
1/2 tsp of mustard seeds
3 tsp of freshly crushed garlic
1 tsp of freshly crushed ginger','Marinate the chicken pieces in curd, red chilli powder, turmeric powder, and salt for 30 mins. If you need to leave it longer, refrigerate it.
Heat oil and add the mustard seeds and fennel seeds. When they pop and sizzle, add the sliced onions and green chillies. Reduce flame to medium-low and fry the onions until they turn golden brown. The amount of oil at this stage should be on the higher side so add a bit more of you feel its not.
Next, add the coriander powder and the freshly crushed masala (cloves, etc) and fry for 10 seconds. Top off with the ginger garlic paste and sautè for another 30 seconds until the mixture turns fragrant.
Add the tomatoes, food colour (if using) and curry leaves and mix well. Cook until the tomatoes turn soft - about 3 mins.
Dunk the marinated chicken pieces into this mixture and increase the flame to medium-high. Cook stirring frequently until the chicken pieces begin to roast. You dont have to add any water, the meat will let out water as it cooks. Adjust salt and keep roasting until the chicken is cooked soft. This will take about 20-25 mins. If you feel the chicken is not cooking well, cook closed to speed up the process. The curry will be watery in this case so once the chicken is cooked, cook on an open flame until your desired consistency is reached.
When the chicken has roasted and most of the water has been cooked off, add the chicken masala and mix well. Cook for another minute and remove from fire.'
,'30 mins',5,1,'lunch');
insert into comments (recipie_id,user_id,comment) values (1,1,'good recipie');

select * from comments;
select r_id,r_name,ingredients,instructions,cook_time,serve_size,category  from recipies;
select * from users;
drop table users;
drop database onlinerecipe;