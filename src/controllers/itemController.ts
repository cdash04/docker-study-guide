import { Request, Response, NextFunction } from "express";
import { Pool } from "pg";
import config from "../config/config";
import { getItemRepository } from "../repository/itemRepository";

const pool = new Pool({
  user: config.dbUser,
  host: config.dbHost,
  database: config.dbDatabase,
  password: config.dbPassword,
  port: config.dbPort,
  statement_timeout: 10000,
});

const itemRepository = getItemRepository(pool);

// Create an item
export const createItem = async (
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  try {
    const { name } = req.body;
    const newItem = await itemRepository.createItem(name);
    res.status(201).json(newItem);
  } catch (error) {
    next(error);
  }
};

// Get all items
export const getItems = async (
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  try {
    const items = await itemRepository.getItems();
    res.json(items);
  } catch (error) {
    next(error);
  }
};

// Get single item
export const getItemById = async (
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  try {
    const id = parseInt(req.params.id as string, 10);
    const item = await itemRepository.getItem(id);
    if (!item) {
      res.status(404).json({ message: "Item not found" });
      return;
    }
    res.json(item);
  } catch (error) {
    next(error);
  }
};

// Update an item
export const updateItem = async (
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  try {
    const id = parseInt(req.params.id as string, 10);
    const { name } = req.body;
    const updatedItem = await itemRepository.updateItem(id, name);

    if (!updatedItem) {
      res.status(404).json({ message: "Item not found" });
      return;
    }
    res.json(updatedItem);
  } catch (error) {
    next(error);
  }
};

// Delete an item
export const deleteItem = async (
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  try {
    const id = parseInt(req.params.id as string, 10);
    const deletedItem = await itemRepository.deleteItem(id);

    if (!deletedItem) {
      res.status(404).json({ message: "Item not found" });
      return;
    }

    res.json(deletedItem);
  } catch (error) {
    next(error);
  }
};
