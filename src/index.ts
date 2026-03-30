// Example based on https://blog.logrocket.com/express-typescript-node/

import express from "express";
import itemRoutes from "./routes/itemRoutes";
import healthRoutes from "./routes/healthRoutes";
import { errorHandler } from "./middlewares/errorHandler";
import { requestLogger } from "./middlewares/requestLogger";
import config from "./config/config";
import { logger } from "./config/logger";

const app = express();

app.use(express.json());
app.use(requestLogger);

// Routes
app.use("/health", healthRoutes);
app.use("/api/items", itemRoutes);

app.use(errorHandler);

app.listen(config.port, () => {
  logger.info({ message: `Server running on port ${config.port}` });
});
