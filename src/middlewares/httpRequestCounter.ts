import { NextFunction, Request, Response } from "express";
import { http_request_total, MetricLabel } from "../config/metrics";

export const httpRequestCounter = (
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  const req_url = new URL(req.url, `http://${req.headers.host}`);

  const original_res_send_function = res.json;

  const res_send_interceptor = function (body: any) {
    // Increment the http_request_total metric
    http_request_total.inc(
      new MetricLabel(req.method, req_url.pathname, res.statusCode),
    );
    // @ts-ignore
    original_res_send_function.call(this, body);
  };

  res.json = res_send_interceptor as any;
  next();
};
