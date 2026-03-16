-- ADMIN USER
INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password_hash,
    is_admin,
    created_at,
    updated_at
) VALUES (
    '00000000-0000-0000-0000-000000000001',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$KbQi1C7nYzWx/ju0RduCMOJHb5H9P2ymlk/wEYBLETymFcpnSUsFy',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- AMENITIES
INSERT INTO amenities (id, name, created_at, updated_at) VALUES
('a1', 'WiFi', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('a2', 'Swimming Pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('a3', 'Air Conditioning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('a4', 'Parking', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('a5', 'Gym', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);