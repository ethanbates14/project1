# Project 1

1) SQL Directory
-- create_tables.sql - adminer postgres dump
-- import.py
utilizes psycopg2 and env.sh file to gather connection parameters.  The logic assumes the base tables have already been created.
creates a staging table, loads data (formats zip code), and then disperses into normalized tables
cur.copy_from -- was much faster than single loop

2) Static content
-- image for the landing page

3) Templates
-- layout - base HTML with CSS - some session logic to manipulate the nav based on user login
-- index - main landing page for login or register - greets user if logged in
-- error/success - routing pages for posts
-- login - user login page - logic skipping if user logged in
-- register - user registration page - logic skipping if user logged in
-- search - CAN search by ZIP or BY Name - does some fuzzy like search logic in Query where clause
-- results - results from search Post - tells you search param type and value, can post you to location page
-- location - will tell you location standard data, weather and checkins

4) Application
-- user info stored in session variable -- cleared when logout rout
-- registration page checks if user exists - errors if does
-- login page does password and username authentication against DB (TO DO: password hashing)
-- search page does some formatting to param values for display and search in DB
-- checkin pages checks to see if current logged user already logged into area - error route if has, success route if hasnt
-- cannot check in if not logged in
-- API Layer (/api/zipcode) -- uses jsonify
