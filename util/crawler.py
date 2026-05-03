
import os
import time
import requests

def download_tarot_images():
    # 이미지 저장 폴더 생성 (상위 폴더 기준으로 생성)
    save_dir = os.path.join('..', 'images')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 전체 이미지 목록
    image_data = [
        {"filename": "00_The_Fool.png", "url": "https://upload.wikimedia.org/wikipedia/commons/c/c0/The_Fool_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "01_The_Magician.png", "url": "https://upload.wikimedia.org/wikipedia/commons/5/57/The_Magician_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "02_The_High_Priestess.png", "url": "https://upload.wikimedia.org/wikipedia/commons/0/0d/The_High_Priestess_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "03_The_Empress.png", "url": "https://upload.wikimedia.org/wikipedia/commons/f/fb/The_Empress_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "04_The_Emperor.png", "url": "https://upload.wikimedia.org/wikipedia/commons/f/f8/The_Emperor_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "05_The_Hierophant.png", "url": "https://upload.wikimedia.org/wikipedia/commons/f/fe/The_Hierophant_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "06_The_Lovers.png", "url": "https://upload.wikimedia.org/wikipedia/commons/1/1b/The_Lovers_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "07_The_Chariot.png", "url": "https://upload.wikimedia.org/wikipedia/commons/8/88/The_Chariot_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "08_Strength.png", "url": "https://upload.wikimedia.org/wikipedia/commons/7/74/Strength_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "09_The_Hermit.png", "url": "https://upload.wikimedia.org/wikipedia/commons/1/1a/The_Hermit_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "10_Wheel_of_Fortune.png", "url": "https://upload.wikimedia.org/wikipedia/commons/0/03/Wheel_of_Fortune_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "11_Justice.png", "url": "https://upload.wikimedia.org/wikipedia/commons/8/85/Justice_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "12_The_Hanged_Man.png", "url": "https://upload.wikimedia.org/wikipedia/commons/8/8e/The_Hanged_Man_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "13_Death.png", "url": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Death_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "14_Temperance.png", "url": "https://upload.wikimedia.org/wikipedia/commons/6/66/Temperance_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "15_The_Devil.png", "url": "https://upload.wikimedia.org/wikipedia/commons/b/b5/The_Devil_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "16_The_Tower.png", "url": "https://upload.wikimedia.org/wikipedia/commons/8/8c/The_Tower_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "17_The_Star.png", "url": "https://upload.wikimedia.org/wikipedia/commons/0/09/The_Star_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "18_The_Moon.png", "url": "https://upload.wikimedia.org/wikipedia/commons/1/18/The_Moon_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "19_The_Sun.png", "url": "https://upload.wikimedia.org/wikipedia/commons/0/0a/The_Sun_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "20_Judgement.png", "url": "https://upload.wikimedia.org/wikipedia/commons/2/2e/Judgement_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "21_The_World.png", "url": "https://upload.wikimedia.org/wikipedia/commons/9/95/The_World_%28Rider-Waite_Smith_tarot_deck%29.png"},
        {"filename": "ace_of_pentacles.png", "url": "https://upload.wikimedia.org/wikipedia/commons/5/54/One_of_Pentacles_%28Rider-Waite_Smith_tarot_deck%29.png"}
    ]

    # 브라우저처럼 보이기 위한 헤더 설정
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://commons.wikimedia.org/wiki/Category:Rider-Waite-Smith_tarot_deck_(Geldard)"
    }

    print(f"총 {len(image_data)}개의 타로 에셋 다운로드를 확인합니다.")

    for item in image_data:
        filename = item['filename']
        url = item['url']
        target_path = os.path.join(save_dir, filename)

        # 이미 정상 파일(1MB 이상)이 있으면 건너뛰기
        if os.path.exists(target_path) and os.path.getsize(target_path) > 1024 * 1024:
            print(f"[OK] {filename}")
            continue

        success = False
        while not success:
            try:
                print(f"[Download] {filename}...", end="", flush=True)
                response = requests.get(url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    with open(target_path, 'wb') as f:
                        f.write(response.content)
                    print(" 완료!")
                    success = True
                    time.sleep(15) # 서버 부하 방지용 딜레이
                elif response.status_code == 429:
                    print("\n[Wait] 차단됨(429). 2분간 대기 후 다시 시도합니다...")
                    time.sleep(120)
                else:
                    print(f" 실패 (상태: {response.status_code})")
                    break
            except Exception as e:
                print(f" 오류: {e}")
                break

    print("모든 에셋이 준비되었습니다.")

if __name__ == "__main__":
    download_tarot_images()
