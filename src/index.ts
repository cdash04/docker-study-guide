// Example based on https://blog.logrocket.com/express-typescript-node/

import express from "express";
import itemRoutes from "./routes/itemRoutes";
import healthRoutes from "./routes/healthRoutes";
import metricsRoutes from "./routes/metricsRoutes";
import { errorHandler } from "./middlewares/errorHandler";
import { requestLogger } from "./middlewares/requestLogger";
import config from "./config/config";
import { logger } from "./config/logger";
import { httpRequestCounter } from "./middlewares/httpRequestCounter";

const app = express();

app.use(express.json());
app.use(requestLogger);
app.use(httpRequestCounter);

// Routes
app.use("/metrics", metricsRoutes);
app.use("/health", healthRoutes);
app.use("/api/items", itemRoutes);

app.use(errorHandler);

app.listen(config.port, () => {
  logger.info({ message: `Server running on port ${config.port}` });
});
