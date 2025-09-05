// frontend/src/components/SkyLiveEmbedCard.jsx
import React from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

const NASA_EYES_SOLAR_URL = "https://eyes.nasa.gov/apps/solar-system/#/?embed=true";
const NASA_EYES_ASTEROIDS_URL = "https://eyes.nasa.gov/apps/asteroids/#/?embed=true";
const DEFAULT_TSL_URL =
  "https://theskylive.com/3dsolarsystem?objs=c2025k1|c2025a6|p2016j3|p2021a3|c2025n1&date=2025-09-14&h=02&m=28&";

export default function SkyLiveEmbedCard({
  title = "3D Solar System View",
  height = 360,           // used when fill is false
  fill = false,           // when true, card grows to fill parent
  initialMode = "solar",  // "solar" or "asteroids"
  tslUrl = DEFAULT_TSL_URL,
}) {
  const [mode, setMode] = React.useState(initialMode); // "solar" | "asteroids"
  const src = mode === "solar" ? NASA_EYES_SOLAR_URL : NASA_EYES_ASTEROIDS_URL;

  // height strategy
  const style = fill ? { minHeight: 320 } : { height };

  return (
    <Card
      className={`bg-slate-800/50 border-slate-700 flex flex-col overflow-hidden ${fill ? "flex-1" : ""}`}
      style={style}
    >
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold">{title}</CardTitle>
          <div className="flex items-center gap-2 text-xs">
            <span className="opacity-70">
              Source: NASA Eyes • {mode === "solar" ? "Solar System" : "Asteroids"}
            </span>
            <button
              type="button"
              onClick={() => setMode((m) => (m === "solar" ? "asteroids" : "solar"))}
              className="rounded-md px-2 py-1 border border-white/10 hover:bg-white/5"
              aria-label="Toggle NASA view"
              title={mode === "solar" ? "Switch to Asteroids" : "Switch to Solar System"}
            >
              Toggle
            </button>
            <a
              href={tslUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-md px-2 py-1 border border-white/10 hover:bg-white/5"
              title="Open TheSkyLive in a new tab"
            >
              Open TheSkyLive
            </a>
          </div>
        </div>
      </CardHeader>

      <CardContent className="pt-0 flex-1">
        <div className="relative w-full h-full overflow-hidden rounded-lg bg-black/40">
          <iframe
            key={src} // reload when switching modes
            src={src}
            title={mode === "solar" ? "NASA Eyes Solar System" : "NASA Eyes Asteroids"}
            className="absolute inset-0 w-full h-full border-0"
            allow="autoplay; fullscreen; xr-spatial-tracking; clipboard-write; encrypted-media"
            allowFullScreen
            loading="lazy"
            referrerPolicy="no-referrer-when-downgrade"
          />
        </div>
      </CardContent>
    </Card>
  );
}
