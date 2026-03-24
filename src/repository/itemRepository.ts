import { Pool } from "pg";
import { Item } from "../models/item";

interface ItemRepository {
  getItem(id: string): Promise<Item>;
  getItems(limit?: number): Promise<Item[]>;
  // updateItem(): Promise<Item>;
  createItem(name: string): Promise<Item[]>;
  // deleteItem(): Promise<void>;
}

export const getItemRepository = (pool: Pool): ItemRepository => {
  return {
    getItem: async (id: string) => {
      const query = `
                SELECT * FROM items
                WHERE id = $1
                ORDER BY timestamp DESC
                LIMIT $2;
            `;

      const values = [id, 1];

      const result = await pool.query<Item>(query, values);

      return result.rows.reverse()[0];
    },

    getItems: async (limit = 50) => {
      const query = `
                SELECT * FROM items
                ORDER BY timestamp DESC
                LIMIT $1;
            `;

      const values = [limit];

      const result = await pool.query<Item>(query, values);

      return result.rows.reverse();
    },

    createItem: async (name: string) => {
      const query = `
            INSERT INTO items (name)
            VALUES ($1)
            RETURNING *;
        `;
      const values = [name];

      const result = await pool.query<Item>(query, values);

      return result.rows.reverse();
    },
  };
};
