#!/bin/bash

#demonstrate how to change and restore umask

#umask value => file permission
#0022 => "666-22" => "644" => rw-r--r--
#0002 => "666-2" => "664" => rw-rw-r--

#global varialbes
old=0
new=0

#save old umask
old=$(umask)
echo old 'umask' is "$old"

#set new umask
umask 0002
new=$(umask)
echo new 'umask' is "$new"

#restore old umask
umask $old
echo current 'umask' is "$(umask)"
