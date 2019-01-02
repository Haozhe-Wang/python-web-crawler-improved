from urllib import request,parse,error
import re

import os
import http.cookiejar

class DownloadPage(object):
    def __init__(self,url):
        self._readed=None
        self._url=url
        self._content=''
        self._contentsPointer=-1
        self._contents=[]
        self._saves={}

    def setUrl(self,url):
        self._url=url
    def getUrl(self):
        return self._url
    def getPage(self):
        return self._content
    def getSaves(self):
        return self._saves
    #add the current page to the opened page list
    def _savePage(self):
        if self._content != '':
            if self._contentsPointer==len(self._contents)-1:
                self._contents.append(self._content)
                self._contentsPointer+=1
            else:
                self._contents=self._contents[:self._contentsPointer+1]
                self._savePage()
    #save to the current page to the saving page list
    def savePage(self):
        if self._content != '':
            n=name=self._url.split('/')[-1]
            i=1
            while name in self._saves:
                name='%s(%d)'%(n,i)
                i+=1
            # self._saves[name]=self._url
            self._saves[name] = self._readed
    def goNextPage(self):
        if not self._contentsPointer==len(self._contents)-1:
            self._contentsPointer+=1
            self._content=self._contents[self._contentsPointer]
    def goLastPage(self):
        if not self._contentsPointer==0:
            self._contentsPointer-=1
            self._content=self._contents[self._contentsPointer]
    def _getEncode(self,page):
        pattern=re.compile(b'<meta[^>]+charset\s*=\s*"*([^>\s"]+)[\s"][^>]*>')
        match=pattern.search(page)
        try:
            return match.group(1).decode('ascii')
        except:
            return None
    #save all pages of the saving page list
    def saveAll(self):
        '''for name,url in self._saves.items():
            #dir=os.getcwd()
            opener=request.urlopen(url)
            f=open(name+'.html','wb')

            block_sz = 8192
            while True:
                buffer = opener.read(block_sz)
                if not buffer:
                    break

                f.write(buffer)
            f.close()'''
        for name,content in self._saves.items():
            f = open(name + '.html', 'wb')
            f.write(content)
            f.close()

    def refineLinks(self,content):
        pattern=re.compile('(<[^>]+(href|src)\s*=\s*"\s*)(//[^>"]+)(\s*"[^>]*>)')
        content=pattern.sub(r'\1http:\3\4',content)
        pattern = re.compile('(<[^>]+(href|src)\s*=\s*"\s*)(/[^>"]+)(\s*"[^>]*>)')
        path=self._url.split('/')
        domain='/'.join(path[:3])
        content=pattern.sub(r'\1'+domain+r'\3\4',content)
        pattern = re.compile('(<[^>]+(href|src)\s*=\s*"\s*)((?!(http:|https:|ftp:))(\.\./)*[^>"]+)(\s*"[^>]*>)')
        def repalce(match):
            relative_url=match.group(3).split('/')
            iter_path=path[:-1]
            while relative_url[0]=='..':
                iter_path=iter_path[:-1]
                relative_url=relative_url[1:]
            new_url='/'.join(iter_path)+'/'+'/'.join(relative_url)
            return match.group(1)+new_url+match.group(6)

        content = pattern.sub(repalce, content)

        return content

    def refineBinaryLinks(self,readed):
        pattern = re.compile(b'(<[^>]+(href|src)\s*=\s*"\s*)(//[^>"]+)(\s*"[^>]*>)')
        readed = pattern.sub(br'\1http:\3\4', readed)
        pattern = re.compile(b'(<[^>]+(href|src)\s*=\s*"\s*)(/[^>"]+)(\s*"[^>]*>)')
        path = self._url.split('/')
        domain = '/'.join(path[:3])
        readed = pattern.sub(br'\1' + bytes(domain,'ascii') + br'\3\4', readed)
        pattern = re.compile(b'(<[^>]+(href|src)\s*=\s*"\s*)((?!(http:|https:|ftp:))(\.\./)*[^>"]+)(\s*"[^>]*>)')

        def repalce(match):
            relative_url = match.group(3).split(b'/')
            iter_path = path[:-1]
            while relative_url[0] == b'..':
                iter_path = iter_path[:-1]
                relative_url = relative_url[1:]
            new_url = bytes('/'.join(iter_path),'ascii') + b'/' + b'/'.join(relative_url)
            return match.group(1) + new_url + match.group(6)

        readed = pattern.sub(repalce, readed)

        return readed

    def downloadFile(self,url,filename):
        testfile = request.URLopener()
        testfile.retrieve(url, filename)


    def urlopen(self):
        try:
            opener=request.urlopen(self._url)
            self._readed= opener.read()
        except error.HTTPError:
            self._content = ''
            self._readed =None
            raise PageNotFound('Can not find the page. Please check if the page matches the server')
        except error.URLError as e:
            self._content = ''
            self._readed = None
            raise NoServerFound('Wrong web server name. Cannot find the server\nReason: %s'%str(e.reason))
        except Exception as e:
            self._content = ''
            self._readed = None
            raise urlError('Error Msg: %s'%str(e))

        try:
            decoding = self._getEncode(self._readed)
            if not decoding:
                decoding = 'UTF-8'
            # As gb18030 has bigger character set, and works more properly
            if decoding == 'gb2312':
                decoding = 'gb18030'
            self._content = self._readed.decode(decoding)
            self._content = self.refineLinks(self._content)
        except:
            self._content='<body><p><b>Cannot decode page content!（不能解码网页内容）</b></p><p>However, Page has been successfully received!（但是网页已获取）</p></body>'

        self._readed = self.refineBinaryLinks(self._readed)
        self._savePage()


    url=property(getUrl,setUrl)
    content=property(getPage)
    saves=property(getSaves)

class NoServerFound(Exception):
    pass
class PageNotFound(Exception):
    pass
class urlError(Exception):
    pass

if __name__=='__main__':

    down=DownloadPage('https://www.51test.net/show/9169567.html')
    down.urlopen()
    down.savePage()
    down.saveAll()
    '''down.urlopen()

    down.url='https://cs1.ucc.ie/~hw7/table.html'
    down.urlopen()
    print(down.content)
    print(len(down._contents))'''

