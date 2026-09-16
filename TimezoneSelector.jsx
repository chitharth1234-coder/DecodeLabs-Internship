import { useState } from "react";
import { ChevronDown, Globe } from "lucide-react";

const TIMEZONES = [
  { label: "UTC -8:00", value: -8 },
  { label: "UTC -5:00", value: -5 },
  { label: "UTC 0:00", value: 0 },
  { label: "UTC +1:00", value: 1 },
  { label: "UTC +5:30", value: 5.5 },
  { label: "UTC +8:00", value: 8 },
  { label: "UTC +9:00", value: 9 },
];

export default function TimezoneSelector({ defaultValue = "UTC 0:00" }) {
  const [selected, setSelected] = useState(defaultValue);

  return (
    <div className="max-w-sm space-y-2">
      <label
        htmlFor="timezone"
        className="block text-sm font-semibold text-slate-700"
      >
        What is your timezone?
      </label>

      <div className="relative">
        <select
          id="timezone"
          value={selected}
          onChange={(e) => setSelected(e.target.value)}
          className="w-full appearance-none rounded-xl border border-slate-200 bg-white px-4 py-3 pr-10 text-sm text-slate-800 shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-300"
        >
          {TIMEZONES.map((tz) => (
            <option key={tz.label} value={tz.label}>
              {tz.label}
            </option>
          ))}
        </select>
        <ChevronDown
          size={18}
          className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-slate-400"
        />
      </div>

      <div className="inline-flex items-center gap-2 rounded-lg border border-slate-200 px-3 py-1.5 text-sm text-slate-700">
        <Globe size={16} className="text-slate-500" />
        <span>{selected}</span>
      </div>
    </div>
  );
}