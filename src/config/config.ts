import dotenv from "dotenv";

dotenv.config();

interface Config {
  port: number;
  nodeEnv: string;
  dbUser: string;
  dbHost: string;
  dbDatabase: string;
  dbPassword: string;
  dbPort: number;
  lokiHost: string;
  lokiPort: number;
}

const config: Config = {
  port: Number(process.env.PORT) || 3000,
  nodeEnv: process.env.NODE_ENV || "development",
  dbUser: process.env.DB_USER || "postgres",
  dbHost: process.env.DB_HOST || "postgres",
  dbDatabase: process.env.DB_NAME || "items",
  dbPassword: process.env.DB_PASSWORD || "password123",
  dbPort: Number(process.env.DB_PORT) || 5432,
  lokiHost: process.env.LOKI_HOST || "loki",
  lokiPort: Number(process.env.LOKI_PORT) || 3100,
};

export default config;
