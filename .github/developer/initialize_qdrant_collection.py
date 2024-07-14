print("Starting the script execution...")  # スクリプトの開始を確認

from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
import os

# .envファイルのパスを指定
env_path = os.path.join(os.path.dirname(__file__), '.github', 'scripts', '.env')
# .envファイルのパスをデバッグ出力
print(f"Loading .env file from: {env_path}")

# .envファイルが存在するか確認
if not os.path.exists(env_path):
    print(f"Error: .env file not found at {env_path}")
else:
    print(f".env file found at {env_path}")

load_dotenv(dotenv_path=env_path)

QDRANT_URL = os.getenv('QD_URL')
QDRANT_API_KEY = os.getenv('QD_API_KEY')

# デバッグ用に環境変数をプリント
print(f"QD_URL: {QDRANT_URL}")
print(f"QD_API_KEY: {QDRANT_API_KEY}")

# APIキーが設定されているか確認
if QDRANT_URL is None:
    print("Error: QD_URL is not set. Please check your .env file.")
    raise ValueError("QD_URL is not set. Please check your .env file.")

if QDRANT_API_KEY is None:
    print("Error: QD_API_KEY is not set. Please check your .env file.")
    raise ValueError("QD_API_KEY is not set. Please check your .env file.")

#print(f"API Key: {QDRANT_API_KEY[:5]}...{QDRANT_API_KEY[-5:]}")  # API keyの最初と最後の5文字のみを表示

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
print(f"Attempting to connect to Qdrant at: {QDRANT_URL}")

try:
    # コレクションの一覧を取得（これは通常、より低い権限で可能）
    collections = client.get_collections()
    print("Existing collections:")
    print(collections)
except Exception as e:
    print(f"Error getting collections: {str(e)}")

try:
    # コレクションの作成を試みる
    client.create_collection(
        collection_name="issue_collection",
        vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
    )
    print("Collection 'issue_collection' created successfully")
except Exception as e:
    print(f"Error creating collection: {str(e)}")

# 既存のコレクションの詳細情報取得を試みる
try:
    collection_info = client.get_collection("issue_collection")
    print("Collection info:")
    print(collection_info)
except Exception as e:
    print(f"Error getting collection info: {str(e)}")
