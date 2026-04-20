import client, { Counter, Histogram } from "prom-client";

export const register = new client.Registry();

enum metric_label {
  PATH = "path",
  METHOD = "method",
  STATUS_CODE = "status_code",
}

const httpMetricsLabelNames = [
  metric_label.PATH,
  metric_label.METHOD,
  metric_label.STATUS_CODE,
];

export class MetricLabel {
  method: string;
  path: string;
  status_code: number;

  constructor(method: string, pathname: string, statusCode: number) {
    this.method = method;
    this.path = pathname;
    this.status_code = statusCode;
  }
}

export const httpRequestCount = new Counter({
  name: "express_http_request_total",
  help: "The total number of HTTP requests received",
  labelNames: httpMetricsLabelNames,
  registers: [register],
});

export const httpRequestDuration = new Histogram({
  name: "express_http_request_duration",
  help: "the last duration or response time of last request",
  labelNames: httpMetricsLabelNames,
  buckets: [0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
  registers: [register],
});

client.collectDefaultMetrics({
  register,
  prefix: "express_",
});
