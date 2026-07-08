# 개요
```sh
# 260505 V1.2

editer: 김은채(ec.kim@shield-one.com)

SentinelOne의 Linux coinminer 방어 사례를 모방하여 안전한 환경에서 사용자 이해를 돕기 위한 Shieldone의 악성 파일 시나리오 시연용 데이터입니다.
절대. 그 외 용도로 사용하지 마세요
```

## 시나리오 동선
본 시나리오는 클라우드 인프라의 '마스터 키'를 노리고 개발자를 겨냥한 'Openclaw 타이포 스쿼팅' 공급망 공격 체인을 재현했습니다. 

피해자가 위장된 악성 레포지토리를 `git clone`하여 `setup.py`를 실행하는 순간, 시스템 백그라운드에서는 은밀하게 백도어 계정이 생성되고 suudo 권한이 변조되며 지속성 유지를 시도합니다. 

그러나 SentinelOne의 Behavioral AI 엔진은 프로세스가 `/etc/shadow`와 같은 민감한 OS 파일에 접근하고, 외부로 유출하기 위해 클라우드 메타데이터(IMDS) 서버에 권한 토큰을 요청하는 일련의 악의적 의도를 문맥적으로 식별하여 즉각적인 알람을 발생시킵니다. 

특히, sudo 권한을 탈취한 공격자가 최상위 Root 계정으로 SentinelOne 에이전트를 무력화하려 시도하더라도, Linux 커널 레벨에서 동작하는 S1의 강력한 eBPF 기반 자가 보호(Anti-Tamperw) 기술이 이를 원천 차단합니다.

## 도입 환경
- **목적**: 최근 2026년 4월 N사에서 발생한 **'Openclaw 타이포 스쿼팅'** 사례를 모방하여 실제 공격 체인을 재현

- **환경**:
    - **피해자**: Rocky Linux 기반의 서비스 개발자로, Cloud-Native 인프라를 개발하는 상황을 상정했습니다.
    - 공격자는 이 개발자가 사용하는 `openclaw`라는 유명 서비스를 노렸습니다.
    - 공격자 입장에서는 이 개발자 한 명만 잡으면 기업 전체 서버 인프라의 '마스터 키'를 얻는 것과 다름없기 때문에, 가장 고수익 공격 대상이 됩니다.

- **주의사항**: 공격의 전 과정을 보여드리기 위해 현재 SentinelOne은 **탐지(Detect) 모드**로만 동작 중입니다.

---

# 환경 설정

## 파일 구성
```
/ec_openclwa
│
├── 기타 파일들
│
├── makeDummy.sh
│   > 유출용 크리덴셜 키 생성
│
├── requirements.txt
│    > 백도어용 계정 생성
│    > C2 통신 정보
│
└── setup.py
	> 실제 공격
	> 인포스틸
	> C2를 통한 정보 유출
```

## 환경 설정
```bash
sudo dnf install nc python3 -y

sudo dnf install -y git
```

- 확인 된 OS
    - Rocky 10
    - Rocky 8.10

- 필요 사항: Github Repository에 연결 가능한 환경

---

# 사용 방법

## 1. Git Repository Clone

```
git clone https://github.com/KimEC995/ec_openclwa.git
```

이 때 Hacking Tool을 가정한 정적 탐지가 2건 발생합니다.

## 2. 환경 구성
시나리오 진행을 위해 임의로 민감 정보를 생성합니다.

```
// 권한 부여
chmod +x makeDummy.sh setup.py

// 더미 파일 생성
sudo ./makeDummy.sh
```

만약 C2 통신과 함께 구성한다면, 이 때 `requirements.txt` 에 C2 값을 수정합니다.

```
// 15번 줄
c2_receiver: IP 정보:포트
```


## 3. 악성 파일 실행
공격자가 Git 프로젝트로 위장한 `requirements.txt`에서 정보를 추출, 실행합니다.

```
// 악성 파일 실행(python3 혹은 py로 실행합니다)
python3 setup.py
```

## 4. 추가 페이로드 실행
setup.py를 실행하면 아래와 같은 문장이 출력됩니다.

```
[*] Checking for external payloads in '{payload_dir}'...
```

다운 받은 악성 파일을 실행합니다.
원하면 1 / 아니라면 2
