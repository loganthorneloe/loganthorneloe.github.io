---
title: "Projects"
date: today
draft: false
---

## **Stock Boy** ([frontend repo](https://github.com/lathorne/stock-boy), [backend repo](https://github.com/lathorne/stock-boy-functions))
A progressive web app that pulls financial data directly from SEC filings and determines a percent confidence in the long-term growth of the stock based on the principles of good investing found in "Warren Buffett and the Interpretation of Financial Statements". The goal was to make it easy for retail investors to invest using proper information.

A user could search the PWA for a stock by name, ticker, or CIK. A table would then display ~25 markers for stock growth for that stock and use the scores of each marker to determine a percent confidence. The markers would display data for each year that could be retrieved from the SEC.

**Uses react.js, firebase, nosql, automation, and google cloud platform.**

## **Self-Playing Nintendo Switch** ([repo](https://github.com/lathorne/swsh-pokemon-breeder))

Firmware for automatically breeding shiny Pokemon using an Arduino. Forked from a project doing a similar thing for The Legend of Zelda: Breath of the Wild.

Code for an Arduino to be treated like a controller for the Nintendo Switch. The Arduino is programmed for character movement and interaction on a loop. I would use it to breed Pokemon over night hoping for a shiny in the morning. This can be used for any simple, repetitive task in a Nintendo Switch game. For more info on how to use it, see the Github repo linked below.

**Uses arduino, automation, and firmware.**