import { Request, Response, NextFunction } from "express";
import { logger } from "../config/logger";

export const requestLogger = (
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  logger.info({
    message: `${req.method} ${req.url}`,
    labels: { method: req.method },
  });
  next();
};
