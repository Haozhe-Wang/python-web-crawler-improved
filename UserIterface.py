from crawWebpages import DownloadPage
from tkinter import *
class DownloadPageGUI():
    def __init__(self,root):
        self._root=root
        self.setWindow()
        self.setShowPageFrame()
        self.enterUrlFrame()
        self.setPageAttributeFrame()
        self.savePageButton()
        self._page=None

    def setWindow(self):
        self._root.title('Webpage download')
    def setShowPageFrame(self):
        self._showPageFrame = Frame(self._root)
        self._showPageFrame.pack(fill=X)
        self._showPagelabel = Label(self._showPageFrame, text='Show Page(展示网页)')
        self._showPage = Text(self._showPageFrame, height=40, width=200)
        self._scroll = Scrollbar(self._showPageFrame, command=self._showPage.yview)
        self._showPage.configure(yscrollcommand=self._scroll.set)
        self._showPagelabel.pack()
        self._showPage.pack(side=LEFT)
        self._scroll.pack(side=RIGHT,fill=Y)

    def enterUrlFrame(self):
        self._urlEntryFrame=Frame(self._root)
        self._urlEntryFrame.pack(fill=X)
        self._urlEntryLabel=Label(self._urlEntryFrame,text='Enter Url(链接输入)',justify=CENTER)
        self._urlEntry=Entry(self._urlEntryFrame,width=60)
        self._urlEntryButton=Button(self._urlEntryFrame,text='Preview Page(预览网页)',justify=CENTER,command=self.preview)
        self._urlEntryLabel.pack(side=LEFT,padx=100)
        self._urlEntry.pack(side=LEFT,padx=10)
        self._urlEntryButton.pack(side=LEFT,padx=10)
    def setPageAttributeFrame(self):
        self._pageAttributeFrame=Frame(self._root)
        self._pageAttributeFrame.pack()
        self.setFiletypesFrame()
        #set image selection
        self._imageRetrivingFrame=self.setSelectAttribute(self._pageAttributeFrame,'Retriving webpage Image (获取网页图片)',
                                                          self.imageRetrivingTrue,self.imageRetrivingFalse)
        #set sytlesheet selection
        self._CssRetrivingFrame = self.setSelectAttribute(self._pageAttributeFrame, 'Retriving webpage Stylesheet (获取网页样式表)',
                                                       self.CssRetrivingTrue, self.CssRetrivingFalse)
        #set script removal
        self._scriptRemovingFrame = self.setSelectAttribute(self._pageAttributeFrame, 'Remove webpage script (移除网页脚本)',
                                                       self.removeScriptTrue, self.removeScriptFalse)
        self._imageRetrivingFrame.pack(side=LEFT,padx=10)
        self._CssRetrivingFrame.pack(side=LEFT,padx=10)
        self._scriptRemovingFrame.pack(side=LEFT,padx=10)


    def setFiletypesFrame(self):
        self._filetypesFrame = Frame(self._pageAttributeFrame)
        self._filetypesLabel = Label(self._filetypesFrame, text='Add file extension(添加文件扩展名)', justify=CENTER)
        self._filetypesEntry = Entry(self._filetypesFrame, width=20)
        self._filetypesButton = Button(self._filetypesFrame, text='add(添加)',command=self.addFile)
        self._filetypesAdded = Frame(self._filetypesFrame, width=40, height=3)
        self._filetypesFrame.pack()
        self._filetypesLabel.pack(side=TOP)
        self._filetypesEntry.pack(side=LEFT,padx=10)
        self._filetypesButton.pack(side=RIGHT,padx=10)
        self._filetypesAdded.pack(side=BOTTOM)
    def setSelectAttribute(self,parentFrame,text,commandTrue,commandFalse):
        frame=Frame(parentFrame)
        label=Label(frame,text=text)
        selection = BooleanVar()
        radioTrue=Radiobutton(frame,text='True',value=True,command=commandTrue,variable=selection,tristatevalue=3)
        radioFalse = Radiobutton(frame, text='False', value=False, command=commandFalse,variable=selection,tristatevalue=3)
        label.pack(side=LEFT)
        radioTrue.pack(side=LEFT)
        radioFalse.pack(side=LEFT)
        return frame
    def savePageButton(self):
        self._savePageFrame=Frame(self._root)
        self._savePageFrame.pack()
        self._saveButton = Button(self._savePageFrame, text='Save page',bg='lightgreen',command=self.savePage)
        self._saveButton.pack()
        self._errorLabel = None
    def preview(self):
        url=self._urlEntry.get()
        self._page=DownloadPage(url)
        self._page.urlopen()
        self._showPage.delete(1.0,'end')
        self._showPage.insert('end',self._page.content)
    def imageRetrivingTrue(self):
        if self._page:
            self._page.setImageRetrivingTrue()
    def imageRetrivingFalse(self):
        if self._page:
            self._page.setImageRetrivingFalse()
    def CssRetrivingTrue(self):
        if self._page:
            self._page.setCssRetrivingTrue()
    def CssRetrivingFalse(self):
        if self._page:
            self._page.setCssRetrivingFalse()
    def removeScriptTrue(self):
        if self._page:
            self._page.setScriptRemovalTrue()
            self._page.setJavascript()
            self._showPage.delete(1.0, 'end')
            self._showPage.insert('end', self._page.content)
    def removeScriptFalse(self):
        if self._page:
            self._page.setScriptRemovalFalse()
            self._page.setJavascript()
            self._showPage.delete(1.0, 'end')
            self._showPage.insert('end', self._page.content)
    def addFile(self):
        filetype=self._filetypesEntry.get()
        if filetype and self._page:
            self._filetypesEntry.delete(0,'end')
            self._page.setFiletypes(filetype)
            label=Label(self._filetypesAdded,text=filetype,cursor='hand2',borderwidth=2,relief='ridge')
            label.pack(side=LEFT,padx=2,ipadx=1)
            label.bind("<Enter>", lambda event, h=label: h.configure(bg="red"))
            label.bind("<Leave>", lambda event, h=label: h.configure(bg="white"))
            label.bind('<Button-1>',lambda event: self.removeFile(label))

    def removeFile(self,label):
        filetype=label['text']
        self._page.removeFiletypes(filetype)
        label.pack_forget()

    def savePage(self):
        if self._page:
            self._page.savePage()
            self._page.saveAll()
            if self._errorLabel:
                self._errorLabel.pack_forget()
                self._errorLabel=None
        else:
            if not self._errorLabel:
                self._errorLabel=Label(self._savePageFrame,text='Please Preview Page First(请先预览网页)',bg='red')
                self._errorLabel.pack()


if __name__ == '__main__':
    root=Tk()
    download=DownloadPageGUI(root)
    root.mainloop()