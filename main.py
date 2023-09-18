import os
import time

import tomli

class Different:
    def __init__(self):
        self.same = None
        self.add = None
        self.remove = None

def Compare(last,now):
    diff = {}
    for addr in last:
        if addr not in now:
            diff[addr] = Different()
            diff[addr].remove = last[addr]
        else:
            diff[addr] = Different()
            diff[addr].same = list(set(last[addr]) & set(now[addr]))
            diff[addr].add = list(set(now[addr]) - set(last[addr]))
            diff[addr].remove = list(set(last[addr]) - set(now[addr]))
    for addr in now:
        if addr not in last:
            diff[addr] = Different()
            diff[addr].add = now[addr]
    return diff

def AddLog(addr,diff):
    """
    1992-01-01 00:00:00
    addr1:
        add:
            file1
            file2
        remove:
            file3
    """
    with open(addr,'a') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        f.write('\n')
        for i in diff:
            f.write(i+':\n')
            if diff[i].add:
                f.write('\tadd:\n')
                for j in diff[i].add:
                    f.write('\t\t'+j+'\n')
            if diff[i].remove:
                f.write('\tremove:\n')
                for j in diff[i].remove:
                    f.write('\t\t'+j+'\n')
        f.write('\n')

def RecordNow(addr,addr2files):
    with open(addr,'w') as f:
        for i in addr2files:
            f.write(i+':\n')
            for j in addr2files[i]:
                f.write('\t'+j+'\n')
    

def ReadRecord(addr):
    addr2files = {}
    if not os.path.exists(addr):
        return addr2files
    with open(addr) as f:
        for line in f:
            if line[0] == '\t':
                addr2files[addr].append(line[1:-1])
            else:
                addr = line[:-2]
                addr2files[addr] = []
    return addr2files
    
    
    
def ReadNow(addr):
    # 读取当前目录下的所有文件
    return os.listdir(addr)

def main():
    with open('config.toml',encoding='utf-8') as f:
        config = f.read()
    
    toml = tomli.loads(config)
    storage = toml['log_addr']
    log_addr = storage + '/log.txt'
    record_addr = storage + '/record.txt'
    moni_addr = toml['monit_addr']

    last = {}
    last = ReadRecord(record_addr)
    now = {}
    for addr in moni_addr:
        now[addr] = ReadNow(addr)
    diff = Compare(last,now)
    AddLog(log_addr,diff)
    RecordNow(record_addr,now)

    
if __name__ == '__main__':
    main()