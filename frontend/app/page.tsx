"use client";
import { useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type Result = {
  valid: boolean; possible: boolean; country_code: number; region: string | null;
  location: string | null; country: string | null; carrier: string | null; line_type: string;
  timezones: string[]; formats: { e164: string; international: string; national: string };
  coordinates: { lat: number; lng: number } | null;
};

export default function Home() {
  const [number, setNumber] = useState("");
  const [region, setRegion] = useState("");
  const [data, setData] = useState<Result | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function lookup(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true); setError(""); setData(null);
    try {
      const qs = new URLSearchParams({ number: number.trim(), ...(region && { region }) });
      const res = await fetch(`${API}/api/lookup?${qs}`);
      const body = await res.json();
      if (!res.ok) throw new Error(typeof body.detail === "string" ? body.detail : "Check the number and try again.");
      setData(body);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not reach the API.");
    } finally {
      setLoading(false);
    }
  }

  const c = data?.coordinates;
  const rows: [string, string | null][] = data ? [
    ["Status", data.valid ? "Valid number" : data.possible ? "Possible, but not valid" : "Not valid"],
    ["Location", [data.location, data.country].filter((v, i, a) => v && a.indexOf(v) === i).join(", ") || null],
    ["Carrier", data.carrier], ["Line type", data.line_type],
    ["International", data.formats.international], ["National", data.formats.national],
    ["E.164", data.formats.e164], ["Time zones", data.timezones.join(", ") || null],
  ] : [];

  return (
    <main className="mx-auto max-w-5xl px-5 py-14 sm:py-24">
      <h1 className="max-w-3xl text-4xl font-semibold leading-[1.05] tracking-tight sm:text-6xl">
        Where is this number from, and who runs the line?
      </h1>
      <p className="mt-5 max-w-xl text-lg text-ink/70">
        Paste a phone number. You get its country, region, carrier, line type and a map pin.
      </p>

      <form onSubmit={lookup} className="mt-10 flex flex-col gap-3 sm:flex-row">
        <label className="flex-1">
          <span className="sr-only">Phone number</span>
          <input value={number} onChange={(e) => setNumber(e.target.value)} required placeholder="+27 82 123 4567"
            className="w-full border-2 border-ink bg-white px-4 py-3 text-xl" />
        </label>
        <label>
          <span className="sr-only">Country code for local numbers</span>
          <input value={region} onChange={(e) => setRegion(e.target.value.slice(0, 2))} placeholder="ZA" maxLength={2}
            title="Only needed if the number has no + prefix" className="w-full border-2 border-ink bg-white px-4 py-3 text-xl uppercase sm:w-24" />
        </label>
        <button disabled={loading} className="bg-ink px-7 py-3 text-xl font-medium text-paper hover:bg-signal disabled:opacity-60">
          {loading ? "Looking up" : "Look up number"}
        </button>
      </form>
      <p className="mt-2 text-sm text-ink/60">Local format like 082 123 4567? Add the two-letter country code, e.g. ZA.</p>

      <div aria-live="polite">
        {error && <p className="mt-8 border-l-4 border-signal pl-4 text-lg">{error}</p>}
        {data && (
          <section className="mt-12 grid gap-8 md:grid-cols-2">
            <dl className="divide-y divide-line border-y border-line">
              {rows.map(([k, v]) => (
                <div key={k} className="flex justify-between gap-4 py-3">
                  <dt className="text-ink/60">{k}</dt>
                  <dd className="text-right font-medium">{v ?? "Not available"}</dd>
                </div>
              ))}
            </dl>
            {c ? (
              <iframe title="Map of number location" className="h-80 w-full border-2 border-ink md:h-full"
                src={`https://www.openstreetmap.org/export/embed.html?bbox=${c.lng - 1},${c.lat - 0.7},${c.lng + 1},${c.lat + 0.7}&layer=mapnik&marker=${c.lat},${c.lng}`} />
            ) : (
              <p className="self-center text-ink/60">No map for this number. Add an OpenCage key to the backend to enable it.</p>
            )}
          </section>
        )}
      </div>
    </main>
  );
}
