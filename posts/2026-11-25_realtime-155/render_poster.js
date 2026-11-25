// 载恩视觉系统 · 静态图渲染 / 度量
// 用法:
//   node render_poster.js --html=poster.html --out=poster.png --w=1080 --h=1920 --scale=2
//   node render_poster.js --html=poster.html --measure          # 只量尺寸与溢出，不截图
// 依赖: puppeteer-core（或已安装 puppeteer）+ 本机 Chrome
const fs = require("fs");
const path = require("path");

const CHROME =
  process.env.ZIEN_CHROME || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

function loadPuppeteer() {
  const extra = process.env.ZIEN_NODE_MODULES;
  const loaders = [() => require("puppeteer-core"), () => require("puppeteer")];
  if (extra) {
    loaders.unshift(
      () => require(path.join(extra, "puppeteer-core")),
      () => require(path.join(extra, "puppeteer"))
    );
  }
  for (const load of loaders) {
    try {
      return load();
    } catch (e) {
      /* 继续尝试下一个位置 */
    }
  }
  throw new Error(
    "找不到 puppeteer-core：请在工作目录 npm i puppeteer-core，或用 ZIEN_NODE_MODULES 指向已安装的 node_modules"
  );
}
const puppeteer = loadPuppeteer();

const argv = process.argv.slice(2);
const getArg = (k, d) => {
  const hit = argv.find((a) => a.startsWith(`--${k}=`));
  return hit ? hit.split("=").slice(1).join("=") : d;
};

const cwd = process.cwd();
const htmlPath = path.resolve(cwd, getArg("html", "poster.html"));
const outPath = path.resolve(cwd, getArg("out", "poster.png"));
const W = Number(getArg("w", "1080"));
const H = Number(getArg("h", "1920"));
const scale = Number(getArg("scale", "2"));
const measure = argv.includes("--measure");

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: "new",
    args: ["--hide-scrollbars", "--disable-gpu", "--no-first-run", "--no-sandbox", "--font-render-hinting=none"],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: W, height: H, deviceScaleFactor: scale });
  await page.goto("file:///" + htmlPath.replace(/\\/g, "/"), { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  await new Promise((r) => setTimeout(r, 700));

  const metrics = await page.evaluate(() => {
    const out = { doc: {}, overflow: [], blocks: [] };
    const poster = document.querySelector(".poster") || document.body;
    const pb = poster.getBoundingClientRect();
    out.doc = { scrollH: document.documentElement.scrollHeight, bodyH: poster.getBoundingClientRect().height };

    out.blocks = [...document.querySelectorAll("[data-block]")].map((el) => {
      const prev = el.getAttribute("style") || "";
      el.style.cssText = "flex:0 0 auto;height:auto;min-height:0;";
      const natural = +el.getBoundingClientRect().height.toFixed(1);
      el.style.cssText = prev;
      const r = el.getBoundingClientRect();
      return {
        cls: (el.className || el.tagName).toString().slice(0, 40),
        top: +r.top.toFixed(1),
        h: +r.height.toFixed(1),
        natural,
        // natural - h > 2 说明这一块被 flex 压缩了（内部内容会被裁切）
        compressed: +(natural - r.height).toFixed(1) > 2,
        overflowY: +(el.scrollHeight - r.height).toFixed(1),
      };
    });
    // 钩子审计：标了 [data-hook] 的大字块必须 ≤2 行、≤16 字（见 references/typography.md）
    out.hooks = [...document.querySelectorAll("[data-hook]")].map((el) => {
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      let lh = parseFloat(cs.lineHeight);
      if (!isFinite(lh) || lh <= 0) lh = parseFloat(cs.fontSize) * 1.2;
      const lines = Math.max(1, Math.round(r.height / lh));
      const chars = (el.textContent || "").replace(/\s+/g, "").length;
      return {
        cls: (el.className || el.tagName).toString().slice(0, 40),
        lines,
        chars,
        fontSize: cs.fontSize,
        tooManyLines: lines > 2,
        tooLong: chars > 16,
      };
    });

    out.summary = {
      compressedBlocks: out.blocks.filter((b) => b.compressed).map((b) => b.cls),
      // 必须为空：钩子折成三行、或超过 16 字，都会在这里报出来
      hookIssues: out.hooks
        .filter((h) => h.tooManyLines || h.tooLong)
        .map((h) => `${h.cls}(${h.lines}行/${h.chars}字)`),
      posterHeight: +pb.height.toFixed(1),
      contentHeight: +(
        [...document.querySelectorAll(".poster > *")].reduce((sum, el) => {
          const r = el.getBoundingClientRect();
          const cs = getComputedStyle(el);
          return sum + r.height + parseFloat(cs.marginTop || 0) + parseFloat(cs.marginBottom || 0);
        }, 0)
      ).toFixed(1),
    };

    [...poster.querySelectorAll("*")].forEach((el) => {
      if (el.closest("[data-no-audit]")) return;
      const r = el.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) return;
      const over = {
        right: +(r.right - pb.right).toFixed(1),
        bottom: +(r.bottom - pb.bottom).toFixed(1),
        left: +(pb.left - r.left).toFixed(1),
      };
      if (Math.max(over.right, over.bottom, over.left) > 1) {
        out.overflow.push({
          cls: (el.className || el.tagName).toString().slice(0, 44),
          text: (el.textContent || "").trim().slice(0, 22),
          ...over,
        });
      }
    });
    out.overflow.sort((a, b) => b.bottom - a.bottom);
    out.overflow = out.overflow.slice(0, 24);
    return out;
  });

  console.log(JSON.stringify(metrics, null, 2));
  if (!measure) {
    await page.screenshot({ path: outPath, clip: { x: 0, y: 0, width: W, height: H } });
    console.log("saved:", outPath, `${W * scale}x${H * scale}`, fs.statSync(outPath).size, "bytes");
  }
  await browser.close();
})().catch((e) => {
  console.error("FAILED:", e.message);
  process.exit(1);
});
