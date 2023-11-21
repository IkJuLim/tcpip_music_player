# TCP/IP Music Player

TCP 프로토콜 기반으로 음악 파일(.wav)을 요청하고 받아서 재생하기위한 프로젝트입니다.

# Environment
- Server : linux, Python3
- Client : macOS, Python3

## Client
- `list` : 서버에 음악 목록을 요청하고 그 결과를 받아 출력합니다.
- `play [song name] `: [song name]를 서버에 요청하여 데이터를 받아 그것을 플레이 시키는 프로세스를 만들어 음악을 재생시킵니다.
- `prev` : 플레이 리스트상 최근 재생한 음악의 이전 곡을 재생시킵니다.
- `next` : 플레이 리스트상 최근 재생한 음악의 다음 곡을 재생시킵니다.
- `stop` : 음악을 재생시키는 프로세스를 terminate 시킵니다.