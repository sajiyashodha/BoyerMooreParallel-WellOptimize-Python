import threading
import time

class BadCharShift(threading.Thread):
    def __init__(self, term):
        threading.Thread.__init__(self)
        self.term = term

    def run(self):
        self.skipList = self.generateBadCharShift(self.term)

    def generateBadCharShift(self,term):
        skipList = {}
        for i in range(0, len(term)-1):
            skipList[term[i]] = len(term)-i-1
        return skipList


class SuffixShift(threading.Thread):
    def __init__(self,key):
        threading.Thread.__init__(self)
        self.key = key

    def run(self):
        self.skipList = self.generateSuffixShift(self.key)

    def generateSuffixShift(self,key):
        skipList = {}
        buffer = ""
        for i in range(0, len(key)):
            skipList[len(buffer)] = self.findSuffixPosition(key[len(key)-1-i], buffer, key)
            buffer = key[len(key)-1-i] + buffer
        return skipList

    def findSuffixPosition(self,badchar, suffix, full_term):
        for offset in range(1, len(full_term)+1)[::-1]:
            flag = True
            for suffix_index in range(0, len(suffix)):
                term_index = offset-len(suffix)-1+suffix_index
                if term_index < 0 or suffix[suffix_index] == full_term[term_index]:
                    pass
                else:
                    flag = False
            term_index = offset-len(suffix)-1
            if flag and (term_index <= 0 or full_term[term_index-1] != badchar):
                return len(full_term)-offset+1


class BmSearch(threading.Thread):
    def _init_(self):
        threading.Thread.__init__(self)

    def run(self):
        needle = self.needle
        haystack = self.haystack
        goodSuffix = self.goodSuffix
        badChar = self.badChar

        i = 0
        while i < len(haystack)-len(needle)+1:
            j = len(needle)
            while j > 0 and needle[j-1] == haystack[i+j-1]:
                j -= 1
            if j > 0:
                badCharShift = badChar.get(haystack[i+j-1], len(needle))
                goodSuffixShift = goodSuffix[len(needle)-j]
                if badCharShift > goodSuffixShift:
                    i += badCharShift
                else:
                    i += goodSuffixShift
            else:
                self.value = i
                return
        self.value = -1
        return

# Actual Search Algorithm
def BMSearch(haystack, needle):
    first = haystack[:int(len(haystack)/2)]
    second = haystack[int(len(haystack)/2):]
    goodSuffix = None
    badChar = None

    #setting good suffix and bad character here
    try:
        thread1 = SuffixShift(needle)
        thread2 = BadCharShift(needle)
        thread1.start()
        thread2.start()
        #waiting for the threads to be finished...
        thread1.join()
        thread2.join()
        #checking whether threads have finished
        if  not(thread1.is_alive() or thread2.is_alive()):
            goodSuffix = thread1.skipList
            badChar = thread2.skipList
        else:
            return -1
    except Exception as ex:
        print("Thread Error ",ex)
        return -1

    
    thread1 = BmSearch()
    thread1.haystack = haystack
    thread1.needle = needle
    thread1.badChar = badChar
    thread1.goodSuffix = goodSuffix
    thread1.start()

    thread2 = BmSearch()
    thread2.haystack = haystack
    thread2.needle = needle
    thread2.badChar = badChar
    thread2.goodSuffix = goodSuffix
    thread2.start()

    thread1.join()
    thread2.join()

    if  not (thread1.is_alive() and thread2.is_alive()):
        if thread1.value == -1:
            if thread2.value != -1:
                return thread2.value + len(thread1.haystack)
            else :
                return -1
        else: 
            return thread1.value
    else:
        return -1

if __name__ == "__main__":
    block = "This is a simple example"
    data = open('testData_all_1.txt','r')
    text = data.read()
    data = open('patterns_all.txt','r')
    pattern = data.read()
    print(text)
    start = time.process_time()
    result = BMSearch(text,pattern)
    end = time.process_time()
    print("pattern found at ",result)
    print("User + System Time for the Task in seconds: ",end-start)
