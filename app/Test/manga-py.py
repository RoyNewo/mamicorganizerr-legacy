# filters output
import subprocess
import os

# 'manga-py -f -u "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/75" --skip-incomplete-chapters --print-json --simulate https://es.ninemanga.com/manga/Mokushiroku+no+Yonkishi.html?waring=1'

# proc = subprocess.Popen(
#     "manga-py -r -c 1 https://es.ninemanga.com/manga/Mokushiroku+no+Yonkishi.html?waring=1 --simulate --show-chapter-info",
#     shell=True,
#     stdout=subprocess.PIPE,
# )
# while True:
#     line = proc.stdout.readline()
#     if not line:
#         break
#     # the real code does filtering here
#     print("test:", line.rstrip())
# 'manga-py -f -u "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/75" --skip-incomplete-chapters --print-json --simulate https://webtoons.com/en/action/the-gamer/list?title_no=88'
# webtooncookien = "--cookies timezoneOffset=1 wtu=9142660cf38b9b46b392a5999eaa24d2 needGDPR=true needCCPA=false needCOPPA=false countryCode=ES wtv=2 wts=1,63976E+12 pagGDPR=true atGDPR=AD_CONSENT isCookieUsable=true _gid=GA1.2.1062739046.1639762980 _scid=cd89fb95-a3ef-4551-bb46-be2841f0b866 tpamGDPR=gad%2Cfb%2Ctw%2Csn%2Cbi%2Ctt tpaaGDPR=ga NEO_SES=nnj3PtwBXJcLaXGDNFU1H++GQa8/d8qMpKgOrje1lVYyrjB3QM2XWo63KjERnroBef//I8HU1I/QjM3Syt965F7GRVRShZegcagHQdPmPnyHOpJEsCJEx52hxX6AZ5u0Jk4S1JWp90twijfvmEaEMMjb0kGfygfD8kcuvQT9s2EPpFsdhnQnbRO1kDLL6S1E8B7KBXsp7U+2R2d/uFsruMxihCL2Vfv+JUE1vAodi0oY0HDyknOr0n28MrubOXnVK2FqSR7wEi7KlrsyJyKEEbZ6nLI/pASVncrG3L3rmKnIt94MqIiCaWygIXLdWujnhXx4Yccn3I6H4QYX3NbY6EgURNSCfYF9Q6x7ZqSUX7b0OwlhEiUK3QJFMVBMUca10prsjb7Iyh+BL3akYdrwVFABHbNN/xsK4Nj0dWgzydc= tool_recent_team_721727=0 NEO_CHK=PZTO+AJBfWvbsLj1CVg9siRbbMTOkhDdaro8fxz4F5qZQEjkn0dixFcs8154KZWc9bDnNQVLulMFlejF/w5ksja8z7qax7xbnNWpAyo5gMWpuZ6tIDwgeEaxq0gfmp9ixPonXkw907aj4WwlLGEbyA== _uetsid=c73e80e05f6011ec9b926bc0e109dcc9 _uetvid=c73ef6b05f6011ec8a96b31cdab036e7 _ga_ZTE4EZ7DVX=GS1.1.1639761790.2.1.1639763570.0 _ga=GA1.2.288329965.1638478311"
webtooncookie = "--cookies ageGatePass=true needGDPR=false"
os.system(
    'manga-py -f -u "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/75" --cookies timezoneOffset=1 wtu=9142660cf38b9b46b392a5999eaa24d2 needGDPR=true needCCPA=false needCOPPA=false countryCode=ES wtv=2 wts=1,63976E+12 pagGDPR=true atGDPR=AD_CONSENT isCookieUsable=true _gid=GA1.2.1062739046.1639762980 _scid=cd89fb95-a3ef-4551-bb46-be2841f0b866 tpamGDPR=gad%2Cfb%2Ctw%2Csn%2Cbi%2Ctt tpaaGDPR=ga NEO_SES=nnj3PtwBXJcLaXGDNFU1H++GQa8/d8qMpKgOrje1lVYyrjB3QM2XWo63KjERnroBef//I8HU1I/QjM3Syt965F7GRVRShZegcagHQdPmPnyHOpJEsCJEx52hxX6AZ5u0Jk4S1JWp90twijfvmEaEMMjb0kGfygfD8kcuvQT9s2EPpFsdhnQnbRO1kDLL6S1E8B7KBXsp7U+2R2d/uFsruMxihCL2Vfv+JUE1vAodi0oY0HDyknOr0n28MrubOXnVK2FqSR7wEi7KlrsyJyKEEbZ6nLI/pASVncrG3L3rmKnIt94MqIiCaWygIXLdWujnhXx4Yccn3I6H4QYX3NbY6EgURNSCfYF9Q6x7ZqSUX7b0OwlhEiUK3QJFMVBMUca10prsjb7Iyh+BL3akYdrwVFABHbNN/xsK4Nj0dWgzydc= tool_recent_team_721727=0 NEO_CHK=PZTO+AJBfWvbsLj1CVg9siRbbMTOkhDdaro8fxz4F5qZQEjkn0dixFcs8154KZWc9bDnNQVLulMFlejF/w5ksja8z7qax7xbnNWpAyo5gMWpuZ6tIDwgeEaxq0gfmp9ixPonXkw907aj4WwlLGEbyA== _uetsid=c73e80e05f6011ec9b926bc0e109dcc9 _uetvid=c73ef6b05f6011ec8a96b31cdab036e7 _ga_ZTE4EZ7DVX=GS1.1.1639761790.2.1.1639763570.0 _ga=GA1.2.288329965.1638478311 --skip-incomplete-chapters --print-json --simulate https://www.webtoons.com/en/action/the-gamer/list?title_no=88'
)


# https://www.webtoons.com/en/action/the-gamer/list?title_no=88
