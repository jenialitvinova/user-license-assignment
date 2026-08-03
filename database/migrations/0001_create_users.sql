-- Migration 0001: create users table

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_principal_name VARCHAR(255) NOT NULL UNIQUE,
    api_user_id VARCHAR(255),
    status VARCHAR(30) NOT NULL DEFAULT 'PENDING'
        CHECK (
            status IN (
                'PENDING',
                'ASSIGNED',
                'ALREADY_ASSIGNED',
                'DISABLED',
                'NOT_FOUND',
                'FAILED'
            )
        ),
    message TEXT,
    processed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
