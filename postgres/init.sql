-- Create a table for storing scraped data
CREATE TABLE IF NOT EXISTS estate_items (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    image_url TEXT
);
