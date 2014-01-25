--[[
   get processID of TestMethodManager
]]

do

   -- delete old log files
   os.execute("rm -f /home/brightc/Desktop/proc-id.log /home/brightc/Desktop/Thread-Count.log");

   -- write testmethodmanager processID into logfile
   os.execute("pgrep -f TestMethodManager | awk 'NR==1' >> /home/brightc/Desktop/proc-id.log");
   
end
