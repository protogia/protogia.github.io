---
title: 'Wie man ein vollgelaufenes Remotesystem retten kann, ohne Daten zu verlieren'
date: '2023-11-03T14:34:06+01:00'
author: 'Giancarlo Rizzo'
draft: false
tags: offtopic
categories: []
color: '--base0a'
---

Es sollte zwar nicht passieren, doch die Realität sieht oft anders aus. Remoteserver, die eventuell nicht im Monitoring eingebunden sind, oder für die kein Alerting existiert, laufen voll, sobald mehrere User diese ausgiebig nutzen und die Systempflege vergessen wird. Schlimmstenfalls sind die füllenden Logdateien sogar noch wichtig und dürfen nicht verloren gehen.


## Identifizieren der speicherintensivsten Ordner

1. Zunächst sollte man den Ort des Problems finden. Man listet alle Verzeichnisse und ihre Speicherbelegung auf. 

```bash
sudo du -sh /*
```

2. Will man den Kern des Problems herausfinden, sollte man die Ausgabe sortieren und dann die Top-10-EInträge filtern: 

```bash
sudo du -sh ./* | sort -h | head -n 10
```

## Transferieren und Löschen

Nun kann man beginnen den Ordner mit der größten Speicherbelegung zu transferieren. Besteht eine unsichere Verbindung wie z.B. über LTE, sollte man Dateiweise vorgehen, um keinen broken-pipe-Fehler zu riskieren. Dafür benutzt man rsync 

```bash
mkdir ~/Downloads/save_bckp
rsync --remove-source-files -av remoteuser@<remoteip>:/path/to/big/folder/* ./Downloads/save_bckp
```

Der Vorgang dauert lange, aber dadurch wird gleichzeitig die Festplatte geleert und die Daten werden gesichert. Im Fall von Verbindungsabbrüchen, kann man den Befehl neustarten, ohne dass man Dateien auslässt. Wenn die Verbindung als sicher eingestuft werden wird, kann man auch scp recursiv verwenden. Das funktioniert schneller, aber es birgt ein Risiko.

## Warum Ansible nicht klappt

Weder das Prüfen des Dateisystems noch das Übertragen und Löschen von Dateien via Ansible würde funktionieren, da beim Ausführen von Ansible-Modulen Python-Pakete auf das remotesystem übertragen werden, die bei einer wirklich vollen Festplatte gar nicht mehr angelegt werden können. 

## Wenn Login nicht mehr möglich ist

Wenn der remote-login nicht mehr möglich ist kann man versuchen per Hardreset den Host neuzustarten, sofern dieser über eine externe Schalteinheit Stromlos geschaltet werden kann.
