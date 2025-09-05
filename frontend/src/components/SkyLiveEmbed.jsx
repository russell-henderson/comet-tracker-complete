// src/components/SkyLiveEmbed.jsx
import React from "react";

const SkyLiveEmbed = ({
  date = "2025-09-14",
  hour = "02",
  minute = "28",
  objects = "c2025k1|c2025a6|p2016j3|p2021a3|c2025n1",
  aspect = 56.25, // 16:9
}) => {
  const url = `https://theskylive.com/3dsolarsystem?objs=${objects}&date=${date}&h=${hour}&m=${minute}&`;
  return (
    <div style={{ position: "relative", paddingTop: `${aspect}%`, background: "#0b1020", borderRadius: 12, overflow: "hidden" }}>
      <iframe
        src={url}
        title="TheSkyLive 3D Solar System"
        style={{ position: "absolute", inset: 0, width: "100%", height: "100%", border: 0 }}
        allowFullScreen
        loading="lazy"
        referrerPolicy="no-referrer-when-downgrade"
      />
    </div>
  );
};

export default SkyLiveEmbed;
