from urllib import request,parse,error
import re

import os
import http.cookiejar

class DownloadPage(object):
    def __init__(self,url):
        # This will be storing binary content
        self._readed=None
        self._url=url
        self._decoding=''
        self._content=''
        self._contentsPointer=-1
        self._contents=[]
        self._saves={}

        self._retrive_filetypes=set()
        self._retrive_images=True
        self._retrive_css=True
        self._remove_script=False
        self._script_removed=False

    def setUrl(self,url):
        self._url=url
    def getUrl(self):
        return self._url
    def getPage(self):
        return self._content
    def setPage(self,content):
        self._content=content
        self._readed=bytes(self._content,self._decoding)
    def getSaves(self):
        return self._saves

    #add file types
    def setFiletypes(self,filetype):
        self._retrive_filetypes.add(str(filetype))
    def removeFiletypes(self,filetype):
        if filetype in self._retrive_filetypes:
            self._retrive_filetypes.remove(filetype)

    #set to download all images
    def setImageRetrivingTrue(self):
        self._retrive_images=True
    # set not to download all images
    def setImageRetrivingFalse(self):
        self._retrive_images=False

    # set to download all stylesheets
    def setCssRetrivingTrue(self):
        self._retrive_css=True
    # set not to download all stylesheets
    def setCssRetrivingFalse(self):
        self._retrive_css=False

    # set to remove all javascripts
    def setScriptRemovalTrue(self):
        self._remove_script=True
    # set not to remove all javascripts
    def setScriptRemovalFalse(self):
        self._remove_script=False
    
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
    #go to next page that has been fetched
    def goNextPage(self):
        if not self._contentsPointer==len(self._contents)-1:
            self._contentsPointer+=1
            self._content=self._contents[self._contentsPointer]
    #go back to the last page that has been fetched
    def goLastPage(self):
        if not self._contentsPointer==0:
            self._contentsPointer-=1
            self._content=self._contents[self._contentsPointer]
    def _getEncode(self,page):
        pattern=re.compile(b'<meta[^>]+charset[\s\n]*=[\s\n]*"*([^>\s\n"]+)[\s\n"][^>]*>')
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
            content=self.downloadAllToFolder(name,content)
            self._saves[name]=content
            f = open(name + '.html', 'wb')
            f.write(content)
            f.close()

    '''
    #convert every links to absolute url with http prefixed
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
    '''

    def refineBinaryLinks(self,readed):
        pattern = re.compile(b'(<[^>]+(href|src)[\s\n]*=[\s\n]*"[\s\n]*)(//[^>"]+)([\s\n]*"[^>]*>)')
        readed = pattern.sub(br'\1http:\3\4', readed)
        pattern = re.compile(b'(<[^>]+(href|src)[\s\n]*=[\s\n]*"[\s\n]*)(/[^>"]+)([\s\n]*"[^>]*>)')
        path = self._url.split('/')
        domain = '/'.join(path[:3])
        readed = pattern.sub(br'\1' + bytes(domain,'ascii') + br'\3\4', readed)
        pattern = re.compile(b'(<[^>]+(href|src)[\s\n]*=[\s\n]*"[\s\n]*)((?!(http:|https:|ftp:))(\.\./)*[^>"]+)([\s\n]*"[^>]*>)')

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
    def changeDirectory(self,path):
        os.chdir(path)
    def createDirectory(self,folderName):
        current = os.getcwd()
        folder = os.path.join(current, folderName)
        if not os.path.exists(folder):
            os.mkdir(folder)
        return folder,current
    def downloadAllToFolder(self,folderName,content):
        folder,current=self.createDirectory(folderName)
        os.chdir(folder)
        content,_=self.downloadFiles(content)
        #down load stylesheets
        content=self.tagDownloadAndChangeLink(content,self._retrive_css,'StyleSheets',rb'<\s*link [^>]*(rel[\s\n]*=[\s\n]*"[\s\n]*stylesheet[\s\n]*")?[^>]*href[\s\n]*=[\s\n]*"[\s\n]*([^>"\n]+)\n*"(?(1)[^>]*|[^>]*rel[\s\n]*=[\s\n]*"[\s\n]*stylesheet[\s\n]*"[^>]*)>',2)
        #down load all images
        content = self.tagDownloadAndChangeLink(content,self._retrive_images,'Images',br'<\s*img [^>]*src[\s\n]*=[\s\n]*"[\s\n]*([^>"\n]+)[\s\n]*"[^>]*>',1)
        os.chdir(current)
        return content

    #disabale or enable javascript in html
    def setJavascript(self):
        if self._remove_script != self._script_removed:
            if self._remove_script and not self._script_removed:
                pattern=re.compile(rb'(?<!<!--)(<\s*script[^>]*>(.|\n)*?<\s*/script\s*>)')
                self._readed=pattern.sub(rb'<!-- (UNSCRIPTION) \1 -->',self._readed)
                self._script_removed=True
            else:
                pattern = re.compile(b'<!--\s*\(UNSCRIPTION\) (<\s*script[^>]*>(.|\n)*?<\s*/script\s*>)\s*-->')
                self._readed=pattern.sub(rb'\1',self._readed)
                self._script_removed=False

            self._content=self._readed.decode(self._decoding)

    #this function is used to download all linked files( which can be stylesheets, images and so on), and also this function will modify the links to local path
    #content: is binary content of the page
    #whether: specify if user want to download this particular document
    #directoryName: specify the directory name to store the documents
    #patternDescription: specify the pattern of the link(or tag) to match
    #groupNo: specify the group for the link in order to replace the absolute link to the location of local path
    def tagDownloadAndChangeLink(self,content,whether,directoryName,patternDescription,groupNO):
        if whether:
            folder,current=self.createDirectory(directoryName)
            os.chdir(folder)
            pattern=re.compile(patternDescription)

            def replace(match):
                url=match.group(groupNO).decode('ascii')
                name=url.split('/')[-1]
                try:
                    self.download(url,name)
                    path = os.path.join(folder, name)
                    return match.group(0).replace(match.group(groupNO),bytes(path,self._decoding))
                except:
                    return match.group(0)

            content=pattern.sub(replace,content)
            os.chdir(current)
        return content


    #download every file which are given by the file extensions
    def downloadFiles(self,content):
        downloadresult={}
        folder,current=self.createDirectory('Files')
        os.chdir(folder)
        for extension in self._retrive_filetypes:
            folderExtension,_=self.createDirectory(extension)
            os.chdir(folderExtension)
            downloaded=0
            total=0
            NoLoad=[]
            pattern=re.compile(br"<[^>]+((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*/([a-zA-Z0-9\r_-]+\."+bytes(extension,'ascii')+b")[?=a-zA-Z0-9_]*)[^>]*>")
            files = pattern.findall(content)
            for file in files:
                try:
                    self.download(file[0].decode('ascii'),file[-1].decode('ascii'))
                    downloaded += 1
                except:
                    NoLoad.append(file[0].decode('ascii'))
                finally:
                    total+=1
            os.chdir(folder)
            downloadresult[extension]=[downloaded,total,NoLoad]
        os.chdir(current)
        return content,downloadresult

    def download(self,url,filename):
        testfile = request.URLopener()
        testfile.retrieve(url, filename)


    def urlopen(self):
        try:
            opener=request.urlopen(self._url)
            self._readed= opener.read()
            self._readed = self.refineBinaryLinks(self._readed)
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
            self._decoding=decoding
            self._content = self._readed.decode(decoding)
        except:
            self._content='<body><p><b>Cannot decode page content!（不能解码网页内容）</b></p><p>However, Page has been successfully received!（但是网页已获取）</p></body>'

        self._savePage()


    url=property(getUrl,setUrl)
    content=property(getPage,setPage)
    saves=property(getSaves)

class NoServerFound(Exception):
    pass
class PageNotFound(Exception):
    pass
class urlError(Exception):
    pass

if __name__=='__main__':

    down=DownloadPage('https://www.ielts.org/about-the-test/sample-test-questions')
    down.urlopen()

    '''
    #can remove javascript
    down.setScriptRemovalTrue()
    down.setJavascript()
    down.setScriptRemovalFalse()
    down.setJavascript()
    '''

    '''
    # change downloading directory
    # down.changeDirectory('D:\python爬虫教程\pythonCrawlers')
    '''


    down.savePage()


    #download pdf files from the page
    # down.setFiletypes('pdf')
    down.setFiletypes('ashx')


    down.saveAll()


    '''down.urlopen()

    down.url='https://cs1.ucc.ie/~hw7/table.html'
    down.urlopen()
    print(down.content)
    print(len(down._contents))'''

