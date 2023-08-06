# coding=utf-8
from QuickStart_Rhy.NetTools import size_format, get_fileinfo
from concurrent.futures import ThreadPoolExecutor, wait
from QuickStart_Rhy.ThreadTools import FileWriters
from threading import Lock
from requests import get
import psutil
import signal
import queue
import time
import os

core_num = psutil.cpu_count()
maxBlockSize = int(1.5e6)
minBlockSize = int(5e5)


def GetBlockSize(sz):
    """
    自动规划块大小

    Automatically program the block size

    :param sz: 文件大小
    :return: 块大小
    """
    if sz >= maxBlockSize << 10:
        return maxBlockSize
    elif sz <= minBlockSize << 3:
        return minBlockSize
    else:
        return max(sz >> 9, minBlockSize)


class Downloader:
    def __init__(self, url: str, num: int, set_name: str = ''):
        """
        qs普通文件下载引擎

        Qs general file download engine

        :param url: 文件url
        :param num: 线程数量
        """
        signal.signal(signal.SIGINT, self._kill_self)
        self.has_ctrl = False
        self.url = url
        self.num = num
        self.name = os.path.basename(url)
        self.fileLock = Lock()
        self.cur_sz = 0
        self.url, self.name, r = get_fileinfo(url)
        if set_name:
            self.name = set_name
        if not self.url:
            print('[ERROR] Connection Error!')
            exit(0)
        try:
            self.size = int(r.headers['Content-Length'])
            if self.size < 5e6:
                print('[INFO] FILE SIZE\t{}'.format(size_format(self.size)))
                self.size = -self.size
            else:
                self.fileBlock = GetBlockSize(self.size)
        except KeyError:
            self.size = -1
        if self.size > 0:
            self.pool = ThreadPoolExecutor(max_workers=self.num)
            self.futures = []
            self.job_queue = queue.Queue()
            if os.path.exists(self.name + '.qs_dl'):
                self.ctn_file = open(self.name + '.qs_dl', 'r+')
                self.ctn = [int(i) for i in self.ctn_file.read().strip().split()]
            else:
                self.ctn_file = open(self.name + '.qs_dl', 'w')
                self.ctn = []
            self.writers = FileWriters(self.name, max(2, int(core_num / 2)), "rb+" if self.ctn else "wb")
            print('[INFO] FILE SIZE\t{}'.format(size_format(self.size, align=True)))
            print('[INFO] BLOCK SIZE\t{}'.format(size_format(self.fileBlock, align=True)))

    def _kill_self(self, signum, frame):
        """
        结束下载任务，保存断点

        Finish the download and save the breakpoint

        :param signum: 信号
        :param frame: frame
        :return: None
        """
        if self.size > 0:
            print('\n[INFO] Get Ctrl-C, exiting...')
            self.ctn_file.close()
            self.pool.shutdown()
            self.writers.wait()
            print('[INFO] Deal Done!')
        os._exit(0)

    def _dl(self, start):
        """
        执行文件块下载任务

        Perform the file block download task

        :param start: 文件块起始偏移量
        :return: None
        """
        try:
            _sz = min(start + self.fileBlock, self.size)
            headers = {'Range': 'bytes={}-{}'.format(start, _sz)}
            tm = time.perf_counter()
            r = get(self.url, headers=headers, timeout=50)
            tm = time.perf_counter() - tm
            self.writers.new_job(r.content, start)
        except Exception as e:
            msg = repr(e)
            print('\n[ERROR] %s' % msg[:msg.index('(')])
            self.job_queue.put(start)
        else:
            self.fileLock.acquire()
            self.ctn.append(start)
            self.ctn_file.write('%d\n' % start)
            self.cur_sz += _sz - start
            self.fileLock.release()
            speed = size_format((self.fileBlock * self.num / tm), align=True)
            per = self.cur_sz / self.size
            print('\r[%s] %.2f%% | %s/s' % (
                '#' * int(40 * per) + ' ' * int(40 - 40 * per),
                per * 100, speed
            ), end='\n' if self.cur_sz == self.size else '')

    def _single_dl(self):
        """
        无法并行下载或无需并行下载时采用串行下载

        Parallel downloads are not possible or serial downloads are not required

        :return: None
        """
        r = get(self.url, stream=True)
        flag = self.size != -1
        size = -self.size
        with open(self.name, 'wb') as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
                self.cur_sz += 8192
                if flag:
                    self.cur_sz = min(self.cur_sz, size)
                print('\r[PROC] %s' % size_format(self.cur_sz, align=True), end='')
            print('')
            if flag and self.cur_sz < size:
                print('[ERROR] Data loss!')

    def run(self):
        """
        规划下载任务并开始下载

        qs可以有效应对网络问题对下载任务造成的影响，如：
          1.下载过程中切换代理

          2.链路异常
        并确保下载任务顺利完成

        :return: None
        """
        if self.size > 0:
            if not self.ctn:
                with open(self.name, "wb") as fp:
                    fp.truncate(self.size)
            for i in range(0, self.size, self.fileBlock):
                if self.ctn and i in self.ctn:
                    self.cur_sz += min(i + self.fileBlock, self.size) - i
                else:
                    self.job_queue.put(i)
            retry_cnt = 0
            while not self.job_queue.empty():
                self.futures.clear()
                while not self.job_queue.empty():
                    cur = self.job_queue.get()
                    if cur not in self.ctn:
                        self.futures.append(self.pool.submit(self._dl, cur))
                wait(self.futures)
                if not self.job_queue.empty() and retry_cnt > 2:
                    print('\r[INFO] Exists File Block Lost, Retrying after 0.5 sec')
                    time.sleep(0.5)
                retry_cnt += 1
            self.writers.wait()
            self.ctn_file.close()
            os.remove(self.name + '.qs_dl')
        else:
            self._single_dl()
        print('[INFO] %s download done!' % self.name)


def normal_dl(url, set_name: str = ''):
    """
    自动规划下载线程数量并开始并行下载

    Automatically schedule the number of download threads and begin parallel downloads

    :param set_name: 设置文件名（默认采用url所指向的资源名）
    :param url: 文件url
    :return: None
    """
    Downloader(url, min(16, core_num * 4), set_name).run()
