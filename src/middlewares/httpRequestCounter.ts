import { NextFunction, Request, Response } from "express";
import {
  httpRequestCount,
  httpRequestDuration,
  MetricLabel,
} from "../config/metrics";

export const httpRequestCounter = (
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  const startTime = process.hrtime.bigint();

  const req_url = new URL(req.url, `http://${req.headers.host}`);

  const original_res_send_function = res.json;

  const res_send_interceptor = function (body: any) {
    // Record the request duration
    const durationNs = process.hrtime.bigint() - startTime;
    const durationSec = Number(durationNs) / 1e9;
    httpRequestDuration
      .labels(new MetricLabel(req.method, req_url.pathname, res.statusCode))
      .observe(durationSec);
    // Increment the http_request_total metric
    httpRequestCount.inc(
      new MetricLabel(req.method, req_url.pathname, res.statusCode),
    );
    // @ts-ignore
    original_res_send_function.call(this, body);
  };

  res.json = res_send_interceptor as any;
  next();
};
