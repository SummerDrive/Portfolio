import chromium from "@sparticuz/chromium";
import { chromium as playwright } from "playwright-core";

function extractValue(html) {
  const strongMatch = html.match(/<strong\s+class="red">(.*?)<\/strong>/);
  if (strongMatch) return strongMatch[1];

  const tdMatch = html.match(/<td\s+class="odds">(.*?)<\/td>/);
  if (tdMatch) return tdMatch[1];

  return "No Data";
}

async function getDev(nameCat, locator, page) {
  await page.getByRole("link", { name: nameCat }).click();
  const html = await page.locator(locator).first().innerHTML();
  return extractValue(html);
}

async function openWebsite(col2, col3, page) {
  const array = [];

  await page.getByRole("link", { name: col2 }).click();
  await page.getByRole("link", { name: col3 }).first().click();

  array.push(await getDev("単勝・複勝", ".basic.narrow-xy.tanpuku.pop", page));
  array.push(await getDev("連複", ".basic.narrow-xy.fuku3.pop", page));

  return array;
}

export const handler = async (event) => {

  console.log("EVENT:", JSON.stringify(event));

  // 🔥 CORSプリフライト対応
  if (event.requestContext?.http?.method === "OPTIONS") {
    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
      },
      body: ""
    };
  }
  
  // 🔥 安全パース
  const body = event?.body ? JSON.parse(event.body) : {};

  const col2 = body.col2 ?? "東京8日";
  const col3 = body.col3 ?? "1レース";

  // 🔥 Lambda用の正しい起動方法
  const browser = await playwright.launch({
    args: chromium.args,
    executablePath: await chromium.executablePath(),
    headless: chromium.headless,
  });

  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto("https://www.jra.go.jp/keiba/", {
    waitUntil: "domcontentloaded",
  });

  await page.getByRole("link", { name: "オッズ", exact: true }).click();
  await page.getByRole("link", { name: col2 }).click();
  await page.locator(".btn-def.btn-sm.btn-narrow.gray").first().click();
  await page.getByRole("link", { name: "人気順" }).click();

  const result = await openWebsite(col2, col3, page);

  await browser.close();

  return {
    statusCode: 200,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      message: result,
      data: result
    })
  };
};