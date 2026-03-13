---
title: 'Welfen Sportscam'
date: '2026-02-17T18:15:44+01:00'
author: 'Giancarlo Rizzo'
draft: true
categories: []
color: '#a09f93'
---

{{< mermaid >}}
flowchart TD

  %% ---------- 1. Remote control ----------

  A[Remote Host Contoller]

  B[MQTT Broker]

  C[Pi‑4‑4 GB]

  D[Pi‑4‑8 GB]

 

  A -->|MQTT publish| B

  B -->|subscribe| C

  B -->|subscribe| D

 

  %% ---------- 2. Camera Pi – Array‑Hat & sensors ----------

  C -->|arrayhat| E[Arducam Array‑Hat]

  E -->|sensor 1| F[IMX477‑1]

  E -->|sensor 2| G[IMX477‑2]

  F & G -->|side‑by‑side frame| H[rpicamera2 – capture SBS]

  H -->|split → Left / Right| I[Split]

  I -->|undistort K1,D1 / K2,D2| J[Rectified halves]

  J -->|stitch & blend| K[Panorama 1080p]

  K -->|queue PANO_Q| D

 

  %% ---------- 3. 8‑GB Pi – post‑process & stream ----------

  D -->|receive 1080p from PANO_Q| L[Optional detection]

  L -->|crop / cameraman effect| M[Final 1080p frame]

  M -->|TCP stream| N[tcp://localhost:7271/game]

 
{{< /mermaid >}}