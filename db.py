import asyncpg
import os
from decouple import config

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=config("DB_USER"),
            password=config("DB_PASS"),
            host=config("DB_HOST"),
            port=config("DB_PORT"),
            database=config("DB_NAME")
        )

    async def create_tables(self):
        query = """
        CREATE TABLE IF NOT EXISTS wiki_pages (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            title TEXT UNIQUE,
            content TEXT
        );
        """
        async with self.pool.acquire() as connection:
            await connection.execute(query)

    async def add_page(self, title: str, content: str):
        query = """
        INSERT INTO wiki_pages (title, content)
        VALUES ($1, $2)
        ON CONFLICT (title)
        DO UPDATE SET content = EXCLUDED.content
        RETURNING id;
        """

        return await self.pool.fetchval(query, title, content)

    async def get_all_pages(self, limit: int = 100) -> list[dict[str, any]]:
        query = "SELECT * FROM wiki_pages ORDER BY title ASC LIMIT $1"
        return [dict(row) for row in await self.pool.fetch(query, limit)]

    async def get_page_by_id(self, page_id: int) -> dict[str, any]:
        query = "SELECT title, content FROM wiki_pages WHERE id = $1"
        return dict(await self.pool.fetchrow(query, int(page_id)))

    async def delete_page(self, page_id: int):
        query = "DELETE FROM wiki_pages WHERE id = $1"
        result_tag = await self.pool.execute(query, int(page_id))

    async def close(self):
        if self.pool:
            await self.pool.close()
