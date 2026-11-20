"""
同步此專案至 Hugging Face Space: violita777/hello2
使用方式: python sync_to_space.py
"""
import os
import sys
import time
from huggingface_hub import HfApi, get_token

REPO_ID = "violita777/hello2"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
CHECK_FILES = ["index.html", "style.css"]


def main():
    print("=" * 55)
    print(f"  同步到 Hugging Face Space: {REPO_ID}")
    print(f"  上傳資料夾: {PROJECT_DIR}")
    print("=" * 55)

    for name in CHECK_FILES:
        path = os.path.join(PROJECT_DIR, name)
        if os.path.exists(path):
            mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(path)))
            print(f"  ✔ {name}  (最後修改 {mtime})")
        else:
            print(f"  ✘ 找不到 {name}")

    token = sys.argv[1].strip() if len(sys.argv) > 1 else None
    token = token or os.environ.get("HF_TOKEN") or get_token()
    if token:
        print("\n已找到儲存的 Token。")
    elif sys.stdin.isatty():
        token = input("\n請貼上 Hugging Face Token (需 Write 權限): ").strip()
    if not token:
        print("未提供 Token，取消上傳。")
        return

    print("\n開始上傳，請稍候...")
    commit = HfApi().upload_folder(
        folder_path=PROJECT_DIR,
        repo_id=REPO_ID,
        repo_type="space",
        token=token,
        commit_message="Sync project to Space",
        ignore_patterns=[".git", ".git/**", "*.pyc", "__pycache__/**",
                         "node_modules/**", "sync_to_space.py"],
    )
    print("\n✅ 上傳成功！")
    print(f"Commit: {getattr(commit, 'commit_url', commit)}")
    print(f"Space：https://huggingface.co/spaces/{REPO_ID}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 上傳失敗：{e}")
    if sys.stdin.isatty():
        input("\n按 Enter 關閉視窗...")