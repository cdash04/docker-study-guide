import { Request, Response, NextFunction } from "express";
import { logger } from "../config/logger";

export interface AppError extends Error {
  status?: number;
}

export const errorHandler = (
  err: AppError,
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  logger.error({
    message: `${req.method} ${err.message || "Internal Server Error"}`,
  });
  res.status(err.status || 500).json({
    message: err.message || "Internal Server Error",
  });
};
