import client from "prom-client";

export const register = new client.Registry();

enum metric_label {
  PATH = "path",
  METHOD = "method",
  STATUS_CODE = "status_code",
}

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

export const http_request_total = new client.Counter({
  name: "express_http_request_total",
  help: "The total number of HTTP requests received",
  labelNames: [
    metric_label.PATH,
    metric_label.METHOD,
    metric_label.STATUS_CODE,
  ],
});

register.registerMetric(http_request_total);

client.collectDefaultMetrics({
  register,
  prefix: "express_",
});
