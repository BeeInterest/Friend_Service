CREATE TABLE IF NOT EXISTS users (
    id uuid primary key not null,
    username varchar(500) not null
);
CREATE TABLE IF NOT EXISTS relations (
    id serial primary key not null,
    user1 varchar(500) not null,
    user2 varchar(500) not null,
    status varchar(50) not null
);
DELETE FROM users;
DELETE FROM relations;
INSERT INTO users(id, username)
VALUES
('aec266a9-923b-4ad3-b336-ddb3537ce282','ylbek134'),
('0c2efc0c-a25c-4ef9-9a77-90d4a76e3971','maluk890'),
('fbb965af-45be-4d53-89d9-1550a4b5462a','gagar189'),
('476ddf8f-9ee7-4246-a638-aa948bf6fe16','lidar908'),
('36d4b22b-ac06-4442-9ac3-47915b84453b','gogerai7'),
('b2d38b2c-1e07-4954-8775-d1f5ccca16a6','serduch901'),
('42355fe7-050e-46db-91b4-c24d79de9482','nepo457'),
('6c5ad673-8cc2-4ada-8ee5-d1828ff2fbf0','ago0876'),
('92ca5638-446d-42d9-8f2b-757423b733bb','run1346'),
('f0d3141f-eb15-46e5-898e-d4d0670d133f','gorelo7654'),
('3b191e60-ab8f-4ad7-b298-27649a9235b5','noshe2893'),
('5bf2ca09-66d4-4825-ac9d-3a56158ffbd1','sheko34223'),
('fbacf402-b512-4ab9-ab3a-1ac04dce5b6c','dira0743234');
INSERT INTO relations(user1, user2, status)
VALUES
('ylbek134','maluk890','outgoing request'),
('maluk890','ylbek134','incoming request');
