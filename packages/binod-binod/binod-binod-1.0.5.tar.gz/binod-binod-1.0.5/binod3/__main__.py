def main():
    def fun(path):
        import ctypes
        SPI_WALLPAPER =0x14
        SPIF_UPDATINGFILE= 0x2
        path=path+'\\00000001.jpg'
        ctypes.windll.user32.SystemParametersInfoW(SPI_WALLPAPER,0,path,SPIF_UPDATINGFILE)
    import os
    path=os.getcwd()
    from urllib import request
    f = open('00000001.jpg', 'wb')
    f.write(request.urlopen("https://i.ibb.co/QktFXHD/binod.png").read())
    f.close()
    fun(path)
    #os.system('cmd /c "binod"')
if __name__ == '__main__':
    main()
