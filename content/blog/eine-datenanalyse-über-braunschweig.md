---
title: 'Ein Porträt in Daten: Braunschweig'
date: '2023-10-30T14:12:47+01:00'
author: 'Giancarlo Rizzo'
draft: false
tags: offtopic
categories: []
color: '--base0a'
---

# Prolog

Die Stadt Braunschweig hat sich in den letzten Jahren sehr verändert. Mithilfe verschiedener Datenquellen möchte ich in diesem Blogpost versuchen, Veränderungen und ihre Wahrnehmung in der Öffentlichkeit zu visualisieren. Dieser Blogpost beginnt eine Serie zu einem datenbasierten Porträt von Braunschweig.  

Dafür möchte ich zu Beginn folgende Datenquellen verwenden:

[OpenData - Braunschweig](https://opendata.braunschweig.de/)

Für den Zugriff auf die Opendata-Datensätze habe ich einen simplen [REST-client auf Basis der DKAN-Portal-API](https://github.com/protogia/govdata) implementiert. Dieser unterstützt zum Zeitpunkt dieser Veröffentlichung nur lesende Zugriffe, um Datensätze aus python heraus zu suchen, herunterzuladen und zu verarbeiten.

GovData/Open Data ist das Resultat aus der Open-Data-Gesetzgebung und der Open-Data-Strategie, nach welchem Behörden der unmittelbaren Bundesverwaltung verpflichtet sind erhobene Daten öffentlich zur Verfügung zu stellen.

[Google Trends](https://trends.google.com/trends/)

Den Zugriff auf die historischen Google-Trends-Ergebnisse möchte ich durch die inoffizielle [pytrends-api](https://pypi.org/project/pytrends/) umsetzen. Dabei wird die Herausforderung sein, anhand von Suchbegriffen systematisch Schlüsse zu ziehen und die Ergebnisse in Kontext zu den Opendata-Datensätzen zu bringen.

# Nachvollziehbarkeit

Zur besseren Nachvollziehbarkeit meiner Analysen können die Daten auch unter [google.colab](https://colab.research.google.com/) selbst analysiert werden. Voraussetzung dafür ist ein Google Konto mit Altersverifizierung. Die Nutzung von colab ist aber kostenlos, solange man keine Zusatzpakete bucht. 

Bei der Nutzung der Notebooks muss bedacht werden, dass alle von mir verwendeten API's keine offiziellen Implementierungen darstellen, wodurch Änderungen an der Schnittstelle der Datenquellen zu Fehlfunktionen führen können.



