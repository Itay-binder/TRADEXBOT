"use client";

import { useEffect, useState } from "react";
import { fetchConfig, fetchHealth, runScan, saveConfig } from "../lib/api";

export default function HomePage() {
  const [health, setHealth] = useState("loading");
  const [config, setConfig] = useState(null);
  const [symbolsInput, setSymbolsInput] = useState("BTCUSDT,ETHUSDT");
  const [scanResult, setScanResult] = useState(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        const [healthData, configData] = await Promise.all([fetchHealth(), fetchConfig()]);
        setHealth(healthData.status);
        setConfig(configData);
        setSymbolsInput(configData.symbols.join(","));
      } catch (error) {
        setHealth("offline");
      }
    }
    load();
  }, []);

  async function onSaveConfig(event) {
    event.preventDefault();
    if (!config) return;
    setBusy(true);
    try {
      const payload = {
        ...config,
        symbols: symbolsInput.split(",").map((item) => item.trim()).filter(Boolean)
      };
      const updated = await saveConfig(payload);
      setConfig(updated);
      alert("Configuration saved");
    } catch (error) {
      alert("Failed saving configuration");
    } finally {
      setBusy(false);
    }
  }

  async function onRunScan() {
    setBusy(true);
    try {
      const data = await runScan();
      setScanResult(data);
    } catch (error) {
      alert("Scan failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="container">
      <h1>TRADEXBOT Dashboard</h1>
      <div className="card">
        <strong>Backend status:</strong> {health}
      </div>

      {config && (
        <form className="card" onSubmit={onSaveConfig}>
          <h3>Bot Settings</h3>
          <div className="row">
            <div>
              <label>Timeframe</label>
              <select
                value={config.timeframe}
                onChange={(e) => setConfig({ ...config, timeframe: e.target.value })}
              >
                <option value="5m">5m</option>
                <option value="15m">15m</option>
                <option value="1h">1h</option>
              </select>
            </div>
            <div>
              <label>Strategy</label>
              <select
                value={config.strategy}
                onChange={(e) => setConfig({ ...config, strategy: e.target.value })}
              >
                <option value="breakout_v1">breakout_v1</option>
                <option value="trend_follow_v1">trend_follow_v1</option>
                <option value="mean_reversion_v1">mean_reversion_v1</option>
              </select>
            </div>
            <div>
              <label>Symbols</label>
              <input
                value={symbolsInput}
                onChange={(e) => setSymbolsInput(e.target.value)}
                placeholder="BTCUSDT,ETHUSDT"
              />
            </div>
          </div>

          <div className="row" style={{ marginTop: 12 }}>
            <label>
              <input
                type="checkbox"
                checked={config.live_trading_enabled}
                onChange={(e) => setConfig({ ...config, live_trading_enabled: e.target.checked })}
              />
              {" "}Enable live trading
            </label>
            <label>
              <input
                type="checkbox"
                checked={config.news_filter_enabled}
                onChange={(e) => setConfig({ ...config, news_filter_enabled: e.target.checked })}
              />
              {" "}Enable economic news filter
            </label>
          </div>

          <div style={{ marginTop: 16 }}>
            <button disabled={busy} type="submit">Save Config</button>
          </div>
        </form>
      )}

      <div className="card">
        <h3>Signals</h3>
        <button disabled={busy} onClick={onRunScan}>Run Manual Scan</button>
        {scanResult && <pre>{JSON.stringify(scanResult, null, 2)}</pre>}
      </div>
    </main>
  );
}
