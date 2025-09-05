/* Embeddable Emergent badge v1 */
(function () {
  try {
    // Do not double insert
    if (document.getElementById("emergent-badge")) return;

    // Read config from the script tag
    /** @type {HTMLScriptElement|null} */
    var script =
      document.currentScript ||
      document.querySelector('script[data-emergent-badge="1"]');

    var ds = (script && script.dataset) || {};

    var href =
      ds.href ||
      "https://app.emergent.sh/?utm_source=emergent-badge";
    var text = ds.text || "Made with Emergent";
    var img =
      ds.img ||
      "https://avatars.githubusercontent.com/in/1201222?s=64";
    var position = (ds.position || "bottom-right").toLowerCase();
    var offset = parseInt(ds.offset || "20", 10) || 20;
    var theme = (ds.theme || "auto").toLowerCase(); // "light" | "dark" | "auto"
    var z = parseInt(ds.zIndex || "9999", 10) || 9999;

    // Theme colors
    var prefersDark =
      theme === "auto"
        ? window.matchMedia &&
          window.matchMedia("(prefers-color-scheme: dark)").matches
        : theme === "dark";
    var bg = prefersDark ? "#0b1020" : "#ffffff";
    var fg = prefersDark ? "#e5e7eb" : "#000000";
    var border = prefersDark ? "rgba(255,255,255,0.18)" : "rgba(0,0,0,0.12)";
    var shadow = "0 2px 8px rgba(0,0,0,0.15)";

    // Create anchor
    var a = document.createElement("a");
    a.id = "emergent-badge";
    a.href = href;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    a.setAttribute("aria-label", text);
    a.style.cssText = [
      "display:flex",
      "align-items:center",
      "position:fixed",
      "text-decoration:none",
      "padding:6px 10px",
      "font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,Cantarell,'Open Sans','Helvetica Neue',sans-serif",
      "font-size:12px",
      "border-radius:8px",
      "background-color:" + bg,
      "color:" + fg,
      "border:1px solid " + border,
      "box-shadow:" + shadow,
      "z-index:" + z,
      "gap:8px",
      "line-height:1",
      "user-select:none",
      "cursor:pointer",
    ].join(";");

    // Positioning
    var pos = { top: "", right: "", bottom: "", left: "" };
    if (position.includes("bottom")) pos.bottom = offset + "px";
    if (position.includes("top")) pos.top = offset + "px";
    if (position.includes("right")) pos.right = offset + "px";
    if (position.includes("left")) pos.left = offset + "px";
    // default
    if (!pos.top && !pos.bottom) pos.bottom = offset + "px";
    if (!pos.left && !pos.right) pos.right = offset + "px";
    Object.assign(a.style, pos);

    // Image
    var logo = document.createElement("img");
    logo.src = img;
    logo.alt = "";
    logo.decoding = "async";
    logo.referrerPolicy = "no-referrer";
    logo.style.cssText = "width:20px;height:20px;display:block;border-radius:4px";
    a.appendChild(logo);

    // Text
    var p = document.createElement("span");
    p.textContent = text;
    p.style.cssText = "margin:0;padding:0;color:" + fg;
    a.appendChild(p);

    // Insert
    document.addEventListener("DOMContentLoaded", function () {
      document.body.appendChild(a);
    });
    if (document.readyState === "interactive" || document.readyState === "complete") {
      document.body.appendChild(a);
    }
  } catch (e) {
    // Fail silent by design
  }
})();
