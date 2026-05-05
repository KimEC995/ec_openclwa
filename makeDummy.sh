#!/bin/bash

echo "======================================================"
echo "[*] Step 1: Generating Infostealer Dummy Data"
echo "======================================================"

# 1. AWS 자격 증명 생성 및 확인
mkdir -p ~/.aws
cat << EOF > ~/.aws/credentials
[default]
aws_access_key_id = AKIAVIMVSAKETHIS404
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
EOF
echo "[+] AWS Credentials Created:"
ls -l ~/.aws/credentials
cat ~/.aws/credentials | head -n 2

# 2. SSH 개인키 생성 및 확인
mkdir -p ~/.ssh
cat << EOF > ~/.ssh/id_rsa
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACD7v7v7v7v7v7v7v7v7v7v7v7v7v7v7v7v7v7v7v7v7v7v7v7v7v7v7v7v7
-----END OPENSSH PRIVATE KEY-----
EOF
chmod 600 ~/.ssh/id_rsa
echo -e "\n[+] SSH Private Key Created:"
ls -l ~/.ssh/id_rsa

# 3. 브라우저 세션 정보 생성 및 확인
mkdir -p ~/.mozilla/firefox/dw32p1.default-release
echo "SESSION_ID=abc123456789deadbeef; USER=admin_finance" > ~/.mozilla/firefox/dw32p1.default-release/cookies.sqlite
echo -e "\n[+] Browser Session Cookie Created:"
ls -l ~/.mozilla/firefox/dw32p1.default-release/cookies.sqlite

echo "------------------------------------------------------"
echo "[!] Verification Complete. All decoy data is ready."
echo "======================================================"