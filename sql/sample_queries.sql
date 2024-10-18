-- Write SQL queries to answer these questions using the data you have loaded into BigQuery:
-- 1. Find the top 5 users with the highest number of posts.

select * from (select distinct username,count(u.user_id) over(partition by username) top_posts_count from kk_users u join posts p on u.id = p.user_id where status = 'lengthy') order by top_posts_count desc limit 5;
-- 2. For each of these top 5 users, calculate the average post length.

select * from (select distinct username,avg(length(body)) over(partition by username) avg_post_length,count(u.user_id) over(partition by username) top_posts_count from kk_users u join kk_posts p on u.id = p.user_id where status = 'lengthy') order by top_posts_count desc limit 5;
-- 3. Identify the day of the week when the most `lengthy` posts are created (assume all posts were created in the UTC timezone).

with most_posts_count as (select DayOfWeek,count(status) most_lengthy_posts from (
    select *,extract(week from created_at) _week,extract(day from created_at) AS DayOfWeek from kk_posts where status = 'lengthy') group by DayOfWeek order by most_lengthy_posts desc)

select dayofweek from most_posts_count where most_lengthy_posts in (select max(most_lengthy_posts) from most_posts_count )
