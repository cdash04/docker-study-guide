import { NextFunction, Router, Request, Response } from "express";
import { register } from "../config/metrics";

const router = Router();

router.get("/", async (req: Request, res: Response, next: NextFunction) => {
  res.setHeader("Content-type", register.contentType);
  res.send(await register.metrics());
});

export default router;
