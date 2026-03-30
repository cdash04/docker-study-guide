import { Pool } from "pg";
import { Item } from "../models/item";

interface ItemRepository {
  getItem(id: number): Promise<Item | undefined>;
  getItems(limit?: number): Promise<Item[]>;
  updateItem(id: number, name: string): Promise<Item | undefined>;
  createItem(name: string): Promise<Item[]>;
  deleteItem(id: number): Promise<Item | undefined>;
}

export const getItemRepository = (pool: Pool): ItemRepository => {
  return {
    getItem: async (id: number) => {
      const query = `
                SELECT * FROM items
                WHERE id = $1
                ORDER BY timestamp DESC
                LIMIT $2;
            `;

      const values = [id, 1];

      const { rows } = await pool.query<Item>(query, values);

      if (rows.length != 1) {
        return undefined;
      }

      return rows[0];
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

    updateItem: async (id: number, name: string) => {
      const query = `
        UPDATE items
        SET name = $2
        WHERE id = $1
        RETURNING id, name;
      `;

      const values = [id, name];

      const { rows } = await pool.query<Item>(query, values);

      if (rows.length != 1) {
        return undefined;
      }

      return rows[0];
    },

    deleteItem: async (id: number) => {
      const query = `
        DELETE FROM items
        WHERE id = $1
        RETURNING id, name;
      `;

      const values = [id];

      const { rows } = await pool.query<Item>(query, values);

      if (rows.length != 1) {
        return undefined;
      }

      return rows[0];
    },
  };
};
