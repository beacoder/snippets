--[[
   following script will generate log files for Debug Failing Cycles
]]

do

   local path = "/opt/hsm/src/execution_engine/TEST.hsm/devices/moscato_ddr3_validation_256sites_r1.0.0/error_simulation/sh_libs/";
   local patterns = {"march6n_1333-999_feat46_label1_all_fail"};
   local pins = {"DQ.00", "DQ.01", "DQ.02", "DQ.03", "DQ.04", "DQ.05", "DQ.06", "DQ.07", "DQS", "DQSn"};
   local sites = 256;
   local templateLog = "template.log";
   local contents = "";

   function GenFailCycleLogs(filename, contents)      
      local log = assert(io.open(filename, "w+"));
      log:write(contents);
      log:flush();
   end

   -- read fail cycles in template log file
   assert(io.input(templateLog));
   contents = io.read("*all");

   for index1 = 1, sites, 1 do
      local site = index1;
      
      for index2 = 1, #patterns do
	 local pattern = patterns[index2];

	 for index3 = 1, #pins do
	    local pin = pins[index3];
	    
	    local filename = path .. site .. "_" .. pattern .. "_" .. pin .. ".log";
	    GenFailCycleLogs(filename, contents)
	 end
      end
   end

end
