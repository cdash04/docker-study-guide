import { createLogger, LoggerOptions, transports, format } from "winston";
import LokiTransport from "winston-loki";
import config from "./config";

const { combine, timestamp, printf } = format;

const logFormat = printf(
  ({ level, message, timestamp }) =>
    `${timestamp} [${level.toUpperCase()}]: ${message}`,
);

const options: LoggerOptions = {
  format: combine(timestamp({ format: "YYYY-MM-DD HH:mm:ss" }), logFormat),
  transports: [
    new transports.Console({ level: "warn" }),
    new LokiTransport({
      level: config.nodeEnv === "development" ? "debug" : "http",
      labels: { appName: "Express" },
      host: `http://${config.lokiHost}:${config.lokiPort}`,
    }),
  ],
};

export const logger = createLogger(options);
