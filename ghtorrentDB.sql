-- CREATE DATABASE GHTorrentDump;
USE GHTorrentDump;
-- SET sql_mode=(SELECT REPLACE(@@sql_mode, 'ONLY_FULL_GROUP_BY', '')); -- Enable GROUP BY used in later queries

-- // SETUP QUERIES
-- // THIS GIVES SIZE OF YOUR CURRENT DATABASE
-- SELECT table_schema "GHTorrentDump", sum( data_length + index_length ) / 1024 / 1024 "Data Base Size in MiB" 
-- FROM information_schema.TABLES GROUP BY table_schema;  

-- // THIS GIVES NUMBER OF ROWS IN WHATS SPECIFIED
-- SELECT SUM(TABLE_ROWS)
--    FROM INFORMATION_SCHEMA.TABLES
--    WHERE TABLE_SCHEMA = 'GHTorrentDump'


-- // ACTUAL QUERIES / PROGRESS //

-- // QUERIES # OF USERS PER PROJECT ID //
-- SELECT pj.repo_id, COUNT(pj.user_id) as UserCount
-- FROM project_members pj 
-- 	LEFT JOIN users u ON pj.user_id = u.id 
-- GROUP BY pj.repo_id;

-- // QUERIES URL, REPO ID (IN THIS DB), AND # OF USERS PER PROJECT ID //
-- SELECT p.url, p.id, COUNT(pj.user_id) AS UserCount
-- FROM project_members pj 
-- 	LEFT JOIN users u ON pj.user_id = u.id 
--     LEFT JOIN projects p ON pj.repo_id = p.id
-- GROUP BY pj.repo_id;

-- // QUERIES THE ABOVE QUERY BUT ONLY PROJECTS WITH > 5 USERS // 
-- SELECT p.id, p.url, psub.UserCount
-- FROM (
-- 	SELECT pj.repo_id, COUNT(pj.user_id) as UserCount
-- 	FROM project_members pj 
-- 		LEFT JOIN users u ON pj.user_id = u.id 
-- 	GROUP BY pj.repo_id
--     ) AS psub, projects p
-- WHERE 
-- 	psub.repo_id = p.id AND
--     psub.UserCount >= 5
-- ;

-- // QUERIES REPO ID (IN THIS DB) AND # OF COMMITS PER PROJECT ID //
SELECT pc.project_id, COUNT(pc.commit_id) AS CommitCount
FROM project_commits pc 
	LEFT JOIN commits c ON pc.commit_id = c.id 
GROUP BY pc.project_id;

-- // QUERIES THE ABOVE QUERY BUT ONLY PROJECTS WITH > 25 COMMITS // ALSO DOESN'T WORK, TOO MANY TABLES TO COUNT. NEED ALTERNATIVE
-- SELECT p.id, p.url, pcom.CommitCount
-- FROM (
--     SELECT pc.project_id, COUNT(pc.commit_id) AS CommitCount
-- 	FROM project_commits pc 
-- 		LEFT JOIN commits c ON pc.commit_id = c.id 
-- 	GROUP BY pc.project_id
--     ) AS pcom,
--     projects p
-- WHERE 
--     pcom.project_id = p.id AND
--     pcom.CommitCount >= 25
-- ; 

-- // QUERIES THE ABOVE QUERIES BUT ONLY PROJECTS WITH > 5 USERS AND > 25 COMMITS // -- SHOULD WORK, CAN'T CONFIRM. DBMS DISCONNECTS
-- SELECT p.id, p.url, pmem.UserCount, pcom.CommitCount
-- FROM (
-- 	SELECT pj.repo_id, COUNT(pj.user_id) as UserCount
-- 	FROM project_members pj 
-- 		LEFT JOIN users u ON pj.user_id = u.id 
-- 	GROUP BY pj.repo_id
--     ) AS pmem, 
--     (
--     SELECT pc.project_id, COUNT(pc.commit_id) AS CommitCount
-- 	FROM project_commits pc 
-- 		LEFT JOIN commits c ON pc.commit_id = c.id 
-- 	GROUP BY pc.project_id
--     ) AS pcom,
--     projects p
-- WHERE 
-- 	pmem.repo_id = p.id AND
--     pcom.project_id = p.id AND
--     pmem.UserCount >= 5 AND
--     pcom.CommitCount >= 25
-- ; 







-- // GET INFO IF YOU HAVE A PROJECT ID - i pretty much only used these for sanity checking // 
-- SELECT * -- Basic info about project p //
-- FROM projects p
-- WHERE p.id = 1;

-- SELECT * -- Check which users belong to a given project ID, can use to ensure user count matches repo id // 
-- FROM project_members pm, users u
-- WHERE pm.repo_id = 1 AND pm.user_id = u.id;