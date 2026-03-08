#!/bin/bash
BASE64=$(base64 -w 0 /home/node/.openclaw/workspace/hero.png)
sed -i "s|data:image/png;base64,iVBORw.*\"|data:image/png;base64,$BASE64\"|" index.html
