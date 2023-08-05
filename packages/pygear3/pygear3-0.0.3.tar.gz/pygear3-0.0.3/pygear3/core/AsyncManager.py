
import functools
import asyncio
import threading
import sys,logging,os
import concurrent

class Log(object):
    '''
    装饰器类
    '''
    def __init__(self, logfile='out.log'):
        self.logfile = logfile

    def __call__(self, func):
        @functools.wraps(func)
        def wrapped_function(*args, **kwargs):
            self.notify()
            return func(*args, **kwargs)



        return wrapped_function

    def notify(self):
        print("当前线程{},当前进程{}".format(threading.current_thread(), os.getpid()))
        pass
class AsyncManager:
    def __init__(self):
        self.thread_loop = asyncio.new_event_loop()
        #创建线程执行器
        # self.thread = concurrent.futures.Thraed()
        #创建进程执行器
        # self.process = concurrent.futures.ProcessPoolExecutor()
        thread = threading.Thread(target=AsyncManager.thread_loop_func,args=(self.thread_loop ,))
        thread.setDaemon(True)
        thread.start()
    @staticmethod
    def thread_loop_func(loop):
        '''
        :param loop: 事件loop对象
        :return: 无
        '''
        asyncio.set_event_loop(loop)
        loop.run_forever()
    def add_task(self,func,args=None,callback=None,is_thread=True,is_process=False):
        '''
        添加运行任务
        :param func: 函数地址
        :return:
        '''
        try:
            if not args:
                #添加async 异步函数,run_coroutine_threadsafe返回Future,无法await
                #添加新的任务放入到线程循环中
                task = asyncio.run_coroutine_threadsafe(func,self.thread_loop)
                # 回调函数
                if callback:
                    task.add_done_callback(callback)
                return task
            else:
                #不加async方法,并发执行,原理执行多个thread
                task = self.thread_loop.run_in_executor(None,func,args)
                # # 回调函数
                return task
        except Exception as e:
            logging.error("[+++++]line:{0},Function:{1},Exception:{2}".format(sys._getframe().f_lineno,
                                                                              sys._getframe().f_code.co_name,
                                                                                  str(e)))
    def loop_stop(self):
        self.thread_loop.stop()
        self.thread_loop.close()



