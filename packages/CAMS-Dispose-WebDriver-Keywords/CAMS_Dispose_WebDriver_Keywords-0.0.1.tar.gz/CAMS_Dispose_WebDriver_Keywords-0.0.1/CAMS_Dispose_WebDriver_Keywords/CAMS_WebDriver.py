def DisposeWebDriver(self):
        """
        Closes the browser and shuts down the ChromeDriver executable
        that is started when starting the ChromeDriver
        """			
        try:
            self._debug('Closing all browsers')
            
            browser.dispose(self)
            browser.quit(self)
            self._cache.close_all()
            self.empty_cache()
            RemoteWebDriver.close(self)
            Thread.Sleep(3000)
            RemoteWebDriver.quit(self)
            RemoteWebDriver.dispose(self)
            RemoteWebDrive = null
            WindowsUtils.KillProcessAndChildren("C:\Program Files\Python38\Scripts\chromedriver.exe") 
        except:
            # We don't care about the message because something probably has gone wrong
            pass
