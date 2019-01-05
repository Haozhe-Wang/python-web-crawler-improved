from crawWebpages import DownloadPage
from tkinter import *
class DownloadPageGUI():
    def __init__(self,root):
        self._root=root
        self.setWindow()
        self.setShowPageFrame()
        self.enterUrlFrame()
        self.setPageAttributeFrame()
        self.savePage()

    def setWindow(self):
        self._root.title('Webpage download')
    def setShowPageFrame(self):
        self._showPageFrame = Frame(self._root)
        self._showPageFrame.pack(fill=X)
        self._showPagelabel = Label(self._showPageFrame, text='Page show(展示网页)')
        self._showPage = Text(self._showPageFrame, height=40, width=200)
        self._showPage.grid(row=2, column=1)
        self._showPagelabel.grid(row=1, column=1)
    def enterUrlFrame(self):
        self._urlEntryFrame=Frame(self._root)
        self._urlEntryFrame.pack(fill=X)
        self._urlEntryLabel=Label(self._urlEntryFrame,text='Enter Url(链接输入)',justify=CENTER)
        self._urlEntry=Entry(self._urlEntryFrame,width=60)
        self._urlEntryButton=Button(self._urlEntryFrame,text='Preview Page(预览网页)',justify=CENTER)
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
        self._imageRetrivingFrame.pack(side=LEFT)
        self._CssRetrivingFrame.pack(side=LEFT)
        self._scriptRemovingFrame.pack(side=LEFT)


    def setFiletypesFrame(self):
        self._filetypesFrame = Frame(self._pageAttributeFrame)
        self._filetypesLabel = Label(self._filetypesFrame, text='Add file extension(添加文件扩展名)', justify=CENTER)
        self._filetypesEntry = Entry(self._filetypesFrame, width=20)
        self._filetypesButton = Button(self._filetypesFrame, text='add(添加)')
        self._filetypesAdded = Frame(self._filetypesFrame, width=40, height=3)
        self._filetypesFrame.pack(fill=X)
        self._filetypesLabel.pack(side=TOP)
        self._filetypesEntry.pack(side=LEFT)
        self._filetypesButton.pack(side=RIGHT)
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
    def savePage(self):
        self._saveButton = Button(self._root, text='Save page',bg='lightgreen')
        self._saveButton.pack()
    def imageRetrivingTrue(self):
        pass
    def imageRetrivingFalse(self):
        pass
    def CssRetrivingTrue(self):
        pass
    def CssRetrivingFalse(self):
        pass
    def removeScriptTrue(self):
        pass
    def removeScriptFalse(self):
        pass



if __name__ == '__main__':
    root=Tk()
    download=DownloadPageGUI(root)
    root.mainloop()