--[[
   1. count running thread count of the processID
   2. print memory usage info
]]

do

   -- count the thread counts according to the processID
   assert(io.input("/home/brightc/Desktop/proc-id.log"));

   local procID = io.read("*number");
   local command = string.format("ps uH p %d | wc -l >> %s", procID, "/home/brightc/Desktop/Thread-Count.log");   
   os.execute(command);

   -- output memory usage info log
   command = "free | awk 'NR==2' | awk '{print $(3)}' >> /home/brightc/Desktop/SMC-Memory.log";
   os.execute(command);

   -- insert a blank line
   --[[
   os.execute("echo >> /home/brightc/Desktop/SMC-Memory.log")
   os.execute(command);
   ]]
   
end
