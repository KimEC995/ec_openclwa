#!/bin/bash

echo "======================================================"
echo "[*] Step 2: Cleaning up Dummy Data & Artifacts"
echo "======================================================"

# 1. 인포스틸러 서비스 및 프로세스 제거
sudo systemctl stop S1_Info.service 2>/dev/null
sudo systemctl disable S1_Info.service 2>/dev/null
sudo rm -f /etc/systemd/system/S1_Info.service
sudo systemctl daemon-reload
sudo pkill -9 -f s1_info 2>/dev/null

# 2. 생성된 더미 파일들 삭제
rm -rf ~/.aws
rm -f ~/.ssh/id_rsa
rm -rf ~/.mozilla/firefox/dw32p1.default-release
sudo rm -rf /var/tmp/.S1_Info

echo "[-] All dummy credentials and artifacts removed."
echo "[+] System is now clean."
echo "======================================================"