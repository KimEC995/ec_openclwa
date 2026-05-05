#!/bin/bash

SAVED_STTY=$(stty -g)

echo "======================================================"
echo "[*] Purging Backdoor Persistence & Simulation"
echo "======================================================"

# 2. requirements.txt에서 실시간 ID 추출
CONFIG_FILE="requirements.txt"
if [ -f "$CONFIG_FILE" ]; then
    BD_ID=$(grep "backdoor_user:" "$CONFIG_FILE" | cut -d':' -f2 | tr -d ' ')
else
    BD_ID="kimEC"
fi

# 3. 시뮬레이션 프로세스 종료
echo -n "[-] Stopping setup.py processes... "
sudo pkill -9 -f setup.py 2>/dev/null
echo "DONE"

# 4. 백도어 사용자 삭제
echo "[-] Targeted User Removal: $BD_ID"
if id "$BD_ID" &>/dev/null; then
    # -f 옵션으로 강제 종료 및 삭제 수행
    sudo userdel -r -f "$BD_ID" 2>/dev/null
    sudo rm -f "/etc/sudoers.d/$BD_ID"
    echo "    [V] User '$BD_ID' and Sudoers entry successfully removed."
else
    echo "    [!] User '$BD_ID' not found. Nothing to delete."
fi

# 5. 터미널 속성 강제 복구
echo -n "[*] Restoring terminal settings... "
stty sane
tput rs1
echo "DONE"

echo "------------------------------------------------------"
if id "$BD_ID" &>/dev/null; then
    echo -e "\e[31m[!] Verification FAILED: User still exists.\e[0m"
else
    echo -e "\e[32m[V] Verification PASSED: User has been purged.\e[0m"
fi
echo "======================================================"

reset -Q 2>/dev/null