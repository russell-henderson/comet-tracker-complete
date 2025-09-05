import React from "react";

const pad2 = (n) => String(n).padStart(2, "0");

function useCountdown(targetISO) {
  const [now, setNow] = React.useState(() => Date.now());
  React.useEffect(() => {
    const id = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(id);
  }, []);
  const t = new Date(targetISO);
  if (Number.isNaN(t.getTime())) return { valid: false };
  let diff = Math.floor((t.getTime() - now) / 1000);
  const sign = diff < 0 ? -1 : 1;
  diff = Math.abs(diff);
  return {
    valid: true,
    sign,
    days: Math.floor(diff / 86400),
    hours: Math.floor((diff % 86400) / 3600),
    minutes: Math.floor((diff % 3600) / 60),
    seconds: diff % 60,
  };
}

export default function CountdownPill({ targetISO, label = "Closest approach" }) {
  const c = useCountdown(targetISO);

  if (!c.valid) {
    return (
      <span
        title="Set REACT_APP_CLOSEST_APPROACH in frontend/.env (UTC ISO)"
        className="inline-flex items-center gap-2 rounded-md border border-yellow-500/30 bg-yellow-500/10 px-3 py-1 text-xs text-yellow-200"
      >
        <span className="h-2 w-2 rounded-full bg-yellow-400" />
        Date not set
      </span>
    );
  }

  if (c.sign < 0) {
    return (
      <span
        title={new Date(targetISO).toUTCString()}
        className="inline-flex items-center gap-2 rounded-md border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-xs text-emerald-200"
      >
        <span className="h-2 w-2 rounded-full bg-emerald-400" />
        {label} reached
      </span>
    );
  }

  return (
    <span
      title={new Date(targetISO).toUTCString()}
      className="inline-flex items-center gap-2 rounded-md border border-sky-500/30 bg-sky-500/10 px-3 py-1 text-xs text-sky-200"
      aria-live="polite"
    >
      <span className="h-2 w-2 rounded-full bg-sky-400" />
      {label}: {c.days}d {pad2(c.hours)}:{pad2(c.minutes)}:{pad2(c.seconds)}
    </span>
  );
}
