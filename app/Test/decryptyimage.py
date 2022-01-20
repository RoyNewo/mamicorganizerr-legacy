import requests

# try block to handle the exception
try:
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
    url = "https://mangaplus.shueisha.co.jp/drm/title/100030/chapter/1004865/manga_page/super_high/2914278.jpg?key=5e51322d13f3ba8ef15ac3407127ac8e&duration=86400"

    # take path of image as a input
    path = '/home/cristian/Github/TachiyomiMangaOrganizer/Test/decryptest.jpg'

    resp = requests.get(url, headers=headers)
    data = bytearray(resp.content)
    key = bytes.fromhex('d2da3b30ac8a2a706254b03527f3ef743a3517f0f535cb7012fb7e8e3a68ca1f6e0be56cc0476a830b4a1297db4f4686149bb4a2e6b750210eb8420160f8e67a')
    a = len(key)
    for s in range(len(data)):
        data[s] ^= key[s % a]

    with open(path, 'wb') as fin:
        # writing decryption data in image
        fin.write(data)
except Exception:
    print('Error caught : ', Exception.__name__)