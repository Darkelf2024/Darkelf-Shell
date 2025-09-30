# Darkelf Shell — Feature Highlights

## Overview

**Darkelf Shell** is a privacy-focused, anti-fingerprinting browser shell with advanced security features. It is designed for researchers, privacy enthusiasts, and anyone seeking maximum anonymity and anti-tracking defenses.

![Darkelf Shell](https://github.com/Darkelf2024/Darkelf-Shell/blob/main/Darkelf%20images/Darkelf%20Shell%20Home.png)

---

## 🔒 Privacy & Fingerprint Defenses

- **Persona Engine:** Rotates realistic browser/OS profiles (user agent, platform, languages, hardware, screen, WebGL, etc.).
- **Canvas Fingerprint Quantization:** All canvas exports and getImageData are quantized (Tor-style) for strong anti-canvas fingerprinting.
- **WebGL Spoofing:** WebGL vendor and renderer strings are spoofed, and readPixels are perturbed.
- **Audio, Fonts, Battery, Clipboard, WebRTC, Media, Sensor Defenses:** Blocks or spoofs all popular fingerprinting surfaces.
- **User-Agent & Client-Hints Spoofing:** Adaptive spoofing of both classic and modern browser identification vectors.
- **Strict CSP Meta Injection:** Enforces inline-script and resource policies to minimize XSS and external code execution.

---

## 🕵️ Tor Integration

- **Native Tor Proxy Management:** Launch, manage, and rotate Tor circuits directly (via `stem` and system Tor).
- **Onion-Optimized Search:** Optionally uses DuckDuckGo's .onion endpoint for private search.
- **Automatic Proxy Routing:** Sets `ALL_PROXY`, `HTTP_PROXY`, `HTTPS_PROXY` for full system routing through Tor.
- **Tor Status Overlay:** Visual indicator and control for Tor activation within the browser shell.

---

## 🖥️ Modern PyWebView UI

- **Custom Toolbar Overlay:** Back/forward/reload, Tor status, tracker/ad blocking, zoom, and home.
- **Context Menu:** Right-click menu with copy/paste/select all, "Paste & Go", etc.
- **Trackers Blocked Badge:** Live count and blocking of trackers/ads via heuristic JS rules.

---

## 🛡️ AI Security & Anti-Phishing

- **Mini AI Security Module:** Detects phishing, malware, and network sniffers via both JS and Python hooks.
- **Panic Mode:** On threat detection, disables JS, locks navigation, clears proxies, and shows a user alert; auto-releases after timeout.
- **Live Scan:** Phishing keywords, malware patterns, and network analysis are performed on each page/request.

---

## 🗑️ Storage & Cookie Hardening

- **Automatic Storage Clearing:** On page load, clears local/session storage, cookies, and indexedDB.
- **Accept-Language/Referer/Origin Stripping:** Removes these headers from outgoing requests.
- **3rd-Party Cookie and IFrame Blocking:** Prevents cross-site tracking via cookies and iframes.

---

## 🖥️ Platform-Specific Features

- **macOS Native Persona/JS Toggle:** Uses WKWebView APIs for real user agent and script toggling at the engine level.
- **Native Zoom/JS Toggle:** For macOS, swaps actual WKWebView instance for true JS enable/disable and zoom.

---

## 🛠️ Tab & API Features

- **Simple Tab State Tracking:** In-memory tabs with full navigation history.
- **Open/Switch/Close Tabs:** All core multi-tab functions are supported.
- **Pythonic API:** All browser controls are exposed via Python for automation/scripts.

---

## 🚀 Command-Line Configuration

- **CLI Options:** `--start`, `--tor`, `--tor-proxy` for custom start page or Tor routing.
- **Modern Home Page:** Custom HTML home page with branding, search, and Tor status.

---

## 🔍 Summary Table

| Feature                        | Description                                                                              |
|---------------------------------|------------------------------------------------------------------------------------------|
| Persona Engine                  | Rotates browser/OS fingerprints, anti-canvas/WebGL, client hints spoofing                |
| Tor Proxy Integration           | Launch, rotate, and control Tor from within the browser                                  |
| AI Security Panic Mode          | Auto-lockdown on phishing/malware/sniffer detection                                      |
| Full Storage/State Clearing     | Deletes cookies, storage, indexedDB on every load                                        |
| Overlay UI                      | Custom toolbar, tracker/ad counter, context menu                                         |
| Tracker/Ad Blocking             | JS-powered blocks and badges for common trackers/ads                                     |
| CSP/Headers Hardening           | Blocks Accept-Language, Referer, Origin; strict CSP; blocks 3rd-party cookies/iframes    |
| Multi-Tab Support               | In-memory tab state/history, open/close/switch tabs                                      |
| Extensive API                   | All browser controls (navigation, zoom, JS enable) via Python                            |
| macOS Native Features           | Real UA/JS toggling and zoom via WKWebView                                               |

---

## 🏁 Philosophy

- **No Addons Needed:** All defenses are built-in; no user scripts or browser extensions required.
- **Transparency:** All UI and defenses are visible and auditable in Python and JS.

---

**Darkelf Shell is one of the most advanced privacy and research browsers in Python.**
